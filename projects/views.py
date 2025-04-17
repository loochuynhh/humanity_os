# projects/views.py
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from django.views.decorators.http import require_POST, require_http_methods
from .models import Tasks, Projects, TimeEntries, TeamProjectMembership, DeadlineExtensionRequest
from .utils import (
    calculate_team_member_data,
    calculate_time_totals,
    filter_tasks,
    get_project_progress,
    get_project_progress_data,
    get_user_projects,
    update_task_status,
    update_task_tracking,
    check_deadline_warnings
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
def my_tasks(request):
    tasks = Tasks.objects.filter(task_assignments__user=request.user).select_related('project').prefetch_related('task_assignments__user')
    for task in tasks:
        update_task_tracking(task, request.user)
    tasks_with_details = []
    for task in tasks:
        warning = check_deadline_warnings(task)
        time_entries = TimeEntries.objects.filter(task=task, user=request.user).order_by('-start_time')[:5]  # Lấy 5 entries gần nhất
        # Tính phần trăm tiến độ
        progress_percentage = 0
        if task.estimated_time and task.estimated_time > 0:  # Kiểm tra để tránh chia cho 0
            progress_percentage = (task.total_time / task.estimated_time) * 100
            progress_percentage = min(100, max(0, round(progress_percentage)))  # Giới hạn trong khoảng 0-100
        # Chuẩn bị dữ liệu time_entries để truyền vào HTML
        time_entries_html = ""
        for entry in time_entries:
            end_time = entry.end_time.strftime("%d/%m/%Y %H:%M") if entry.end_time else "Đang tracking"
            # Định dạng duration bằng Python
            duration = round(float(entry.duration), 1) if entry.duration is not None else 0.0
            time_entries_html += f'<li>{entry.start_time.strftime("%d/%m/%Y %H:%M")} - {end_time} ({duration} giờ)</li>'
        tasks_with_details.append({
            'task': task,
            'warning': warning,
            'time_entries': time_entries,
            'time_entries_html': time_entries_html,  # Dữ liệu HTML để JavaScript sử dụng
            'progress_percentage': progress_percentage,
        })
    return render(request, 'main/pages/projects/my_tasks.html', {
        'tasks_with_details': tasks_with_details,
        'status_choices': Tasks.STATUS_CHOICES,
        'difficulty_choices': Tasks.DIFFICULTY_CHOICES,
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
@login_required
def toggle_time(request: HttpRequest) -> JsonResponse:
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

@require_POST
@login_required
def update_task_details(request):
    try:
        task_id = request.POST.get('task_id')
        task = Tasks.objects.get(id=task_id, task_assignments__user=request.user)
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.difficulty = request.POST.get('difficulty', task.difficulty)
        task.estimated_time = float(request.POST.get('estimated_time', task.estimated_time)) if request.POST.get('estimated_time') else task.estimated_time
        task.github_link = request.POST.get('github_link', task.github_link)
        task.notes = request.POST.get('notes', task.notes)
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