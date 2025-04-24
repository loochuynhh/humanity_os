# projects/views.py
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from django.views.decorators.http import require_POST, require_http_methods
from .models import Tasks, Projects, TimeEntries, TeamProjectMembership, DeadlineExtensionRequest, TaskAssignments
from .utils import (
    calculate_team_member_data,
    calculate_time_totals,
    filter_tasks,
    get_project_progress,
    get_project_progress_data,
    get_user_projects,
    update_task_status,
    update_task_tracking,
    check_deadline_warnings,
    calculate_time_by_day,
    calculate_time_by_task
)


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
    tasks_with_details = []
    for task in tasks:
        warning = check_deadline_warnings(task)
        time_entries = TimeEntries.objects.filter(task=task, user=request.user).order_by('-start_time')[:5]
        progress_percentage = 0
        if task.estimated_time and task.estimated_time > 0:
            progress_percentage = (task.total_time / task.estimated_time) * 100
            progress_percentage = min(100, max(0, round(progress_percentage)))
        tasks_with_details.append({
            'task': task,
            'warning': warning,
            'time_entries': time_entries,
            'progress_percentage': progress_percentage,
        })
    return render(request, 'main/pages/projects/my_tasks.html', {
        'tasks_with_details': tasks_with_details,
        'status_choices': Tasks.STATUS_CHOICES,
        'difficulty_choices': Tasks.DIFFICULTY_CHOICES,
        'now': timezone.now().date()
    })


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Tasks.objects.select_related('project').prefetch_related('task_assignments__user'), 
                             id=task_id, task_assignments__user=request.user)
    task.update_total_time()  # Cập nhật total_time
    task.update_start_date()  # Cập nhật start_date
    progress_percentage = 0
    if task.estimated_time and task.estimated_time > 0:
        progress_percentage = (task.total_time / task.estimated_time) * 100
        progress_percentage = min(100, max(0, round(progress_percentage)))
    
    # Lấy TimeEntries liên quan đến task
    time_entries = TimeEntries.objects.filter(task=task).select_related('user').order_by('-start_time')
    
    context = {
        'task': task,
        'progress_percentage': progress_percentage,
        'status_choices': Tasks.STATUS_CHOICES,
        'difficulty_choices': Tasks.DIFFICULTY_CHOICES,
        'task_assignments': task.task_assignments.all(), # type: ignore
        'time_entries': time_entries,  # Thêm time_entries vào context
    }
    return render(request, 'main/pages/projects/task_detail.html', context)


@require_POST
@login_required
def update_status(request):
    try:
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')
        task = Tasks.objects.get(id=task_id, task_assignments__user=request.user)
        assignment = task.task_assignments.get(user=request.user) # type: ignore
        assignment.status = status
        if task.deadline < timezone.now().date() and status != "Completed":
            assignment.status = "Late"
        assignment.save()
        task.update_status_from_assignments()  
        return JsonResponse({
            'success': True,
            'new_status': assignment.status
        })
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task không tồn tại hoặc không có quyền'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
@login_required
def toggle_time(request: HttpRequest) -> JsonResponse: # type: ignore
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
            task.update_start_date() 
            task.save()
            return JsonResponse({'success': True, 'action': 'started'})
        elif action == 'stop':
            entry = TimeEntries.objects.get(user=request.user, task=task, end_time__isnull=True)
            entry.end_time = timezone.now()
            entry.save()
            task.update_total_time()  
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


@require_POST
@login_required
def update_task_details(request):
    try:
        task_id = request.POST.get('task_id')
        task = Tasks.objects.get(id=task_id, task_assignments__user=request.user)
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.difficulty = request.POST.get('difficulty', task.difficulty)
        task.github_link = request.POST.get('github_link', task.github_link)
        task.notes = request.POST.get('notes', task.notes)
        
        assignment = task.task_assignments.get(user=request.user) # type: ignore
        assignment_estimated_time = request.POST.get(f'estimated_time_{assignment.user.id}')
        if assignment_estimated_time:
            assignment.estimated_time = float(assignment_estimated_time)
            assignment.save()
        
        task.save()
        return JsonResponse({'success': True, 'message': 'Cập nhật task thành công!'})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task không tồn tại hoặc không có quyền'}, status=404)
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Dữ liệu không hợp lệ'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
@login_required
def request_deadline_extension(request):
    try:
        task_id = request.POST.get('task_id')
        requested_deadline = request.POST.get('requested_deadline')
        reason = request.POST.get('reason')
        if not requested_deadline or not reason:
            return JsonResponse({'success': False, 'error': 'Vui lòng cung cấp ngày và lý do'}, status=400)
        task = Tasks.objects.get(id=task_id, task_assignments__user=request.user)
        DeadlineExtensionRequest.objects.create(
            task=task,
            requested_by=request.user,
            requested_deadline=requested_deadline,
            reason=reason
        )
        return JsonResponse({'success': True, 'message': 'Yêu cầu gia hạn đã được gửi!'})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task không tồn tại hoặc không có quyền'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


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
    time_entries = TimeEntries.objects.filter(user=request.user).select_related('task').order_by('-start_time')
    time_totals = calculate_time_totals(request.user)
    
    # Dữ liệu cho biểu đồ
    time_by_day = calculate_time_by_day(request.user)
    time_by_task = calculate_time_by_task(request.user)
    
    context = {
        'time_entries': time_entries,
        'total_time_today': time_totals['today'],
        'total_time_week': time_totals['week'],
        'total_time_month': time_totals['month'],
        'time_by_day': time_by_day,
        'time_by_task': time_by_task,
        'status_choices': Tasks.STATUS_CHOICES,
    }
    return render(request, 'main/pages/projects/time_tracking.html', context)

@require_POST
@login_required
def update_time_entry(request):
    try:
        entry_id = request.POST.get('entry_id')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        if not entry_id or not start_time:
            return JsonResponse({'success': False, 'error': 'Thiếu tham số'}, status=400)
        
        entry = TimeEntries.objects.get(id=entry_id, user=request.user)
        entry.start_time = timezone.datetime.fromisoformat(start_time.replace('T', ' '))
        if end_time:
            entry.end_time = timezone.datetime.fromisoformat(end_time.replace('T', ' '))
        else:
            entry.end_time = None
            entry.duration = None
        entry.save()
        
        # Cập nhật task liên quan
        task = entry.task
        task.update_total_time()
        task.update_start_date()
        task.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cập nhật time entry thành công!',
            'duration': entry.duration if entry.duration else 0
        })
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Time entry không tồn tại hoặc không có quyền'}, status=404)
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Dữ liệu không hợp lệ'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_POST
@login_required
def update_assignment_status(request):
    try:
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')
        if not task_id or not status:
            return JsonResponse({'success': False, 'error': 'Thiếu tham số'}, status=400)
        
        assignment = TaskAssignments.objects.get(task_id=task_id, user=request.user)
        if status not in dict(Tasks.STATUS_CHOICES):
            return JsonResponse({'success': False, 'error': 'Trạng thái không hợp lệ'}, status=400)
        
        assignment.status = status
        assignment.save()
        
        # Cập nhật trạng thái task nếu cần
        task = assignment.task
        task.update_status_from_assignments()
        
        return JsonResponse({
            'success': True,
            'message': 'Cập nhật trạng thái thành công!'
        })
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task assignment không tồn tại hoặc không có quyền'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)