from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import EmployeeKPIs
from projects.models import Tasks, TimeEntries
from .utils import get_period_dates, get_all_projects, filter_kpis_by_project, calculate_kpi_metrics
import json
from django.utils.safestring import mark_safe


@login_required
def performance_dashboard(request):
    period = request.GET.get('period', 'Monthly')
    project_id = request.GET.get('project_id', 'all')
    start_date, end_date = get_period_dates(period)
    
    kpis = EmployeeKPIs.objects.filter(
        user=request.user,
        start_date__lte=end_date,
        end_date__gte=start_date
    ).select_related('kpi', 'kpi__project')
    
    kpis = filter_kpis_by_project(kpis, project_id)
    
    for kpi in kpis:
        kpi.update_from_project()
    
    total_kpis, achieved_kpis, completion_rate = calculate_kpi_metrics(kpis)
    
    projects = set()
    for kpi in kpis:
        if kpi.kpi.project:
            projects.add(kpi.kpi.project)
    num_projects = len(projects)
    
    tasks = Tasks.objects.filter(task_assignments__user=request.user)
    tasks_in_period = tasks.filter(
        deadline__gte=start_date,
        deadline__lte=end_date
    )
    
    tasks_with_time = Tasks.objects.filter(
        task_assignments__time_entries__start_time__gte=start_date,
        task_assignments__time_entries__start_time__lte=end_date,
        task_assignments__user=request.user
    )
    
    all_tasks = (tasks_in_period | tasks_with_time).distinct()
    num_tasks = all_tasks.count()
    
    completed_tasks = all_tasks.filter(status='Completed').count()
    in_progress_tasks = all_tasks.filter(status='In progress').count()
    delayed_tasks = all_tasks.filter(deadline__lt=end_date).exclude(status='Completed').count()
    
    total_time = TimeEntries.objects.filter(
        task_assignment__user=request.user,
        start_time__gte=start_date,
        start_time__lte=end_date
    ).aggregate(Sum('duration'))['duration__sum'] or 0.0
    total_time = round(total_time, 2)
    
    valid_kpis = kpis.filter(actual_value__isnull=False)
    kpi_chart_data = {
        'labels': mark_safe(json.dumps([kpi.kpi.name for kpi in valid_kpis], ensure_ascii=False)),
        'data': mark_safe(json.dumps([float(round(kpi.achieved_percentage, 2)) for kpi in valid_kpis])),
        'base64': ''
    }
    context = {
        'period': period,
        'project_id': project_id,
        'start_date': start_date,
        'end_date': end_date,
        'total_kpis': total_kpis,
        'achieved_kpis': achieved_kpis,
        'completion_rate': completion_rate,
        'num_projects': num_projects,
        'num_tasks': num_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'delayed_tasks': delayed_tasks,
        'total_time': total_time,
        'kpis': kpis,
        'kpi_chart_data': kpi_chart_data,
        'projects': get_all_projects(request.user),
    }
    
    return render(request, 'main/pages/kpis/performance_dashboard.html', context)

@login_required
def kpi_detail(request, kpi_id):
    kpi = get_object_or_404(EmployeeKPIs, id=kpi_id, user=request.user)
    context = {
        'kpi': kpi,
        'kpi_info': kpi.kpi,  
    }
    return render(request, 'main/pages/kpis/kpi_detail.html', context)