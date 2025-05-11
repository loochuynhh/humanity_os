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
    fixed_location = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/static/assets/img/default-avatar.png'


class UserFaceImage(models.Model):
    user = models.ForeignKey("users.Users", on_delete=models.CASCADE, related_name="face_images")
    face_image = models.ImageField(upload_to="face_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_face_images"

    def __str__(self):
        return f"Face image for {self.user.username}"


class CheckInCheckOut(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    date = models.DateField()
    checkin_time = models.DateTimeField(null=True, blank=True)
    checkout_time = models.DateTimeField(null=True, blank=True)
    checkin_image = models.ImageField(upload_to='checkin_images/', null=True, blank=True)
    checkout_image = models.ImageField(upload_to='checkout_images/', null=True, blank=True)
    checkin_location = models.CharField(max_length=100, null=True, blank=True)
    checkout_location = models.CharField(max_length=100, null=True, blank=True)
    is_valid_checkin = models.BooleanField(default=False)
    is_valid_checkout = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Check-in/Check-out"
        verbose_name_plural = "Check-in/Check-out"
        db_table = "checkin_checkout"
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='unique_checkin_checkout_per_day'),
        ]
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.date}"
