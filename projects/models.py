# projects/models.py
from django.db import models


class Projects(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
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

    def __str__(self):
        return self.name


class Tasks(models.Model):
    STATUS_CHOICES = [
        ("To-do", "To-do"),
        ("In progress", "In progress"),
        ("Completed", "Completed"),
        ("Late", "Late"),
    ]
    
    project = models.ForeignKey("projects.Projects", on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="To-do")
    difficulty = models.CharField(max_length=20, null=True, blank=True)
    estimated_time = models.FloatField(null=True, blank=True)
    github_link = models.URLField(null=True, blank=True)
    total_time = models.FloatField(default=0.0)  # Thêm trường mới
    is_tracking = models.BooleanField(default=False)  # Thêm trường mới

    class Meta:
        db_table = "tasks"
        indexes = [
            models.Index(fields=['deadline']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title


class TaskAssignments(models.Model):
    task = models.ForeignKey("projects.Tasks", on_delete=models.CASCADE, related_name="task_assignments")
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE, related_name="task_assignments")

    class Meta:
        db_table = "task_assignments"
        unique_together = ("task", "user")

    def __str__(self):
        return f"{self.task.title} - {self.user.username}"


class TimeEntries(models.Model):
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE, related_name="time_entries")
    task = models.ForeignKey("projects.Tasks", on_delete=models.CASCADE, related_name="time_entries")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)  

    class Meta:
        db_table = "time_entries"

    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            self.duration = (self.end_time - self.start_time).total_seconds() / 3600
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.task.title} ({self.start_time})"


class TeamProjectMembership(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE)
    join_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "team_project_memberships"
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.user.username} in {self.project.name}"