from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.conf import settings
from .models import Users
import traceback


def user_list(request):
    return HttpResponse("Danh sách người dùng.")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = Users.objects.get(email=email)
            if check_password(password, user.password):
                auth.login(request, user)
                messages.success(request, "Đăng nhập thành công!")
                return redirect(request.GET.get("next", "home"))
            else:
                messages.error(request, "Mật khẩu không chính xác!")
        except Users.DoesNotExist:
            messages.error(request, "Email không tồn tại!")

    return render(request, "users/login.html")


@login_required(login_url="login")
def logout_view(request):
    auth.logout(request)
    messages.success(request, "Bạn đã đăng xuất!")
    return redirect("login")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = Users.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse("reset_password", kwargs={"uidb64": uid, "token": token})
            )

            send_mail(
                subject="Đặt lại mật khẩu của bạn",
                message=f"Nhấp vào liên kết sau để đặt lại mật khẩu: {reset_url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(
                request, "Liên kết đặt lại mật khẩu đã được gửi vào email của bạn."
            )
        except Users.DoesNotExist:
            messages.error(request, "Email không tồn tại!")
        except Exception as e:
            messages.error(request, "Có lỗi xảy ra! Vui lòng thử lại sau.")
            print(traceback.format_exc())

    return render(request, "users/forgot_password.html")


@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        try:
            user = request.user
            if not check_password(current_password, user.password):
                messages.error(request, "Mật khẩu hiện tại không chính xác!")
            elif new_password != confirm_password:
                messages.error(request, "Mật khẩu mới không khớp!")
            else:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, "Mật khẩu đã được thay đổi thành công!")
                return redirect("home")
        except Exception as e:
            messages.error(request, "Đã xảy ra lỗi. Vui lòng thử lại!")
            print(traceback.format_exc())

    return render(request, "users/change_password.html")
