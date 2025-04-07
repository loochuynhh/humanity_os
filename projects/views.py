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
from datetime import timedelta
from django.db import models

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

@login_required
def time_tracking(request):
    """Hiển thị trang Time Tracking cho nhân viên"""
    tasks = Tasks.objects.filter(
        task_assignments__user=request.user
    ).select_related('project')

    for task in tasks:
        task.is_tracking = TimeEntries.objects.filter(
            task=task,
            user=request.user,
            end_time__isnull=True
        ).exists()
        task.save()

    time_entries = TimeEntries.objects.filter(
        user=request.user
    ).select_related('task').order_by('-start_time')

    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    total_time_today = TimeEntries.objects.filter(
        user=request.user,
        start_time__date=today
    ).aggregate(total=Sum('duration'))['total'] or 0
    total_time_week = TimeEntries.objects.filter(
        user=request.user,
        start_time__gte=week_start
    ).aggregate(total=Sum('duration'))['total'] or 0
    total_time_month = TimeEntries.objects.filter(
        user=request.user,
        start_time__gte=month_start
    ).aggregate(total=Sum('duration'))['total'] or 0

    def format_time(hours):
        if hours is None:
            return "0h 0m"
        h = int(hours)
        m = int((hours - h) * 60)
        return f"{h}h {m}m"

    context = {
        'tasks': tasks,
        'time_entries': time_entries,
        'total_time_today': format_time(total_time_today),
        'total_time_week': format_time(total_time_week),
        'total_time_month': format_time(total_time_month),
    }
    return render(request, 'main/pages/projects/time_tracking.html', context)

@login_required
def all_projects(request):
    """Hiển thị tất cả dự án"""
    projects = Projects.objects.all()
    context = {
        'projects': projects,
        'today': timezone.now().date(),
    }
    return render(request, 'main/pages/projects/all_projects.html', context)

@login_required
def my_projects(request):
    """Hiển thị dự án của tôi"""
    memberships = TeamProjectMembership.objects.filter(user=request.user).select_related('project')
    for membership in memberships:
        tasks = Tasks.objects.filter(project=membership.project)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status="Completed").count()
        membership.project_progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    context = {
        'memberships': memberships,
    }
    return render(request, 'main/pages/projects/my_projects.html', context)

@login_required
def team_members(request):
    """Hiển thị trang thành viên nhóm"""
    projects = Projects.objects.filter(team_members=request.user)  # Chỉ hiển thị dự án mà user tham gia
    context = {
        'projects': projects,
    }
    return render(request, 'main/pages/projects/team_members.html', context)

@login_required
def team_members_data(request):
    """Trả về dữ liệu thành viên qua AJAX"""
    project_id = request.GET.get('project_id')
    members_data = []
    if project_id:
        project = Projects.objects.get(id=project_id)
        memberships = TeamProjectMembership.objects.filter(project=project).select_related('user')
        for membership in memberships:
            user = membership.user
            task_count = Tasks.objects.filter(task_assignments__user=user, project=project).count()
            total_time = TimeEntries.objects.filter(user=user, task__project=project).aggregate(
                total=models.Sum('duration')
            )['total'] or 0
            total_time_str = f"{int(total_time)}h {int((total_time % 1) * 60)}m"
            members_data.append({
                'name': user.get_full_name(),
                'role': 'Quản lý' if user == project.manager else 'Thành viên',
                'join_date': membership.join_date.strftime('%d/%m/%Y'),
                'task_count': task_count,
                'total_time': total_time_str,
            })
    return JsonResponse({'members': members_data})

@login_required
def project_progress(request):
    """Hiển thị trang thống kê tiến độ"""
    projects = Projects.objects.filter(team_members=request.user) 
    context = {
        'projects': projects,
    }
    return render(request, 'main/pages/projects/project_progress.html', context)

@login_required
def project_progress_data(request):
    """Trả về dữ liệu tiến độ qua AJAX"""
    project_id = request.GET.get('project_id')
    if project_id:
        project = Projects.objects.get(id=project_id)
        tasks = Tasks.objects.filter(project=project)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status="Completed").count()
        task_counts = dict(tasks.values('status').annotate(count=models.Count('status')).values_list('status', 'count'))
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        return JsonResponse({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'progress': round(progress, 1),
            'task_counts': task_counts,
        })
    return JsonResponse({'total_tasks': 0, 'completed_tasks': 0, 'progress': 0, 'task_counts': {}})