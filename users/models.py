from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=50,
        choices=[("Employee", "Employee"), ("Manager", "Manager"), ("Admin", "Admin")],
        default="Employee",
    )
    department = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Active",
    )
    date_of_joining = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username
    
    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/static/assets/img/default-avatar.png'

    
class CheckInCheckOut(models.Model):
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE)
    checkin_time = models.DateTimeField()
    checkout_time = models.DateTimeField(null=True, blank=True)
    checkin_image = models.ImageField(upload_to="checkin_images/", null=True, blank=True)
    checkout_image = models.ImageField(upload_to="checkout_images/", null=True, blank=True)
    date = models.DateField()

    class Meta:
        db_table = "checkin_checkout"
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Goals(models.Model):
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE, related_name="goals")
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[("Pending", "Pending"), ("Achieved", "Achieved"), ("Missed", "Missed")],
        default="Pending"
    )
    priority = models.CharField(
        max_length=10,
        choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")],
        default="Medium"
    )
    achieved_percentage = models.FloatField(default=0.0)

    class Meta:
        db_table = "goals"

    def __str__(self):
        return f"{self.name} - {self.user.username}"