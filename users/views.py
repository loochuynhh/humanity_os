from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from .models import Users, CheckInCheckOut
from .utils import (
    get_task_counts, get_time_tracking, get_kpi_snapshot, 
    get_project_progress, get_ai_suggestions, get_recent_tasks, get_personal_goals
)

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
    return render(request, "main/pages/users/list.html", {"users": users})


@login_required(login_url="login")
def index(request):
    user = request.user
    
    context = {
        'user': user,
        'task_counts': get_task_counts(user.id),
        'task_chart_data': get_task_counts(user.id, as_json=True),
        'today_time': get_time_tracking(user.id, period='today'),
        'week_time': get_time_tracking(user.id, period='week'),
        'week_chart_data': get_time_tracking(user.id, period='week', as_json=True),
        'kpi_completion': get_kpi_snapshot(user.id, 'completion'),
        'kpi_percentage': get_kpi_snapshot(user.id, 'percentage'),
        'project_progress': get_project_progress(user.id),
        'suggestions': get_ai_suggestions(user.id),
        'recent_tasks': get_recent_tasks(user.id),
        'personal_goals': get_personal_goals(user.id),
    }
    
    return render(request, 'main/pages/index.html', context)


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
    return render(request, "main/pages/users/login.html")


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    messages.success(request, "Bạn đã đăng xuất!")
    return redirect("home")


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

    return render(request, "main/pages/users/forgot_password.html")


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
    return render(request, "main/pages/users/change_password.html")


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
    return render(request, "main/pages/users/reset_password.html")


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

@login_required
def check_in(request):
    if request.method == "POST":
        try:
            CheckInCheckOut.objects.create(
                user=request.user,
                checkin_time=timezone.now(),
                date=timezone.now().date(),
                # Có thể thêm checkin_image nếu cần
            )
            messages.success(request, "Check-in thành công!")
            return redirect('users:index')
        except Exception as e:
            messages.error(request, f"Có lỗi xảy ra: {str(e)}")
    return redirect('users:index')

@login_required
def check_out(request):
    if request.method == "POST":
        try:
            checkin = CheckInCheckOut.objects.filter(
                user=request.user,
                date=timezone.now().date(),
                checkout_time__isnull=True
            ).latest('checkin_time')
            
            checkin.checkout_time = timezone.now()
            checkin.save()
            messages.success(request, "Check-out thành công!")
            return redirect('users:index')
        except CheckInCheckOut.DoesNotExist:
            messages.error(request, "Bạn chưa check-in hôm nay!")
        except Exception as e:
            messages.error(request, f"Có lỗi xảy ra: {str(e)}")
    return redirect('users:index')

def set_goal(request):
    if request.method == "POST":
        return render(request, 'users/action_success.html', {'message': 'Đặt mục tiêu thành công!'})
    return redirect('users:index')