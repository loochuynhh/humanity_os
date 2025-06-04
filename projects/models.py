# projects/models.py
from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.core.exceptions import ValidationError


class Projects(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    manager = models.ForeignKey(
        "users.Users",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_projects",
    )
    team_members = models.ManyToManyField(
        "users.Users",
        through="TeamProjectMembership",
        related_name="projects"
    )

    class Meta:
        db_table = "projects"
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name


class Tasks(models.Model):
    STATUS_CHOICES = [
        ("To-do", "To-do"),
        ("In progress", "In progress"),
        ("Completed", "Completed"),
        ("Late", "Late"),
    ]

    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    project = models.ForeignKey("projects.Projects", on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="To-do")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default="Medium") 
    estimated_time = models.FloatField(null=True, blank=True)
    github_link = models.URLField(null=True, blank=True)
    total_time = models.FloatField(default=0.0)
    is_tracking = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)  
    completed_date = models.DateTimeField(null=True, blank=True) 
    
    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        indexes = [
            models.Index(fields=['deadline']),
            models.Index(fields=['status']),
            models.Index(fields=['start_date']),
        ]

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        return self.deadline.date() < timezone.now().date() and self.status != "Completed"

    @property
    def days_until_deadline(self):
        return (self.deadline.date() - timezone.now().date()).days
    
    def update_start_date(self):
        """Cập nhật ngày bắt đầu dựa trên TimeEntry đầu tiên của task"""
        # Lấy TimeEntry đầu tiên từ tất cả TaskAssignment của task này
        earliest_entry = TimeEntries.objects.filter(
            task_assignment__task=self
        ).order_by('start_time').first()
        
        self.start_date = earliest_entry.start_time if earliest_entry else None
        self.save(update_fields=['start_date'])

    def update_total_time(self):
        """Cập nhật tổng thời gian thực tế từ tất cả TaskAssignment"""
        # Tính tổng thời gian từ tất cả TaskAssignment
        total = TaskAssignments.objects.filter(task=self).aggregate(
            total=Sum('actual_time')
        )['total'] or 0
        
        self.total_time = total
        self.save(update_fields=['total_time'])

    def update_status_from_assignments(self):
        """Cập nhật trạng thái task dựa trên trạng thái của các TaskAssignment"""
        assignments = TaskAssignments.objects.filter(task=self)
        
        if not assignments.exists():
            self.status = "To-do"
            self.completed_date = None
            self.save(update_fields=['status', 'completed_date'])
            return
            
        if all(assignment.status == "Completed" for assignment in assignments):
            self.status = "Completed"
            if not self.completed_date:
                self.completed_date = timezone.now()
        elif self.is_overdue:
            self.status = "Late"
        elif any(assignment.status == "In progress" for assignment in assignments):
            self.status = "In progress"
        else:
            self.status = "To-do"
        
        self.save(update_fields=['status', 'completed_date'])


class TaskAssignments(models.Model):
    ROLE_CHOICES = [
        ("Thực hiện chính", "Thực hiện chính"),
        ("Đồng thực hiện", "Đồng thực hiện"),
        ("Review", "Review"),
        ("Test", "Test"),
        ("Khác", "Khác"),
    ]
    
    task = models.ForeignKey("projects.Tasks", on_delete=models.CASCADE, related_name="task_assignments")
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE, related_name="task_assignments")
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="Thực hiện chính")
    estimated_time = models.FloatField(null=True, blank=True)
    actual_time = models.FloatField(default=0.0)
    status = models.CharField(
        max_length=20,
        choices=Tasks.STATUS_CHOICES,
        default="To-do"
    )
    
    class Meta:
        db_table = "task_assignments"
        verbose_name = "Task Assignment"
        verbose_name_plural = "Task Assignments"
        unique_together = ("task", "user", "role")
        indexes = [
            models.Index(fields=['task', 'user']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.task.title} - {self.user.username} ({self.role})"
    
    def update_actual_time(self):
        """Cập nhật thời gian thực tế từ các TimeEntries"""
        total = TimeEntries.objects.filter(task_assignment=self).aggregate(
            total=Sum('duration')
        )['total'] or 0
        
        self.actual_time = total
        self.save(update_fields=['actual_time'])
        
        # Cập nhật tổng thời gian của task
        self.task.update_total_time()


class TimeEntries(models.Model):
    task_assignment = models.ForeignKey("projects.TaskAssignments", on_delete=models.CASCADE, related_name="time_entries")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "time_entries"
        verbose_name = "Time Entry"
        verbose_name_plural = "Time Entries"
        indexes = [
            models.Index(fields=['task_assignment', 'start_time']),
            models.Index(fields=['start_time']),
        ]

    def __str__(self):
        return f"{self.task_assignment.user.username} - {self.task_assignment.task.title} ({self.start_time})"

    def clean(self):
        """Kiểm tra end_time > start_time"""
        if self.end_time and self.start_time and self.end_time <= self.start_time:
            raise ValidationError("Thời gian kết thúc phải lớn hơn thời gian bắt đầu.")
            
    def save(self, *args, **kwargs):
        # Kiểm tra điều kiện trước khi lưu
        self.clean()
        
        # Tính duration nếu có end_time
        if self.end_time and self.start_time:
            self.duration = (self.end_time - self.start_time).total_seconds() / 3600
            
        super().save(*args, **kwargs)
        
        # Cập nhật actual_time của TaskAssignment
        if self.task_assignment:
            self.task_assignment.update_actual_time()


class DeadlineExtensionRequest(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    task = models.ForeignKey("projects.Tasks", on_delete=models.CASCADE, related_name="deadline_requests")
    requested_by = models.ForeignKey("users.Users", on_delete=models.CASCADE, related_name="deadline_requests")
    requested_deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "deadline_extension_requests"
        verbose_name = "Deadline Request"
        verbose_name_plural = "Deadline Requests"
        indexes = [
            models.Index(fields=['task', 'status']),
            models.Index(fields=['requested_by', 'status']),
        ]

    def __str__(self):
        return f"Request for {self.task.title} by {self.requested_by.username}"


class TeamProjectMembership(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, default="Member")

    class Meta:
        db_table = "team_project_memberships"
        verbose_name = "Project Member"
        verbose_name_plural = "Project Members"
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.user.username} in {self.project.name}"