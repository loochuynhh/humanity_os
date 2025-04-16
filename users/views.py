# users/views.py
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.http import require_POST
from .models import Goals, Users
from .utils import (
    get_task_counts,
    get_time_tracking,
    get_kpi_snapshot,
    get_project_progress,
    get_recent_tasks,
    get_personal_goals,
    get_project_time_allocation,
    get_goals_progress,
    handle_check_in,
    handle_check_out,
    get_goals_summary,
    get_task_stats,
    get_goals_stats,
    get_project_data,
)


def admin_required(view_func):
    @login_required(login_url="login")
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return HttpResponseForbidden("Bạn không có quyền truy cập.")
        return view_func(request, *args, **kwargs)
    return wrapper


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
def user_list(request):
    users = Users.objects.all()
    return render(request, "main/pages/users/list.html", {"users": users})


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
@require_POST
def check_in(request):
    """
    Xử lý check-in của người dùng, lưu thời gian, địa điểm và hình ảnh.
    """
    location = request.POST.get('checkin_location')
    image_data = request.POST.get('checkin_image')

    success, message = handle_check_in(request.user, location, image_data)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect('users:index')


@login_required
@require_POST
def check_out(request):
    """
    Xử lý check-out của người dùng, lưu thời gian, địa điểm và hình ảnh.
    """
    location = request.POST.get('checkout_location')
    image_data = request.POST.get('checkout_image')

    success, message = handle_check_out(request.user, location, image_data)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect('users:index')

@login_required
def index(request):
    user = request.user
    context = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "avatar_url": user.avatar_url,  
        "task_counts": get_task_counts(user.id),
        "task_chart_data": get_task_counts(user.id, as_json=True),
        "today_time": get_time_tracking(user.id, period="today"),
        "week_time": get_time_tracking(user.id, period="week"),
        "week_chart_data": get_time_tracking(user.id, period="week", as_json=True),
        "kpi_completion": get_kpi_snapshot(user.id, "completion"),
        "kpi_percentage": round(float(get_kpi_snapshot(user.id, "percentage")), 2),
        "project_progress": get_project_progress(user.id),
        "recent_tasks": get_recent_tasks(user.id),
        "personal_goals": get_personal_goals(user.id),
        "project_time_allocation": get_project_time_allocation(user.id, as_json=True),
        "goals_progress": get_goals_progress(user.id, as_json=True),
    }
    return render(request, "main/pages/index.html", context)


def set_goal(request):
    if request.method == "POST":
        return render(request, "users/action_success.html", {"message": "Đặt mục tiêu thành công!"})
    return redirect("users:index")


@login_required
def goals(request):
    goals = Goals.objects.filter(user=request.user)
    context = {
        "goals": goals,
        **get_goals_summary(request.user),
        "today": timezone.now().date(),
    }
    return render(request, "main/pages/users/goals.html", context)


@require_POST
@login_required
def add_goal(request):
    try:
        Goals.objects.create(
            user=request.user,
            name=request.POST.get("goal_name"),
            description=request.POST.get("goal_description"),
            deadline=request.POST.get("goal_deadline"),
            priority=request.POST.get("goal_priority"),
            achieved_percentage=0,
            status="Pending",
        )
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@require_POST
@login_required
def update_goal(request):
    try:
        goal_id = request.POST.get("goal_id")
        goal = Goals.objects.get(id=goal_id, user=request.user)
        goal.name = request.POST.get("goal_name")
        goal.description = request.POST.get("goal_description")
        goal.deadline = request.POST.get("goal_deadline")
        goal.priority = request.POST.get("goal_priority")
        goal.achieved_percentage = float(request.POST.get("goal_achieved_percentage"))
        goal.status = request.POST.get("goal_status")
        goal.save()
        return JsonResponse({"success": True})
    except Goals.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Mục tiêu không tồn tại"}, status=404
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@login_required
def profile(request):
    user = request.user
    context = {
        "user": user,
        "task_stats": get_task_stats(user),
        "goals": get_goals_stats(user),
        "projects": get_project_data(user),
        "time_tracking": get_time_tracking(user.id),
        "recent_tasks": get_recent_tasks(user.id),
        "personal_goals": get_personal_goals(user.id),
    }
    return render(request, "main/pages/users/profile.html", context)


@login_required
def update_profile(request):
    if request.method == "POST":
        user = request.user
        try:
            user.first_name = request.POST.get("first_name", user.first_name)
            user.last_name = request.POST.get("last_name", user.last_name)
            user.phone = request.POST.get("phone", user.phone)
            user.department = request.POST.get("department", user.department)
            user.bio = request.POST.get("bio", user.bio) 
            date_of_joining = request.POST.get("date_of_joining")
            if date_of_joining:
                user.date_of_joining = date_of_joining
            if "avatar" in request.FILES:
                user.avatar = request.FILES["avatar"]
            user.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})