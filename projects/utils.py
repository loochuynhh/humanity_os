# projects/utils.py
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Tasks, Projects, TimeEntries, TeamProjectMembership


def filter_tasks(tasks, project_id=None, status=None):
    if project_id:
        tasks = tasks.filter(project_id=project_id)
    if status:
        tasks = tasks.filter(status=status)
    return tasks


def get_user_projects(user):
    managed_projects = Projects.objects.filter(manager=user)
    member_projects = Projects.objects.filter(
        id__in=TeamProjectMembership.objects.filter(user=user).values('project_id')
    )
    return (managed_projects | member_projects).distinct()


def update_task_tracking(task, user):
    task.is_tracking = TimeEntries.objects.filter(
        task=task,
        user=user,
        end_time__isnull=True
    ).exists()
    task.update_total_time()
    task.update_start_date()
    task.save()


def update_task_status(task, status):
    task.status = status
    if task.deadline.date() < timezone.now().date() and status != 'Completed' and not task.completed_date:
        task.status = 'Late'
    task.save()


def calculate_time_totals(user):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    # Chuyển đổi sang offset-aware DateTime
    today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    week_start_dt = timezone.make_aware(timezone.datetime.combine(week_start, timezone.datetime.min.time()))
    month_start_dt = timezone.make_aware(timezone.datetime.combine(month_start, timezone.datetime.min.time()))

    total_time_today = TimeEntries.objects.filter(
        user=user,
        start_time__gte=today_start,
        start_time__lt=today_start + timedelta(days=1)
    ).aggregate(total=Sum('duration'))['total'] or 0
    total_time_week = TimeEntries.objects.filter(
        user=user,
        start_time__gte=week_start_dt
    ).aggregate(total=Sum('duration'))['total'] or 0
    total_time_month = TimeEntries.objects.filter(
        user=user,
        start_time__gte=month_start_dt
    ).aggregate(total=Sum('duration'))['total'] or 0

    def format_time(hours):
        if hours is None:
            return "0h 0m"
        h = int(hours)
        m = int((hours - h) * 60)
        return f"{h}h {m}m"

    return {
        'today': format_time(total_time_today),
        'week': format_time(total_time_week),
        'month': format_time(total_time_month)
    }


def get_project_progress(project):
    tasks = Tasks.objects.filter(project=project)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()
    return (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0


def calculate_team_member_data(project_id):
    members_data = []
    try:
        project = Projects.objects.get(id=project_id)
        memberships = TeamProjectMembership.objects.filter(project=project).select_related('user')
        for membership in memberships:
            user = membership.user
            task_count = Tasks.objects.filter(task_assignments__user=user, project=project).count()
            total_time = TimeEntries.objects.filter(user=user, task__project=project).aggregate(
                total=Sum('duration')
            )['total'] or 0
            total_time_str = f"{int(total_time)}h {int((total_time % 1) * 60)}m"
            members_data.append({
                'name': user.get_full_name(),
                'role': 'Quản lý' if user == project.manager else 'Thành viên',
                'join_date': membership.join_date.strftime('%d/%m/%Y'),
                'task_count': task_count,
                'total_time': total_time_str,
            })
    except Exception as e:
        print(f"Error in calculate_team_member_data: {str(e)}")
    return members_data


def calculate_project_progress_data(project_id):
    project = Projects.objects.get(id=project_id)
    tasks = Tasks.objects.filter(project=project)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()
    task_counts = dict(tasks.values('status').annotate(count=Count('status')).values_list('status', 'count'))
    progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'progress': round(progress, 1),
        'task_counts': task_counts
    }


