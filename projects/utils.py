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
    task.save()


def update_task_status(task, status):
    task.status = status
    if task.deadline < timezone.now().date() and status != 'Completed':
        task.status = 'Late'
    task.save()


def calculate_days_overdue(deadline):
    return (timezone.now().date() - deadline).days


def calculate_time_totals(user):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    total_time_today = TimeEntries.objects.filter(
        user=user,
        start_time__date=today
    ).aggregate(total=Sum('duration'))['total'] or 0
    total_time_week = TimeEntries.objects.filter(
        user=user,
        start_time__gte=week_start
    ).aggregate(total=Sum('duration'))['total'] or 0
    total_time_month = TimeEntries.objects.filter(
        user=user,
        start_time__gte=month_start
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
    return members_data


def get_project_progress_data(project_id):
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