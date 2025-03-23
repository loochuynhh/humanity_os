from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.conf import settings
from .models import Users


def admin_required(view_func):
    @login_required(login_url="login")
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return HttpResponseForbidden("Bạn không có quyền truy cập.")
        return view_func(request, *args, **kwargs)

    return wrapper


@admin_required
def user_list(request):
    users = Users.objects.all()
    return render(request, "users/user_list.html", {"users": users})


@login_required(login_url="login")
def index(request):
    return render(request, "users/index.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Đăng nhập thành công!")
            return redirect("users:index")
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")
    return render(request, "users/login.html")


@login_required(login_url="login")
def logout_view(request):
    logout(request)
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
                reverse("users:reset_password", kwargs={"uidb64": uid, "token": token})
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
            messages.error(request, "Có lỗi xảy ra! Vui lòng thử lại sau")

    return render(request, "users/forgot_password.html")


@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        user = request.user
        if not user.check_password(current_password):
            messages.error(request, "Mật khẩu hiện tại không chính xác!")
        elif new_password != confirm_password:
            messages.error(request, "Mật khẩu mới không khớp!")
        else:
            user.set_password(new_password)
            user.save()
            logout(request)
            messages.success(
                request, "Mật khẩu đã được thay đổi. Vui lòng đăng nhập lại!"
            )
            return redirect("login")
    return render(request, "users/change_password.html")


def reset_password(request, uidb64, token):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Users.objects.get(pk=uid)
            if PasswordResetTokenGenerator().check_token(user, token):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Mật khẩu đã được đặt lại!")
                    return redirect("login")
                else:
                    messages.error(request, "Mật khẩu không khớp!")
            else:
                messages.error(request, "Liên kết không hợp lệ!")
        except (Users.DoesNotExist, ValueError):
            messages.error(request, "Liên kết không hợp lệ!")
    return render(request, "users/reset_password.html")


@admin_required
def create_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if Users.objects.filter(username=username).exists():
            messages.error(request, "Tên đăng nhập đã tồn tại!")
        elif Users.objects.filter(email=email).exists():
            messages.error(request, "Email đã tồn tại!")
        else:
            user = Users(username=username, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, "Tài khoản đã được tạo!")
            return redirect("user_list")
    return render(request, "users/create_user.html")
