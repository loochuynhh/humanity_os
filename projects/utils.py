from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Tasks, Projects, TimeEntries, TeamProjectMembership, TaskAssignments

def filter_tasks(tasks, project_id=None, status=None):
    if project_id:
        tasks = tasks.filter(project_id=project_id)
    if status:
        tasks = tasks.filter(status=status)
    return tasks

def get_user_projects(user):
    return Projects.objects.filter(Q(manager=user) | Q(team_members=user)).distinct()

def update_task_tracking(task, user):
    try:
        assignment = TaskAssignments.objects.get(task=task, user=user)
        task.is_tracking = TimeEntries.objects.filter(task_assignment=assignment, end_time__isnull=True).exists()
        task.save()
    except TaskAssignments.DoesNotExist:
        pass

def calculate_time_totals(user):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    week_start_dt = timezone.make_aware(timezone.datetime.combine(week_start, timezone.datetime.min.time()))
    month_start_dt = timezone.make_aware(timezone.datetime.combine(month_start, timezone.datetime.min.time()))

    assignments = TaskAssignments.objects.filter(user=user)
    time_entries = TimeEntries.objects.filter(task_assignment__in=assignments)

    total_time_today = time_entries.filter(start_time__gte=today_start, start_time__lt=today_start + timedelta(days=1)).aggregate(total=Sum('duration'))['total'] or 0
    total_time_week = time_entries.filter(start_time__gte=week_start_dt).aggregate(total=Sum('duration'))['total'] or 0
    total_time_month = time_entries.filter(start_time__gte=month_start_dt).aggregate(total=Sum('duration'))['total'] or 0

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
    tasks = project.tasks.all()
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
            assignments = TaskAssignments.objects.filter(task__project=project, user=user)
            task_count = Tasks.objects.filter(task_assignments__in=assignments).distinct().count()
            total_time = assignments.aggregate(total=Sum('actual_time'))['total'] or 0
            total_time_str = f"{int(total_time)}h {int((total_time % 1) * 60)}m"
            members_data.append({
                'name': user.get_full_name(),
                'role': 'Quản lý' if user == project.manager else membership. role,
                'join_date': membership.join_date.strftime('%d/%m/%Y'),
                'task_count': task_count,
                'total_time': total_time_str,
            })
    except Exception as e:
        print(f"Error in calculate_team_member_data: {str(e)}")
    return members_data

def get_project_progress_data(project_id):
    try:
        project = Projects.objects.get(id=project_id)
        today = timezone.now().date()
        tasks = project.tasks.all()
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='Completed').count()
        task_counts = dict(tasks.values('status').annotate(count=Count('status')).values_list('status', 'count'))
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        status = get_project_status(project)[0]
        days_left = (project.end_date.date() - today).days if project.end_date else 0
        difficulty_counts = dict(tasks.values('difficulty').annotate(count=Count('difficulty')).values_list('difficulty', 'count'))

        month_start = today.replace(day=1)
        progress_by_date = {}
        for i in range(31):
            date = month_start + timedelta(days=i)
            if date > today:
                break
            completed_by_date = tasks.filter(status='Completed', completed_date__date__lte=date).count()
            progress_by_date_value = (completed_by_date / total_tasks * 100) if total_tasks > 0 else 0
            progress_by_date[date.strftime('%d/%m')] = round(progress_by_date_value, 1)

        member_statistics = []
        for user in project.team_members.all():
            assignments = TaskAssignments.objects.filter(task__project=project, user=user)
            user_tasks = tasks.filter(task_assignments__in=assignments).distinct()
            user_completed = assignments.filter(status='Completed').count()
            user_progress = (user_completed / assignments.count() * 100) if assignments.count() > 0 else 0
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
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=14)
    assignments = TaskAssignments.objects.filter(user=user)
    time_entries = TimeEntries.objects.filter(task_assignment__in=assignments, start_time__date__gte=start_date)
    
    result = []
    current_date = start_date
    while current_date <= end_date:
        day_entries = time_entries.filter(start_time__date=current_date)
        total_time = day_entries.aggregate(total=Sum('duration'))['total'] or 0
        estimated_time = sum(a.estimated_time or 0 for a in assignments if a.task.deadline.date() == current_date)
        
        day_data = {
            'day': current_date.strftime('%d/%m/%Y'),
            'total_time': round(total_time, 2),
            'estimated_time': round(estimated_time, 2) or 8,
        }
        result.append(day_data)
        current_date += timedelta(days=1)
    
    return result

def calculate_time_by_task(user):
    assignments = TaskAssignments.objects.filter(user=user).select_related('task__project')
    result = []
    
    for assignment in assignments:
        try:
            task = assignment.task
            total_time = assignment.actual_time or 0
            status = assignment.status
            estimated_time = assignment.estimated_time or task.estimated_time or 0
            completion_percentage = 100 if status == 'Completed' else min(round((total_time / (estimated_time or 1)) * 100), 95) if status == 'In progress' else 0
            
            # Sanitize task_title to avoid JSON parsing issues
            task_title = str(task.title).replace('"', '\\"').replace("'", "\\'")

            task_data = {
                'task_id': task.id,
                'task_title': task_title,
                'project_name': task.project.name,
                'total_time': float(total_time),  # Ensure float
                'status': status,
                'estimated_time': float(estimated_time),  # Ensure float
                'completion_percentage': completion_percentage,
                'difficulty': task.difficulty,
                'role': assignment.role
            }
            result.append(task_data)
        except Exception as e:
            print(f"Error processing task assignment {assignment.id}: {str(e)}")
    
    result.sort(key=lambda x: x['total_time'], reverse=True)
    return result

def get_project_status(project):
    today = timezone.now().date()
    tasks = project.tasks.all()
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()

    if total_tasks == 0 or project.start_date.date() > today:
        return 'Not started', 'Chưa thực hiện'
    if completed_tasks == total_tasks and total_tasks > 0:
        return 'Completed', 'Đã hoàn thành'
    if project.end_date.date() < today:
        return 'Late', 'Quá hạn'
    return 'In progress', 'Đang thực hiện'