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
    set_goal,
    goals,
    add_goal,
    update_goal,
    profile,
    update_profile
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
    path("set-goal/", set_goal, name="set_goal"),
    path("goals/", goals, name="goals"),
    path("goals/add/", add_goal, name="add_goal"),
    path("goals/update/", update_goal, name="update_goal"),
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
]
