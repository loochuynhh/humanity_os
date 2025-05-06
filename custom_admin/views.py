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
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from custom_admin.utils import superuser_required
from django.contrib import messages


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


@login_required
@require_POST
def update_fixed_location(request):
    """
    Cập nhật vị trí cố định của người dùng.
    """
    try:
        fixed_location = request.POST.get('fixed_location', '')

        # Kiểm tra định dạng
        if fixed_location:
            try:
                lat, lng = map(float, fixed_location.split(','))
                if not (-90 <= lat <= 90 and -180 <= lng <= 180):
                    messages.error(request, "Vị trí không hợp lệ. Vui lòng kiểm tra lại.")
                    return redirect('profile')
            except:
                messages.error(request, "Định dạng vị trí không hợp lệ. Vui lòng sử dụng định dạng: latitude,longitude")
                return redirect('profile')

        # Cập nhật vị trí
        user = request.user
        user.fixed_location = fixed_location
        user.save()

        messages.success(request, "Cập nhật vị trí làm việc thành công.")
        return redirect('profile')
    except Exception as e:
        messages.error(request, f"Lỗi khi cập nhật vị trí: {str(e)}")
        return redirect('profile')

