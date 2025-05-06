from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, UserFaceImage, CheckInCheckOut
from django.utils.html import format_html


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "phone", "department", "fixed_location", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "department")
    search_fields = ("username", "email", "phone")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email", "avatar", "phone", "department", "fixed_location")}),
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
                    "department",
                    "fixed_location",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


class UserFaceImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('user__username', 'user__email')


class CheckInCheckOutAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'checkin_time', 'checkout_time', 'checkin_location_status',
                   'checkout_location_status', 'face_verification_status', 'view_checkin_image', 'view_checkout_image')
    list_filter = ('date', 'is_valid_checkin', 'is_valid_checkout', 'user__department')
    search_fields = ('user__username', 'user__email', 'checkin_location', 'checkout_location')
    date_hierarchy = 'date'

    def checkin_location_status(self, obj):
        if not obj.checkin_location:
            return format_html('<span class="text-muted">Không có</span>')

        user = obj.user
        if not user.fixed_location:
            return format_html('<span class="text-warning">Chưa đăng ký vị trí cố định</span>')

        try:
            # Phân tích vị trí
            fixed_lat, fixed_lng = map(float, user.fixed_location.split(','))
            current_lat, current_lng = map(float, obj.checkin_location.split(','))

            # Tính khoảng cách
            from math import sin, cos, sqrt, atan2, radians
            R = 6371  # Bán kính trái đất (km)

            lat1, lng1 = radians(fixed_lat), radians(fixed_lng)
            lat2, lng2 = radians(current_lat), radians(current_lng)

            dlat = lat2 - lat1
            dlng = lng2 - lng1

            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c

            if distance <= 0.5:
                return format_html('<span class="text-success">Hợp lệ ({:.2f} km)</span>', distance)
            else:
                return format_html('<span class="text-danger">Không hợp lệ ({:.2f} km)</span>', distance)
        except:
            return format_html('<span class="text-danger">Lỗi định dạng</span>')

    checkin_location_status.short_description = 'Vị trí check-in'

    def checkout_location_status(self, obj):
        if not obj.checkout_location:
            return format_html('<span class="text-muted">Chưa check-out</span>')

        user = obj.user
        if not user.fixed_location:
            return format_html('<span class="text-warning">Chưa đăng ký vị trí cố định</span>')

        try:
            # Phân tích vị trí
            fixed_lat, fixed_lng = map(float, user.fixed_location.split(','))
            current_lat, current_lng = map(float, obj.checkout_location.split(','))

            # Tính khoảng cách
            from math import sin, cos, sqrt, atan2, radians
            R = 6371  # Bán kính trái đất (km)

            lat1, lng1 = radians(fixed_lat), radians(fixed_lng)
            lat2, lng2 = radians(current_lat), radians(current_lng)

            dlat = lat2 - lat1
            dlng = lng2 - lng1

            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c

            if distance <= 0.5:
                return format_html('<span class="text-success">Hợp lệ ({:.2f} km)</span>', distance)
            else:
                return format_html('<span class="text-danger">Không hợp lệ ({:.2f} km)</span>', distance)
        except:
            return format_html('<span class="text-danger">Lỗi định dạng</span>')

    checkout_location_status.short_description = 'Vị trí check-out'

    def face_verification_status(self, obj):
        checkin_status = "Chưa check-in" if not obj.checkin_image else "Hợp lệ" if obj.is_valid_checkin else "Không hợp lệ"
        checkout_status = "Chưa check-out" if not obj.checkout_image else "Hợp lệ" if obj.is_valid_checkout else "Không hợp lệ"

        if checkin_status == "Hợp lệ" and (checkout_status == "Hợp lệ" or checkout_status == "Chưa check-out"):
            return format_html('<span class="text-success">✓</span>')
        elif checkin_status == "Không hợp lệ" or (checkout_status != "Chưa check-out" and checkout_status == "Không hợp lệ"):
            return format_html('<span class="text-danger">✗</span>')
        else:
            return format_html('<span class="text-warning">?</span>')

    face_verification_status.short_description = 'Xác minh khuôn mặt'

    def view_checkin_image(self, obj):
        if obj.checkin_image:
            return format_html('<a href="{}" target="_blank">Xem ảnh</a>', obj.checkin_image.url)
        return "Không có ảnh"

    view_checkin_image.short_description = 'Ảnh check-in'

    def view_checkout_image(self, obj):
        if obj.checkout_image:
            return format_html('<a href="{}" target="_blank">Xem ảnh</a>', obj.checkout_image.url)
        return "Không có ảnh"

    view_checkout_image.short_description = 'Ảnh check-out'


admin.site.register(Users, CustomUserAdmin)
admin.site.register(UserFaceImage, UserFaceImageAdmin)
admin.site.register(CheckInCheckOut, CheckInCheckOutAdmin)
