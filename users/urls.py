from django.urls import path
from .views import (
    login_view,
    logout_view,
    forgot_password,
    change_password,
    index,
    reset_password,
)

urlpatterns = [
    path("", index, name="index"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("change-password/", change_password, name="change_password"),
    path("reset-password/<uidb64>/<token>/", reset_password, name="reset_password"),
]
