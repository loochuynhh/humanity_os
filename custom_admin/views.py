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


# Authentication
class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def get_success_url(self):
        return "/admin/dashboard/"


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully!")
            return redirect("/accounts/login/")
        else:
            print("Register failed!")
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "accounts/register.html", context)


def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = UserPasswordChangeForm
