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

    class Meta:
        db_table = "projects"

    def __str__(self):
        return self.name


class Tasks(models.Model):
    project = models.ForeignKey("projects.Projects", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("To-do", "To-do"),
            ("In progress", "In progress"),
            ("Completed", "Completed"),
            ("Late", "Late"),
        ],
        default="To-do",
    )
    difficulty = models.CharField(max_length=20, null=True, blank=True)
    estimated_time = models.FloatField(null=True, blank=True)
    github_link = models.URLField(null=True, blank=True)

    class Meta:
        db_table = "tasks"

    def __str__(self):
        return self.title


class TaskAssignments(models.Model):
    task = models.ForeignKey("projects.Tasks", on_delete=models.CASCADE)
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE)

    class Meta:
        db_table = "task_assignments"

    def __str__(self):
        return f"{self.task.title} - {self.user.username}"


class TimeEntries(models.Model):
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE)
    task = models.ForeignKey("projects.Tasks", on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "time_entries"

    def __str__(self):
        return f"{self.user.username} - {self.task.title} ({self.start_time})"
