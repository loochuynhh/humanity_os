from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username


class EmployeeKPIs(models.Model):
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE)
    kpi = models.ForeignKey("kpis.KPIs", on_delete=models.CASCADE)
    target_value = models.CharField(max_length=50)
    actual_value = models.CharField(max_length=50, null=True, blank=True)
    period = models.CharField(max_length=20)

    class Meta:
        db_table = "employee_kpis"

    def __str__(self):
        return f"{self.user.username} - {self.kpi.name} ({self.period})"


class PersonalGoals(models.Model):
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE)
    goal_description = models.TextField()
    target_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", "Pending"),
            ("achieved", "Achieved"),
            ("missed", "Missed"),
        ],
        default="pending",
    )

    class Meta:
        db_table = "personal_goals"

    def __str__(self):
        return f"{self.user.username} - {self.goal_description[:50]}"
