# projects/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.utils import timezone
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from .models import Tasks, Projects, TimeEntries, TeamProjectMembership
from django.http import HttpRequest
from typing import cast
from django.http.response import HttpResponseBase

@login_required
def all_tasks(request):
    managed_projects = Projects.objects.filter(manager=request.user)
    
    member_projects = Projects.objects.filter(
        id__in=TeamProjectMembership.objects.filter(user=request.user).values('project_id')
    )
    
    projects = (managed_projects | member_projects).distinct()
    
    tasks = Tasks.objects.filter(
        project__in=projects
    ).select_related('project').prefetch_related('task_assignments__user')
    
    project_id = request.GET.get('project')
    status = request.GET.get('status')
    
    if project_id:
        tasks = tasks.filter(project_id=project_id)
    if status:
        tasks = tasks.filter(status=status)
    
    return render(request, 'main/pages/projects/all_tasks.html', {
        'tasks': tasks,
        'projects': projects,
        'status_choices': Tasks.STATUS_CHOICES,
        'now': timezone.now().date()
    })

@login_required
def my_tasks(request):
    """Hiển thị các task được giao cho user hiện tại"""
    tasks = Tasks.objects.filter(
        task_assignments__user=request.user
    ).select_related('project').prefetch_related('task_assignments__user')
    
    for task in tasks:
        task.is_tracking = TimeEntries.objects.filter(
            task=task, 
            user=request.user,
            end_time__isnull=True
        ).exists()
        task.save()  
    
    return render(request, 'main/pages/projects/my_tasks.html', {
        'tasks': tasks,
        'status_choices': Tasks.STATUS_CHOICES,
        'now': timezone.now().date()
    })

@require_POST
@login_required
def update_status(request):
    """Cập nhật trạng thái task (AJAX)"""
    try:
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')
        
        task = Tasks.objects.get(
            id=task_id,
            task_assignments__user=request.user
        )
        
        task.status = status
        if task.deadline < timezone.now().date() and status != 'Completed':
            task.status = 'Late'
        task.save()
        
        return JsonResponse({
            'success': True, 
            'new_status': task.status,
            'status_display': task.get_status_display()
        })
    
    except ObjectDoesNotExist:
        return JsonResponse(
            {'success': False, 'error': 'Task không tồn tại hoặc không có quyền'}, 
            status=404
        )
    except Exception as e:
        return JsonResponse(
            {'success': False, 'error': str(e)}, 
            status=400
        )

@require_POST
@login_required
def toggle_time(request: HttpRequest) -> HttpResponseBase:
    """Bắt đầu/dừng tracking thời gian làm task (AJAX)"""
    try:
        task_id = request.POST.get('task_id')
        action = request.POST.get('action')
        if not task_id or not action:
            return JsonResponse(
                {'success': False, 'error': 'Thiếu tham số'}, 
                status=400
            )
            
        task = Tasks.objects.get(
            id=task_id,
            task_assignments__user=request.user
        )
        
        if action == 'start':
            if TimeEntries.objects.filter(
                user=request.user, 
                end_time__isnull=True
            ).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Bạn đang tracking một task khác. Hãy dừng nó trước.'
                }, status=400)
                
            TimeEntries.objects.create(
                user=request.user,
                task=task,
                start_time=timezone.now()
            )
            task.is_tracking = True
            task.save()
            
            return cast(HttpResponseBase, JsonResponse(
                {'success': True, 'action': 'started'}
            ))
        
        elif action == 'stop':
            entry = TimeEntries.objects.get(
                user=request.user,
                task=task,
                end_time__isnull=True
            )
            entry.end_time = timezone.now()
            entry.save()
            
            task.total_time = TimeEntries.objects.filter(
                task=task,
                user=request.user
            ).aggregate(total=Sum('duration'))['total'] or 0
            task.is_tracking = False
            task.save()
            
            return cast(HttpResponseBase, JsonResponse({
                'success': True,
                'action': 'stopped',
                'duration': entry.duration
            }))
            
    except ObjectDoesNotExist:
        return cast(HttpResponseBase, JsonResponse(
            {'success': False, 'error': 'Không tìm thấy task hoặc entry'}, 
            status=404
        ))
    except Exception as e:
        return cast(HttpResponseBase, JsonResponse(
            {'success': False, 'error': str(e)}, 
            status=400
        ))

@login_required
def overdue_tasks(request):
    tasks = Tasks.objects.filter(
        task_assignments__user=request.user,
        deadline__lt=timezone.now().date(),
        status__in=['To-do', 'In progress', 'Late']
    ).select_related('project')
    
    tasks_with_overdue = [{
        'task': task,
        'days_overdue': (timezone.now().date() - task.deadline).days
    } for task in tasks]
    
    return render(request, 'main/pages/projects/overdue_tasks.html', {
        'tasks_with_overdue': tasks_with_overdue,
        'now': timezone.now().date()
    })

@require_http_methods(["POST"])
@login_required
def extend_deadline(request, task_id):
    """Xử lý yêu cầu gia hạn task"""
    try:
        task = Tasks.objects.get(
            id=task_id,
            task_assignments__user=request.user
        )
        
        new_deadline = request.POST.get('new_deadline')
        reason = request.POST.get('reason', '')
        
        if not new_deadline:
            return JsonResponse(
                {'success': False, 'error': 'Vui lòng chọn ngày gia hạn'},
                status=400
            )
            
        task.deadline = new_deadline
        if task.status == 'Late':
            task.status = 'In progress'
        task.save()
        
        
        return JsonResponse({
            'success': True,
            'new_deadline': task.deadline.strftime('%d/%m/%Y'),
            'new_status': task.status
        })
    
    except ObjectDoesNotExist:
        return JsonResponse(
            {'success': False, 'error': 'Task không tồn tại hoặc không có quyền'},
            status=404
        )
    except Exception as e:
        return JsonResponse(
            {'success': False, 'error': str(e)},
            status=400
        )