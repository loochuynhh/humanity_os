from django.db.models import Count, Sum, ExpressionWrapper, F, DurationField
from django.utils import timezone
from datetime import timedelta
import json
from projects.models import Tasks, TaskAssignments, TimeEntries, Projects
from users.models import EmployeeKPIs
from users.models import PersonalGoals

def get_task_counts(user_id, as_json=False):
    task_counts = TaskAssignments.objects.filter(user_id=user_id).values('task__status').annotate(count=Count('task__id'))
    task_status = {'To_do': 0, 'In_progress': 0, 'Completed': 0}
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
    
    total_duration = entries.filter(end_time__isnull=False).aggregate(
        total=Sum(
            ExpressionWrapper(
                F('end_time') - F('start_time'),
                output_field=DurationField()
            )
        )
    )['total'] or timedelta(0)
    
    total_hours = total_duration.total_seconds() / 3600
    
    if period == 'week' and as_json:

        week_data = []
        for i in range(7):
            day = week_start + timedelta(days=i)
            day_entries = entries.filter(start_time__date=day, end_time__isnull=False)
            day_duration = day_entries.aggregate(
                total=Sum(
                    ExpressionWrapper(
                        F('end_time') - F('start_time'),
                        output_field=DurationField()
                    )
                )
            )['total'] or timedelta(0)
            week_data.append(day_duration.total_seconds() / 3600)
        return json.dumps(week_data)
    
    hours = int(total_hours)
    minutes = int((total_hours - hours) * 60)
    return f"{hours}h {minutes}m" if not as_json else json.dumps([total_hours])
def get_kpi_snapshot(user_id, metric='completion'):
    kpi = EmployeeKPIs.objects.filter(user_id=user_id, period='monthly').first()
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

def get_project_progress(user_id):
    projects = Projects.objects.filter(tasks__taskassignments__user_id=user_id).distinct()
    project_progress = []
    for project in projects:
        total_tasks = Tasks.objects.filter(project_id=project.pk).count()
        completed_tasks = Tasks.objects.filter(project_id=project.pk, status='Completed').count()
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        project_progress.append({'name': project.name, 'progress': progress})
    return project_progress

def get_ai_suggestions(user_id):
    return Tasks.objects.filter(
        taskassignments__user_id=user_id, 
        status__in=['To-do', 'In progress']
    ).values('title', 'difficulty', 'estimated_time')[:2]

def get_recent_tasks(user_id):
    return Tasks.objects.filter(taskassignments__user_id=user_id).select_related('project').order_by('-deadline')[:5]

def get_personal_goals(user_id):
    goals = PersonalGoals.objects.filter(user_id=user_id).order_by('target_date')
    goal_progress = []
    for goal in goals:
        progress = 100 if goal.status == 'achieved' else (0 if goal.status == 'missed' else 50)
        goal_progress.append({'description': goal.goal_description, 'progress': progress})
    return goal_progress