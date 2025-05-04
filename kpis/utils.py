from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from .models import EmployeeKPIs
from projects.models import Projects

def get_period_dates(period):
    today = timezone.now()
    if period == 'Weekly':
        start = today - timedelta(days=today.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=7) - timedelta(seconds=1)
    elif period == 'Monthly':
        start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = start + relativedelta(months=1)
        end = next_month - timedelta(seconds=1)
    elif period == 'Quarterly':
        quarter = (today.month - 1) // 3
        start_month = (quarter * 3) + 1
        start = today.replace(day=1, month=start_month, hour=0, minute=0, second=0, microsecond=0)
        end = start + relativedelta(months=3) - timedelta(seconds=1)
    elif period == 'Yearly':
        start = today.replace(day=1, month=1, hour=0, minute=0, second=0, microsecond=0)
        end = start + relativedelta(years=1) - timedelta(seconds=1)
    else:
        raise ValueError("Invalid period")
    return start, end

def calculate_kpi_metrics(kpis):
    """Calculate total KPIs, achieved KPIs, and completion rate."""
    total_kpis = kpis.count()
    achieved_kpis = kpis.filter(evaluation__in=['Achieved', 'Exceeded', 'Partially Achieved']).count()
    completion_rate = (achieved_kpis / total_kpis * 100) if total_kpis > 0 else 0.0
    return total_kpis, achieved_kpis, round(completion_rate, 2)

def filter_kpis_by_project(kpis, project_id):
    """Filter KPIs by project_id, return all if project_id is None or 'all'."""
    if project_id and project_id != 'all':
        return kpis.filter(kpi__project__id=project_id)
    return kpis

def get_all_projects(user):
    """Get all projects associated with user's KPIs."""
    projects = Projects.objects.filter(kpis__employee_kpis__user=user).distinct()
    return projects