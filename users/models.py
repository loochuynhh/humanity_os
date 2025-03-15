from django.db import models

class Users(models.Model):
  user_id = models.AutoField(primary_key=True)
  user_name = models.CharField(max_length=150, unique=True)
  password = models.CharField(max_length=128)
  role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('employee', 'Employee')])
  email = models.EmailField(unique=True)
  company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)

  class Meta:
    db_table = 'users'

  def __str__(self):
    return self.username
class EmployeeKPIs(models.Model):
  employee_kpi_id = models.AutoField(primary_key=True)
  user = models.ForeignKey('users.Users', on_delete=models.CASCADE)
  kpi = models.ForeignKey('kpis.KPIs', on_delete=models.CASCADE)
  target_value = models.CharField(max_length=50)
  actual_value = models.CharField(max_length=50, null=True, blank=True)
  period = models.CharField(max_length=20)

  class Meta:
    db_table = 'employee_kpis'

  def __str__(self):
    return f"{self.user.username} - {self.kpi.name} ({self.period})"


class PersonalGoals(models.Model):
  goal_id = models.AutoField(primary_key=True)
  user = models.ForeignKey('users.Users', on_delete=models.CASCADE)
  goal_description = models.TextField()
  target_date = models.DateField()
  status = models.CharField(
    max_length=10,
    choices=[('pending', 'Pending'), ('achieved', 'Achieved'), ('missed', 'Missed')],
    default='pending'
  )

  class Meta:
    db_table = 'personal_goals'

  def __str__(self):
    return f"{self.user.username} - {self.goal_description[:50]}"