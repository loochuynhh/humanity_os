# projects/views.py
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from django.views.decorators.http import require_POST, require_http_methods
from .models import Tasks, Projects, TimeEntries, TeamProjectMembership
from .utils import (
    calculate_days_overdue,
    calculate_team_member_data,
    calculate_time_totals,
    filter_tasks,
    get_project_progress,
    get_project_progress_data,
    get_user_projects,
    update_task_status,
    update_task_tracking,
)


@login_required
def all_tasks(request):
    projects = get_user_projects(request.user)
    tasks = Tasks.objects.filter(project__in=projects).select_related('project').prefetch_related('task_assignments__user')
    tasks = filter_tasks(tasks, request.GET.get('project'), request.GET.get('status'))
    return render(request, 'main/pages/projects/all_tasks.html', {
        'tasks': tasks,
        'projects': projects,
        'status_choices': Tasks.STATUS_CHOICES,
        'now': timezone.now().date()
    })


@login_required
def my_tasks(request):
    tasks = Tasks.objects.filter(task_assignments__user=request.user).select_related('project').prefetch_related('task_assignments__user')
    for task in tasks:
        update_task_tracking(task, request.user)
    return render(request, 'main/pages/projects/my_tasks.html', {
        'tasks': tasks,
        'status_choices': Tasks.STATUS_CHOICES,
        'now': timezone.now().date()
    })


@require_POST
@login_required
def update_status(request):
    try:
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')
        task = Tasks.objects.get(id=task_id, task_assignments__user=request.user)
        update_task_status(task, status)
        return JsonResponse({
            'success': True,
            'new_status': task.status
        })
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task không tồn tại hoặc không có quyền'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
@login_required # type: ignore
def toggle_time(request: HttpRequest):
    try:
        task_id = request.POST.get('task_id')
        action = request.POST.get('action')
        if not task_id or not action:
            return JsonResponse({'success': False, 'error': 'Thiếu tham số'}, status=400)
        task = Tasks.objects.get(id=task_id, task_assignments__user=request.user)
        if action == 'start':
            if TimeEntries.objects.filter(user=request.user, end_time__isnull=True).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Bạn đang tracking một task khác. Hãy dừng nó trước.'
                }, status=400)
            TimeEntries.objects.create(user=request.user, task=task, start_time=timezone.now())
            task.is_tracking = True
            task.save()
            return JsonResponse({'success': True, 'action': 'started'})
        elif action == 'stop':
            entry = TimeEntries.objects.get(user=request.user, task=task, end_time__isnull=True)
            entry.end_time = timezone.now()
            entry.save()
            task.total_time = TimeEntries.objects.filter(task=task, user=request.user).aggregate(total=Sum('duration'))['total'] or 0
            task.is_tracking = False
            task.save()
            return JsonResponse({
                'success': True,
                'action': 'stopped',
                'duration': entry.duration
            })
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Không tìm thấy task hoặc entry'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def overdue_tasks(request):
    tasks = Tasks.objects.filter(
        task_assignments__user=request.user,
        deadline__lt=timezone.now().date(),
        status__in=['To-do', 'In progress', 'Late']
    ).select_related('project')
    tasks_with_overdue = [{'task': task, 'days_overdue': calculate_days_overdue(task.deadline)} for task in tasks]
    return render(request, 'main/pages/projects/overdue_tasks.html', {
        'tasks_with_overdue': tasks_with_overdue,
        'now': timezone.now().date()
    })


@require_http_methods(["POST"])
@login_required
def extend_deadline(request, task_id):
    try:
        task = Tasks.objects.get(id=task_id, task_assignments__user=request.user)
        new_deadline = request.POST.get('new_deadline')
        if not new_deadline:
            return JsonResponse({'success': False, 'error': 'Vui lòng chọn ngày gia hạn'}, status=400)
        task.deadline = new_deadline
        update_task_status(task, task.status)
        return JsonResponse({
            'success': True,
            'new_deadline': task.deadline.strftime('%d/%m/%Y'),
            'new_status': task.status
        })
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task không tồn tại hoặc không có quyền'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def time_tracking(request):
    tasks = Tasks.objects.filter(task_assignments__user=request.user).select_related('project')
    for task in tasks:
        update_task_tracking(task, request.user)
    time_entries = TimeEntries.objects.filter(user=request.user).select_related('task').order_by('-start_time')
    time_totals = calculate_time_totals(request.user)
    context = {
        'tasks': tasks,
        'time_entries': time_entries,
        'total_time_today': time_totals['today'],
        'total_time_week': time_totals['week'],
        'total_time_month': time_totals['month'],
    }
    return render(request, 'main/pages/projects/time_tracking.html', context)


@login_required
def all_projects(request):
    projects = Projects.objects.all()
    context = {
        'projects': projects,
        'today': timezone.now().date(),
    }
    return render(request, 'main/pages/projects/all_projects.html', context)


@login_required
def my_projects(request):
    memberships = TeamProjectMembership.objects.filter(user=request.user).select_related('project')
    memberships_with_progress = [
        {'membership': m, 'progress': get_project_progress(m.project)}
        for m in memberships
    ]
    context = {
        'memberships': memberships_with_progress,
    }
    return render(request, 'main/pages/projects/my_projects.html', context)


@login_required
def team_members(request):
    projects = Projects.objects.filter(team_members=request.user)
    context = {
        'projects': projects,
    }
    return render(request, 'main/pages/projects/team_members.html', context)


@login_required
def team_members_data(request):
    project_id = request.GET.get('project_id')
    members_data = calculate_team_member_data(project_id) if project_id else []
    return JsonResponse({'members': members_data})


@login_required
def project_progress(request):
    projects = Projects.objects.filter(team_members=request.user)
    context = {
        'projects': projects,
    }
    return render(request, 'main/pages/projects/project_progress.html', context)


@login_required
def project_progress_data(request):
    project_id = request.GET.get('project_id')
    progress_data = get_project_progress_data(project_id) if project_id else {
        'total_tasks': 0,
        'completed_tasks': 0,
        'progress': 0,
        'task_counts': {}
    }
    return JsonResponse(progress_data)