from django.urls import path
from .views import login_view, logout_view, forgot_password, change_password

urlpatterns = [
    path("", views.user_list, name="user_list"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("change-password/", change_password, name="change_password"),
]
