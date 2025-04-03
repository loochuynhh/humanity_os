from django.db import models


class KPIs(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = "kpis"

    def __str__(self):
        return self.name


class EmployeeKPIs(models.Model):
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE)
    kpi = models.ForeignKey("kpis.KPIs", on_delete=models.CASCADE)
    target_value = models.CharField(max_length=50)
    actual_value = models.CharField(max_length=50, null=True, blank=True)
    unit = models.CharField(max_length=20, null=True, blank=True) 
    time_period = models.CharField(max_length=20) 
    evaluation = models.CharField(
        max_length=20,
        choices=[("Achieved", "Achieved"), ("Not Achieved", "Not Achieved")],
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "employee_kpis"

    def __str__(self):
        return f"{self.user.username} - {self.kpi.name} ({self.time_period})"