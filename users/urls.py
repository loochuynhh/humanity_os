from django.urls import path
from .views import (
    login_view,
    logout_view,
    forgot_password,
    change_password,
    index,
    reset_password,
    check_in,
    check_out,
    profile,
    update_profile,
    upload_face_image,
    update_fixed_location,
    attendance,
    get_current_work_time,
    generate_user_report
)

urlpatterns = [
    path("", index, name="index"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("change-password/", change_password, name="change_password"),
    path("reset-password/<uidb64>/<token>/", reset_password, name="reset_password"),
    path("check-in/", check_in, name="check_in"),
    path("check-out/", check_out, name="check_out"),
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('attendance/', attendance, name='attendance'),
    path('profile/upload-face-image/', upload_face_image, name='upload_face_image'),
    path('update-fixed-location/', update_fixed_location, name='update_fixed_location'),
    path('api/current-work-time/', get_current_work_time, name='get_current_work_time'),
    path('report/', generate_user_report, name='generate_user_report'),
]