def get_project_progress_data(project_id):
    """
    Lấy dữ liệu tiến độ chi tiết của dự án.
    """
    try:
        project = Projects.objects.get(id=project_id)
        today = timezone.now().date()

        # Lấy thông tin cơ bản về tasks
        tasks = Tasks.objects.filter(project=project)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='Completed').count()
        task_counts = dict(tasks.values('status').annotate(count=Count('status')).values_list('status', 'count'))
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Xác định trạng thái dự án
        status = 'In progress'
        if completed_tasks == total_tasks and total_tasks > 0:
            status = 'Completed'
        elif project.end_date.date() < today:
            status = 'Late'

        # Tính toán thời gian còn lại
        days_left = (project.end_date.date() - today).days if project.end_date else 0

        # Dữ liệu task theo độ khó
        difficulty_counts = dict(tasks.values('difficulty').annotate(count=Count('difficulty')).values_list('difficulty', 'count'))

        # Dữ liệu tiến độ theo thời gian (tháng hiện tại)
        month_start = today.replace(day=1)
        progress_by_date = {}
        for i in range(31):  # Tối đa 31 ngày/tháng
            date = month_start + timedelta(days=i)
            if date > today:
                break
            completed_by_date = tasks.filter(
                status='Completed',
                completed_date__date__lte=date
            ).count()
            progress_by_date_value = (completed_by_date / total_tasks * 100) if total_tasks > 0 else 0
            progress_by_date[date.strftime('%d/%m')] = round(progress_by_date_value, 1)

        # Thống kê thành viên
        member_statistics = []
        for user in project.team_members.all():
            user_tasks = tasks.filter(task_assignments__user=user)
            user_completed = user_tasks.filter(task_assignments__status='Completed').count()
            user_progress = (user_completed / user_tasks.count() * 100) if user_tasks.count() > 0 else 0

            member_statistics.append({
                'name': f"{user.first_name} {user.last_name}",
                'task_count': user_tasks.count(),
                'completed': user_completed,
                'progress': round(user_progress, 1)
            })

        return {
            'project_name': project.name,
            'status': status,
            'start_date': project.start_date.strftime('%d/%m/%Y') if project.start_date else None,
            'end_date': project.end_date.strftime('%d/%m/%Y') if project.end_date else None,
            'days_left': days_left,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'progress': round(progress, 1),
            'task_counts': task_counts,
            'difficulty_counts': difficulty_counts,
            'progress_by_date': progress_by_date,
            'member_statistics': member_statistics
        }
    except Exception as e:
        print(f"Error in get_project_progress_data: {str(e)}")
        return {
            'total_tasks': 0,
            'completed_tasks': 0,
            'progress': 0,
            'task_counts': {}
        }


def check_deadline_warnings(task):
    days_until_deadline = task.days_until_deadline
    if task.is_overdue:
        return {'type': 'danger', 'message': 'Task đã quá hạn!'}
    elif 0 <= days_until_deadline <= 2:
        return {'type': 'warning', 'message': f'Task sắp đến hạn ({days_until_deadline} ngày còn lại)!'}
    return None


def calculate_time_by_day(user):
    today = timezone.now().date()
    week_start = today - timedelta(days=6)  # 7 ngày gần nhất
    data = []

    for i in range(7):
        day = week_start + timedelta(days=i)
        # Đảm bảo day_start và day_end là offset-aware
        day_start = timezone.make_aware(timezone.datetime.combine(day, timezone.datetime.min.time()))
        day_end = day_start + timedelta(days=1)
        total_time = 0.0

        entries = TimeEntries.objects.filter(
            user=user,
            start_time__lte=day_end,
            end_time__gte=day_start
        ).exclude(end_time__isnull=True)

        for entry in entries:
            # Giới hạn thời gian trong ngày
            start = max(entry.start_time, day_start)
            end = min(entry.end_time, day_end)  # end_time đã được lọc không null
            if start < end:
                duration = (end - start).total_seconds() / 3600
                total_time += duration

        # Đảm bảo tổng thời gian không vượt quá 24 giờ
        total_time = min(total_time, 24.0)

        data.append({
            'day': day.strftime('%d/%m'),
            'total_time': round(total_time, 2)
            })

    return data


def calculate_time_by_task(user):
    data = []
    tasks = Tasks.objects.filter(
        task_assignments__user=user
    )
    for task in tasks:
        total_time = TimeEntries.objects.filter(
            user=user,
            task=task
        ).aggregate(total=Sum('duration'))['total'] or 0
        if total_time > 0:
            data.append({
                'task_title': task.title,
                'total_time': round(total_time, 2)
                })
    return data


def get_project_status(project):
    """
    Xác định trạng thái dự án dựa trên tiến độ và deadline.
    """
    today = timezone.now().date()
    tasks = Tasks.objects.filter(project=project)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()

    if total_tasks == 0:
        return 'Not started'

    if completed_tasks == total_tasks:
        return 'Completed'

    if project.end_date and project.end_date.date() < today:
        return 'Late'

    return 'In progress'
