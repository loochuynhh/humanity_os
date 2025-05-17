from django.db import models
from django.utils import timezone
from django.db.models import Sum
from projects.models import TimeEntries 


class KPIs(models.Model):
    KPI_TYPES = [
        ("Quantitative", "Quantitative"),
        ("Qualitative", "Qualitative"),
        ("Efficiency", "Efficiency"),
        ("Quality", "Quality"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    kpi_type = models.CharField(max_length=20, choices=KPI_TYPES, default="Quantitative")
    unit = models.CharField(max_length=20, null=True, blank=True)
    weight = models.FloatField(default=1.0, help_text="Weight for overall performance calculation")
    project = models.ForeignKey(
        "projects.Projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="kpis",
        help_text="Optional: Link to a specific project"
    )

    class Meta:
        db_table = "kpis"

    def __str__(self):
        return self.name


class EmployeeKPIs(models.Model):
    TIME_PERIODS = [
        ("Weekly", "Weekly"),
        ("Monthly", "Monthly"),
        ("Quarterly", "Quarterly"),
        ("Yearly", "Yearly"),
    ]

    EVALUATION_LEVELS = [
        ("Exceeded", "Exceeded"),
        ("Achieved", "Achieved"),
        ("Partially Achieved", "Partially Achieved"),
        ("Not Achieved", "Not Achieved"),
    ]

    user = models.ForeignKey("users.Users", on_delete=models.CASCADE, related_name="kpis")
    kpi = models.ForeignKey("kpis.KPIs", on_delete=models.CASCADE, related_name="employee_kpis")
    target_value = models.FloatField()
    actual_value = models.FloatField(null=True, blank=True)
    achieved_percentage = models.FloatField(default=0.0, help_text="Percentage of target achieved")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    time_period = models.CharField(max_length=20, choices=TIME_PERIODS, default="Monthly")
    evaluation = models.CharField(
        max_length=20,
        choices=EVALUATION_LEVELS,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "employee_kpis"
        indexes = [
            models.Index(fields=['user', 'start_date']),
            models.Index(fields=['kpi', 'time_period']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.kpi.name} ({self.time_period})"

    def calculate_achieved_percentage(self):
        """Calculate achieved percentage based on actual_value and target_value."""
        if self.actual_value is not None and self.target_value > 0:
            self.achieved_percentage = (self.actual_value / self.target_value) * 100
            self.achieved_percentage = min(self.achieved_percentage, 200)
        else:
            self.achieved_percentage = 0
        self.save()

    def update_evaluation(self):
        """Update evaluation based on achieved percentage."""
        if self.achieved_percentage >= 120:
            self.evaluation = "Exceeded"
        elif self.achieved_percentage >= 100:
            self.evaluation = "Achieved"
        elif self.achieved_percentage >= 50:
            self.evaluation = "Partially Achieved"
        else:
            self.evaluation = "Not Achieved"
        self.save()

    def update_from_project(self):
        """Update actual_value based on project data."""
        if self.kpi.project and self.kpi.kpi_type == "Quantitative":
            # Lấy tất cả task_assignments của user trong project
            task_assignments = self.user.task_assignments.filter(
                task__project=self.kpi.project
            )
            
            # Lọc time_entries thông qua task_assignment
            time_entries = TimeEntries.objects.filter(
                task_assignment__in=task_assignments,
                start_time__gte=self.start_date,
                start_time__lte=self.end_date
            )
            
            # Lấy các task được gán cho user trong khoảng thời gian
            tasks = self.kpi.project.tasks.filter(
                task_assignments__user=self.user,
                deadline__gte=self.start_date,
                deadline__lte=self.end_date
            ).distinct()
            
            if self.kpi.name.lower().find("time spent") != -1:
                self.actual_value = time_entries.aggregate(total=Sum('duration'))['total'] or 0.0
            elif self.kpi.name.lower().find("task completion") != -1:
                completed_tasks = tasks.filter(status="Completed").count()
                total_tasks = tasks.count()
                self.actual_value = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0
            elif self.kpi.name.lower().find("bug rate") != -1:
                self.actual_value = time_entries.aggregate(total=Sum('duration'))['total'] or 0.0
            
            self.calculate_achieved_percentage()
            self.update_evaluation()
        
        self.save()