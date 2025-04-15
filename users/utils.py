# users/utils.py
from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
import json
from projects.models import Tasks, TaskAssignments, TimeEntries, Projects
from kpis.models import EmployeeKPIs
from users.models import Goals, Users, CheckInCheckOut
import base64
import io
from PIL import Image
from django.core.files.base import ContentFile


def get_task_counts(user_id, as_json=False):
    task_counts = TaskAssignments.objects.filter(user_id=user_id).values('task__status').annotate(count=Count('task__id'))
    task_status = {'To_do': 0, 'In_progress': 0, 'Completed': 0, 'Late': 0}
    for item in task_counts:
        status = item['task__status'].replace(' ', '_').replace('-', '_')
        if status in task_status:
            task_status[status] = item['count']
    return json.dumps(list(task_status.values())) if as_json else task_status


def get_time_tracking(user_id, period='today', as_json=False):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    if period == 'today':
        entries = TimeEntries.objects.filter(user_id=user_id, start_time__date=today)
    elif period == 'week':
        entries = TimeEntries.objects.filter(user_id=user_id, start_time__gte=week_start)
    total_hours = entries.filter(duration__isnull=False).aggregate(total=Sum('duration'))['total'] or 0
    if period == 'week' and as_json:
        week_data = []
        for i in range(7):
            day = week_start + timedelta(days=i)
            day_entries = entries.filter(start_time__date=day, duration__isnull=False)
            day_hours = day_entries.aggregate(total=Sum('duration'))['total'] or 0
            week_data.append(day_hours)
        return json.dumps(week_data)
    hours = int(total_hours)
    minutes = int((total_hours - hours) * 60)
    return f"{hours}h {minutes}m" if not as_json else json.dumps([total_hours])


def get_kpi_snapshot(user_id, metric='completion'):
    kpi = EmployeeKPIs.objects.filter(user_id=user_id, time_period='monthly').first()
    if not kpi or not kpi.target_value:
        return "0/0" if metric == 'completion' else 0
    try:
        actual = int(kpi.actual_value) if kpi.actual_value else 0
        target = int(kpi.target_value)
        completion = f"{actual}/{target}"
        percentage = (actual / target * 100) if target != 0 else 0
    except ValueError:
        completion = "0/0"
        percentage = 0
    return completion if metric == 'completion' else percentage


def get_kpi_score(user):
    latest_kpi = EmployeeKPIs.objects.filter(user=user).order_by('-id').first()
    return latest_kpi.actual_value if latest_kpi and latest_kpi.actual_value else "0"


def get_project_data(user):
    projects = Projects.objects.filter(team_members=user).distinct()
    project_data = []
    for project in projects:
        total_tasks = project.tasks.count() # type: ignore
        completed_tasks = project.tasks.filter(status='Completed').count() # type: ignore
        progress = round((completed_tasks / total_tasks * 100), 2) if total_tasks else 0
        project_data.append({
            'id': project.id, # type: ignore
            'name': project.name,
            'progress': progress
        })
    return project_data


def get_project_progress(user_id):
    return [
        {'name': project['name'], 'progress': project['progress']}
        for project in get_project_data(Users.objects.get(id=user_id))
    ]


def get_task_stats(user):
    tasks = Tasks.objects.filter(task_assignments__user=user).distinct()
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()
    return {
        'total': total_tasks,
        'completed': completed_tasks,
        'completion_rate': round(completed_tasks / total_tasks * 100, 2) if total_tasks else 0
    }


def get_goals_stats(user):
    goals = Goals.objects.filter(user=user)
    total_goals = goals.count()
    achieved_goals = goals.filter(status='Achieved').count()
    return {
        'total': total_goals,
        'achieved': achieved_goals,
        'completion_rate': round(achieved_goals / total_goals * 100, 2) if total_goals else 0
    }


def get_goals_summary(user):
    goals = Goals.objects.filter(user=user)
    total_goals = goals.count()
    achieved_goals = goals.filter(status='Achieved').count()
    average_progress = goals.aggregate(models.Avg('achieved_percentage'))['achieved_percentage__avg'] or 0
    return {
        'total_goals': total_goals,
        'achieved_goals': achieved_goals,
        'average_progress': round(average_progress, 1)
    }


def get_ai_suggestions(user_id):
    return Tasks.objects.filter(
        task_assignments__user_id=user_id,
        status__in=['To-do', 'In progress']
    ).values('title', 'difficulty', 'estimated_time')[:2]


