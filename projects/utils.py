from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import Projects, TimeEntries, TaskAssignments

def filter_tasks(tasks, project_id=None, status=None):
    if project_id:
        tasks = tasks.filter(project_id=project_id)
    if status:
        tasks = tasks.filter(status=status)
    return tasks

def get_user_projects(user):
    return Projects.objects.filter(Q(manager=user) | Q(team_members=user)).distinct()

def calculate_time_totals(user):
    today = timezone.localtime(timezone.now(), timezone=timezone.get_fixed_timezone(420)).date()
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

def check_deadline_warnings(task):
    days_until_deadline = task.days_until_deadline
    if task.is_overdue:
        return {'type': 'danger', 'message': 'Task đã quá hạn!'}
    elif 0 <= days_until_deadline <= 2:
        return {'type': 'warning', 'message': f'Task sắp đến hạn ({days_until_deadline} ngày còn lại)!'}
    return None

def calculate_time_by_day(user):
    end_date = timezone.localtime(timezone.now(), timezone=timezone.get_fixed_timezone(420)).date()
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
            
            task_title = str(task.title).replace('"', '\\"').replace("'", "\\'")

            task_data = {
                'task_id': task.id,
                'task_title': task_title,
                'project_name': task.project.name,
                'total_time': float(total_time),  
                'status': status,
                'estimated_time': float(estimated_time),  
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
    today = timezone.localtime(timezone.now(), timezone=timezone.get_fixed_timezone(420)).date()
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