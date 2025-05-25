from django.shortcuts import render, redirect

from django.contrib.auth import logout
from custom_admin.utils import superuser_required
from django.apps import apps
from django.db.models import Count, Avg
from django.contrib.auth import get_user_model
from django.contrib.admin.models import LogEntry
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta

# Authentication
def logout_view(request):
    logout(request)
    return redirect("/admin/")

@superuser_required
def index(request):
    """
    Admin dashboard view with statistics and charts
    """
    User = get_user_model()
    
    # Get counts for dashboard stats
    user_count = User.objects.count()
    active_user_count = User.objects.filter(is_active=True).count()
    
    # Try to get Projects model
    try:
        Projects = apps.get_model('projects', 'Projects')
        project_count = Projects.objects.count()
        
        active_projects = Projects.objects.filter(
            end_date__gt=timezone.now()
        ).order_by('-id')[:5]
        
        now = timezone.now()
        completed_projects = Projects.objects.filter(end_date__lt=now).count()
        ongoing_projects = project_count - completed_projects
        
        project_data = []
        for project in active_projects:
            try:
                task_count = getattr(project, 'tasks', None)
                task_count = task_count.count() if task_count else 0
                
                completed_tasks = getattr(project, 'tasks', None)
                completed_tasks = completed_tasks.filter(status='Completed').count() if completed_tasks else 0
                
                progress = round((completed_tasks / task_count * 100), 0) if task_count > 0 else 0
                
                team_members = getattr(project, 'team_members', None)
                team_count = team_members.count() if team_members else 0
                
                team_members_list = list(team_members.all()[:3]) if team_members else []
                team_initials = []
                for member in team_members_list:
                    if member.first_name and member.last_name:
                        initials = f"{member.first_name[0]}{member.last_name[0]}"
                    else:
                        initials = member.username[:2].upper()
                    team_initials.append({
                        'initials': initials,
                        'id': member.id,
                        'username': member.username
                    })
                    
                if hasattr(project, 'end_date'):
                    if now.date() >= project.end_date.date():
                        status = "Overdue"
                        status_class = "danger"
                    elif (project.end_date.date() - now.date()).days <= 7:
                        status = "Due Soon"
                        status_class = "warning"
                    else:
                        status = "In Progress"
                        status_class = "success"
                else:
                    status = "Unknown"
                    status_class = "secondary"
                
                project_data.append({
                    'id': project.id if hasattr(project, 'id') else '',
                    'name': project.name if hasattr(project, 'name') else f"Project {project.pk}",
                    'deadline': project.end_date if hasattr(project, 'end_date') else None,
                    'status': status,
                    'status_class': status_class,
                    'team_members': team_initials,
                    'team_count': team_count,
                    'progress': progress
                })
            except Exception as e:
                project_name = getattr(project, 'name', f"Project {project.pk}")
                print(f"Error processing project data {project_name}: {str(e)}")
        
        project_chart_data = {
            'labels': ['In Progress', 'Completed'],
            'data': [ongoing_projects, completed_projects],
            'colors': ['#0d6efd', '#198754']
        }
        
    except Exception as e:
        print(f"Error loading project data: {str(e)}")
        project_count = 0
        project_data = []
        project_chart_data = {
            'labels': ['No Data'],
            'data': [1],
            'colors': ['#6c757d']
        }
    
    # Try to get Tasks model
    try:
        Tasks = apps.get_model('projects', 'Tasks')
        task_count = Tasks.objects.count()
        
        task_status = Tasks.objects.values('status').annotate(count=Count('id'))
        task_status_data = {item['status']: item['count'] for item in task_status}
        
        for status in ['To-do', 'In progress', 'Completed', 'Late']:
            if status not in task_status_data:
                task_status_data[status] = 0
                
        task_chart_data = {
            'labels': list(task_status_data.keys()),
            'data': list(task_status_data.values()),
            'colors': ['#0d6efd', '#ffc107', '#198754', '#dc3545']
        }
    except Exception as e:
        print(f"Error loading task data: {str(e)}")
        task_count = 0
        task_chart_data = {
            'labels': ['No Data'],
            'data': [1],
            'colors': ['#6c757d']
        }
    
    # Calculate user growth for past 6 months
    months_data = []
    labels = []
    
    now = timezone.now()
    for i in range(5, -1, -1):
        month_start = (now - relativedelta(months=i)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = (month_start + relativedelta(months=1) - timedelta(seconds=1))
        
        count = User.objects.filter(date_joined__gte=month_start, date_joined__lte=month_end).count()
        months_data.append(count)
        
        month_name = month_start.strftime("%b")
        labels.append(f"{month_name} {month_start.year}")
    
    user_chart_data = {
        'labels': labels,
        'data': months_data,
    }
    
    # Calculate trend percentages
    previous_month_start = (now - relativedelta(months=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_month_end = (current_month_start + relativedelta(months=1) - timedelta(seconds=1))
    
    current_month_users = User.objects.filter(date_joined__gte=current_month_start, date_joined__lte=current_month_end).count()
    previous_month_users = User.objects.filter(
        date_joined__gte=previous_month_start, 
        date_joined__lt=current_month_start
    ).count()
    
    if previous_month_users > 0:
        user_trend = round((current_month_users - previous_month_users) / previous_month_users * 100, 1)
    else:
        user_trend = current_month_users * 100 if current_month_users > 0 else 0
    
    # Get recent activity logs
    recent_logs = LogEntry.objects.select_related('content_type', 'user').order_by('-action_time')[:10]
    
    # Performance metrics data (KPIs)
    try:
        EmployeeKPIs = apps.get_model('kpis', 'EmployeeKPIs')
        
        kpi_count = EmployeeKPIs.objects.count()
        achieved_kpis = EmployeeKPIs.objects.filter(
            evaluation__in=['Achieved', 'Exceeded']
        ).count()
        
        partially_achieved = EmployeeKPIs.objects.filter(
            evaluation='Partially Achieved'
        ).count()
        
        not_achieved = EmployeeKPIs.objects.filter(
            evaluation='Not Achieved'
        ).count()
        
        avg_achievement = EmployeeKPIs.objects.aggregate(
            avg=Avg('achieved_percentage')
        )['avg'] or 0
        
        kpis_by_type = EmployeeKPIs.objects.values(
            'kpi__kpi_type'
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        
        performance_chart_data = {
            'labels': ['Exceeded/Achieved', 'Partially Achieved', 'Not Achieved'],
            'data': [achieved_kpis, partially_achieved, not_achieved],
            'colors': ['#198754', '#ffc107', '#dc3545']
        }
        
    except Exception as e:
        print(f"Error loading KPI data: {str(e)}")
        performance_chart_data = {
            'labels': ['No Data'],
            'data': [1],
            'colors': ['#6c757d']
        }
        kpi_count = 0
        avg_achievement = 0
    
    context = {
        'title': 'Admin Dashboard',
        'user_count': user_count,
        'active_user_count': active_user_count,
        'user_trend': user_trend,
        'user_chart_data': user_chart_data,
        'project_count': project_count,
        'project_data': project_data,
        'project_chart_data': project_chart_data,
        'task_count': task_count,
        'task_chart_data': task_chart_data,
        'kpi_count': kpi_count,
        'avg_achievement': round(float(avg_achievement), 2),
        'performance_chart_data': performance_chart_data,
        'activity_count': LogEntry.objects.count(),
        'recent_logs': recent_logs,
    }
    
    return render(request, 'admin/dashboard.html', context)