def get_recent_tasks(user_id):
    return Tasks.objects.filter(task_assignments__user_id=user_id).select_related('project').order_by('-deadline')[:5]


def get_personal_goals(user_id):
    goals = Goals.objects.filter(user_id=user_id).order_by('-deadline')
    return [{
        'description': goal.description,
        'progress': goal.achieved_percentage,
        'name': goal.name,
        'deadline': goal.deadline,
        'status': goal.status
    } for goal in goals]


def get_chart_data(user):
    # Lấy dữ liệu hiệu suất theo tháng (12 tháng gần nhất)
    now = timezone.now()
    months = []
    performance_data = []
    
    for i in range(12):
        month = now - timedelta(days=30*i)
        months.insert(0, month.strftime("%b %Y"))
        
        # Tính hiệu suất theo tháng (có thể thay bằng logic tính KPI thực tế)
        start_date = month.replace(day=1)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # Tính toán hiệu suất dựa trên task hoàn thành
        completed_tasks = Tasks.objects.filter(
            task_assignments__user=user,
            status='Completed',
            deadline__range=(start_date, end_date)
        ).count()
        
        total_tasks = Tasks.objects.filter(
            task_assignments__user=user,
            deadline__range=(start_date, end_date)
        ).count()
        
        performance = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        performance_data.insert(0, round(performance, 2))
    
    # Lấy dữ liệu phân bổ công việc
    tasks = Tasks.objects.filter(task_assignments__user=user).distinct()
    task_distribution_data = [
        tasks.filter(status='Completed').count(),
        tasks.filter(status='In progress').count(),
        tasks.filter(status='Late').count(),
        tasks.filter(status='To-do').count()
    ]
    
    return {
        'performance_labels': json.dumps(months),
        'performance_data': json.dumps(performance_data),
        'task_distribution_labels': json.dumps(['Hoàn thành', 'Đang làm', 'Quá hạn', 'Chưa bắt đầu']),
        'task_distribution_data': json.dumps(task_distribution_data)
    }


def handle_check_in(user, location, image_data):
    """
    Xử lý logic check-in, lưu thông tin vào database.
    """
    today = timezone.now().date()
    existing_checkin = CheckInCheckOut.objects.filter(user=user, date=today).first()
    
    if existing_checkin:
        return False, "Bạn đã check-in hôm nay rồi."

    checkin = CheckInCheckOut(
        user=user,
        checkin_time=timezone.now(),
        date=today,
        checkin_location=location,
    )

    if image_data:
        try:
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            img_bytes = base64.b64decode(image_data)
            img = Image.open(io.BytesIO(img_bytes))
            img = img.resize((320, 240), LANCZOS) # type: ignore  # noqa: F821
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=70)
            img_name = f"checkin_{user.username}_{today}.jpg"
            checkin.checkin_image.save(img_name, ContentFile(buffer.getvalue()), save=False)
        except Exception as e:
            return False, f"Lỗi xử lý ảnh: {str(e)}"

    checkin.save()
    return True, "Check-in thành công."

def handle_check_out(user, location, image_data):
    """
    Xử lý logic check-out, cập nhật thông tin vào database.
    """
    today = timezone.now().date()
    checkin = CheckInCheckOut.objects.filter(user=user, date=today).first()
    
    if not checkin:
        return False, "Bạn chưa check-in hôm nay."
    if checkin.checkout_time:
        return False, "Bạn đã check-out hôm nay rồi."

    checkin.checkout_time = timezone.now()
    checkin.checkout_location = location

    if image_data:
        try:
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            img_bytes = base64.b64decode(image_data)
            img = Image.open(io.BytesIO(img_bytes))
            img = img.resize((320, 240), LANCZOS)  # type: ignore # noqa: F821
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=70)
            img_name = f"checkout_{user.username}_{today}.jpg"
            checkin.checkout_image.save(img_name, ContentFile(buffer.getvalue()), save=False)
        except Exception as e:
            return False, f"Lỗi xử lý ảnh: {str(e)}"

    checkin.save()
    return True, "Check-out thành công."

def get_today_work_hours(user):
    """
    Tính số giờ làm việc hôm nay.
    """
    today = timezone.now().date()
    checkin = CheckInCheckOut.objects.filter(user=user, date=today).first()
    if not checkin:
        return None
    if checkin.checkout_time:
        duration = checkin.checkout_time - checkin.checkin_time
    else:
        duration = timezone.now() - checkin.checkin_time
    hours = duration.total_seconds() / 3600
    return f"{hours:.2f} giờ"