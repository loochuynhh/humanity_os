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
from .models import Users, CheckInCheckOut, Goals
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import models
from projects.models import Tasks, Projects
from kpis.models import EmployeeKPIs
import json
from django.db.models import Count, Q
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
@login_required
def goals(request):
    """Hiển thị trang Goals"""
    goals = Goals.objects.filter(user=request.user)

    total_goals = goals.count()
    achieved_goals = goals.filter(status="Achieved").count()
    average_progress = goals.aggregate(models.Avg('achieved_percentage'))['achieved_percentage__avg'] or 0

    context = {
        'goals': goals,
        'total_goals': total_goals,
        'achieved_goals': achieved_goals,
        'average_progress': round(average_progress, 1),
        'today': timezone.now().date(),
    }
    return render(request, 'main/pages/users/goals.html', context)

@require_POST
@login_required
def add_goal(request):
    """Thêm mục tiêu mới"""
    try:
        Goals.objects.create(
            user=request.user,
            name=request.POST.get('goal_name'),
            description=request.POST.get('goal_description'),
            deadline=request.POST.get('goal_deadline'),
            priority=request.POST.get('goal_priority'),
            achieved_percentage=0,
            status="Pending"
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_POST
@login_required
def update_goal(request):
    """Cập nhật mục tiêu"""
    try:
        goal_id = request.POST.get('goal_id')
        goal = Goals.objects.get(id=goal_id, user=request.user)
        goal.name = request.POST.get('goal_name')
        goal.description = request.POST.get('goal_description')
        goal.deadline = request.POST.get('goal_deadline')
        goal.priority = request.POST.get('goal_priority')
        goal.achieved_percentage = float(request.POST.get('goal_achieved_percentage'))
        goal.status = request.POST.get('goal_status')
        goal.save()
        return JsonResponse({'success': True})
    except Goals.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Mục tiêu không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
@login_required
def profile(request):
    user = request.user

    # ----------- TASKS -----------------
    tasks = Tasks.objects.filter(task_assignments__user=user).distinct()
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()

    task_stats = {
        'total': total_tasks,
        'completed': completed_tasks,
        'completion_rate': round(completed_tasks / total_tasks * 100, 2) if total_tasks else 0
    }

    # ----------- KPI -------------------
    latest_kpi = EmployeeKPIs.objects.filter(user=user).order_by('-id').first()
    kpi_score = latest_kpi.actual_value if latest_kpi and latest_kpi.actual_value else "0"

    # ----------- GOALS -----------------
    goals = Goals.objects.filter(user=user)
    total_goals = goals.count()
    achieved_goals = goals.filter(status='Achieved').count()

    goals_stats = {
        'total': total_goals,
        'achieved': achieved_goals,
        'completion_rate': round(achieved_goals / total_goals * 100, 2) if total_goals else 0
    }

    # ----------- RECENT ACTIVITIES (TODO: real data later) ---------------
    recent_activities = [
        {
            'icon': 'check-circle',
            'color': 'success',
            'title': 'Hoàn thành task "Fix bug đăng nhập"',
            'description': 'Dự án HR Management',
            'time': '2 giờ trước'
        },
        # Bạn có thể thay bằng dữ liệu thật từ TaskAssignments, TimeEntries v.v.
    ]

    # ----------- PROJECTS & PROGRESS -----------------
    projects = Projects.objects.filter(team_members=user).distinct()
    project_data = []

    for project in projects:
        total_project_tasks = project.tasks.count()
        completed_project_tasks = project.tasks.filter(status='Completed').count()
        progress = round((completed_project_tasks / total_project_tasks * 100), 2) if total_project_tasks else 0

        project_data.append({
            'id': project.id,
            'name': project.name,
            'progress': progress
        })

    # ----------- CHART DATA (dummy) -------------------
    performance_labels = json.dumps(['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5'])
    performance_data = json.dumps([75, 82, 68, 90, 88])

    task_distribution_labels = json.dumps(['Hoàn thành', 'Đang làm', 'Quá hạn', 'Chưa bắt đầu'])
    task_distribution_data = json.dumps([
        completed_tasks,
        tasks.filter(status='In progress').count(),
        tasks.filter(status='Late').count(),
        tasks.filter(status='To-do').count()
    ])

    context = {
        'user': user,
        'task_stats': task_stats,
        'kpi_score': kpi_score,
        'goals': goals_stats,
        'skills': [
            {'name': 'Python', 'level': 85},
            {'name': 'Django', 'level': 90},
            {'name': 'JavaScript', 'level': 70},
        ],
        'recent_activities': recent_activities,
        'projects': project_data,
        'performance_labels': performance_labels,
        'performance_data': performance_data,
        'task_distribution_labels': task_distribution_labels,
        'task_distribution_data': task_distribution_data,
    }

    return render(request, 'main/pages/users/profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        try:
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.phone = request.POST.get('phone', user.phone)
            user.department = request.POST.get('department', user.department)

            date_of_joining = request.POST.get('date_of_joining')
            if date_of_joining:
                user.date_of_joining = date_of_joining

            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']

            user.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
