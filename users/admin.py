from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, UserFaceImage, CheckInCheckOut
from django.utils.html import format_html

class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone",
        "department",
        "role",
        "status",
        "fixed_location",
        "date_of_joining",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "department", "role", "status")
    search_fields = ("username", "email", "first_name", "last_name", "phone", "department")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "avatar",
                    "phone",
                    "department",
                    "role",
                    "status",
                    "date_of_joining",
                    "fixed_location",
                    "bio",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "phone",
                    "department",
                    "role",
                    "status",
                    "date_of_joining",
                    "fixed_location",
                    "bio",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )
    def avatar_preview(self, obj):
            if obj.avatar:
                return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar_url)
            return "No avatar"

    avatar_preview.short_description = "Avatar"

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
            fixed_location_parts = user.fixed_location.split(',')
            checkin_location_parts = obj.checkin_location.split(',')

            if len(fixed_location_parts) != 2 or len(checkin_location_parts) != 2:
                return format_html('<span class="text-danger">Định dạng không hợp lệ</span>')

            fixed_lat = float(fixed_location_parts[0].strip())
            fixed_lng = float(fixed_location_parts[1].strip())

            current_lat = float(checkin_location_parts[0].strip())
            current_lng = float(checkin_location_parts[1].strip())

            from math import sin, cos, sqrt, atan2, radians
            R = 6371  

            lat1, lng1 = radians(fixed_lat), radians(fixed_lng)
            lat2, lng2 = radians(current_lat), radians(current_lng)

            dlat = lat2 - lat1
            dlng = lng2 - lng1

            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c

            if distance <= 0.5:
                distance_str = "{:.2f}".format(distance)
                return format_html('<span class="text-success">Hợp lệ ({} km)</span>', distance_str)
            else:
                distance_str = "{:.2f}".format(distance)
                return format_html('<span class="text-danger">Không hợp lệ ({} km)</span>', distance_str)
        except Exception as e:
            return format_html('<span class="text-danger">Lỗi định dạng: {}</span>', str(e))

    checkin_location_status.short_description = 'Vị trí check-in'

    def checkout_location_status(self, obj):
        if not obj.checkout_location:
            return format_html('<span class="text-muted">Chưa check-out</span>')

        user = obj.user
        if not user.fixed_location:
            return format_html('<span class="text-warning">Chưa đăng ký vị trí cố định</span>')

        try:
            fixed_location_parts = user.fixed_location.split(',')
            checkout_location_parts = obj.checkout_location.split(',')

            if len(fixed_location_parts) != 2 or len(checkout_location_parts) != 2:
                return format_html('<span class="text-danger">Định dạng không hợp lệ</span>')

            fixed_lat = float(fixed_location_parts[0].strip())
            fixed_lng = float(fixed_location_parts[1].strip())

            current_lat = float(checkout_location_parts[0].strip())
            current_lng = float(checkout_location_parts[1].strip())

            from math import sin, cos, sqrt, atan2, radians
            R = 6371 

            lat1, lng1 = radians(fixed_lat), radians(fixed_lng)
            lat2, lng2 = radians(current_lat), radians(current_lng)

            dlat = lat2 - lat1
            dlng = lng2 - lng1

            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c

            if distance <= 0.5:
                distance_str = "{:.2f}".format(distance)
                return format_html('<span class="text-success">Hợp lệ ({} km)</span>', distance_str)
            else:
                distance_str = "{:.2f}".format(distance)
                return format_html('<span class="text-danger">Không hợp lệ ({} km)</span>', distance_str)
        except Exception as e:
            return format_html('<span class="text-danger">Lỗi định dạng: {}</span>', str(e))

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

    def has_add_permission(self, request):
        return False
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [f.name for f in obj._meta.fields if f.name not in ['is_valid_checkin', 'is_valid_checkout']]
        return []

class AIChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'content_preview', 'timestamp')
    list_filter = ('role', 'timestamp', 'user__department')
    search_fields = ('user__username', 'user__email', 'content')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)

    def content_preview(self, obj):
        """Hiển thị bản xem trước nội dung tin nhắn, giới hạn 50 ký tự."""
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')

    content_preview.short_description = 'Nội dung'

    def get_readonly_fields(self, request, obj=None):
        """Đặt các trường chỉ đọc để tránh chỉnh sửa trực tiếp."""
        return ('user', 'role', 'content', 'timestamp')
    
    def has_add_permission(self, request):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
        
    def has_view_permission(self, request, obj=None):
        return False
    
admin.site.register(Users, CustomUserAdmin)
admin.site.register(UserFaceImage, UserFaceImageAdmin)
admin.site.register(CheckInCheckOut, CheckInCheckOutAdmin)
# admin.site.register(AIChatMessage, AIChatMessageAdmin)
