from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, EmployeeKPIs, PersonalGoals


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "phone", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("username", "email", "phone")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email", "avatar", "phone")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(Users, CustomUserAdmin)
admin.site.register(EmployeeKPIs)
admin.site.register(PersonalGoals)
