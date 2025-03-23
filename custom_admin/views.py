from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordChangeView,
    PasswordResetConfirmView,
)
from custom_admin.forms import (
    RegistrationForm,
    LoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm,
)
from django.contrib.auth import logout
from custom_admin.utils import superuser_required


@superuser_required
def index(request):
    return render(request, "pages/index.html", {"segment": "dashboard"})


@superuser_required
def billing(request):
    return render(request, "pages/billing.html", {"segment": "billing"})


@superuser_required
def tables(request):
    return render(request, "pages/tables.html", {"segment": "tables"})


@superuser_required
def vr(request):
    return render(request, "pages/virtual-reality.html", {"segment": "virtual_reality"})


@superuser_required
def rtl(request):
    return render(request, "pages/rtl.html", {"segment": "rtl"})


@superuser_required
def profile(request):
    return render(request, "pages/profile.html", {"segment": "profile"})


# Authenticatio
def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")
