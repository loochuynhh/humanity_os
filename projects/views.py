from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Count, Q
import json
from django.views.decorators.http import require_POST, require_http_methods
from .models import Tasks, Projects, TimeEntries, TeamProjectMembership, DeadlineExtensionRequest, TaskAssignments
from .utils import (
    calculate_team_member_data,
    calculate_time_totals,
    filter_tasks,
    get_project_progress,
    get_user_projects,
    check_deadline_warnings,
    calculate_time_by_day,
    calculate_time_by_task,
    get_project_status
)
from datetime import timedelta, datetime

@login_required
def all_projects(request):
    all_projects = Projects.objects.all().prefetch_related('team_members', 'manager')
    my_projects = Projects.objects.filter(Q(team_members=request.user) | Q(manager=request.user)).distinct()
    managed_projects = Projects.objects.filter(manager=request.user).distinct()

    filter_type = request.GET.get('filter', 'all')
    status_filter = request.GET.get('status', 'all')
    sort_by = request.GET.get('sort', 'date-desc')
    search_term = request.GET.get('search', '')

    if filter_type == 'my':
        projects = my_projects
    elif filter_type == 'managed':
        projects = managed_projects
    else:
        projects = all_projects

    if search_term:
        projects = projects.filter(Q(name__icontains=search_term) | Q(description__icontains=search_term))

    projects_with_data = []
    today = timezone.now().date()

    for project in projects:
        progress = get_project_progress(project)
        member_count = project.team_members.count()
        tasks = Tasks.objects.filter(project=project)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='Completed').count()
        in_progress_tasks = tasks.filter(status='In progress').count()
        late_tasks = tasks.filter(status='Late').count()

        status, status_display = get_project_status(project)

        if status_filter != 'all' and status != status_filter:
            continue

        project_data = {
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'start_date': project.start_date,
            'end_date': project.end_date,
            'manager': project.manager,
            'progress': round(progress, 1),
            'member_count': member_count,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'late_tasks': late_tasks,
            'status': status,
            'status_display': status_display,
            'is_member': request.user in project.team_members.all(),
            'is_manager': request.user == project.manager,
            'team_members': project.team_members.all()
        }
        projects_with_data.append(project_data)

    sort_keys = {
        'date-desc': lambda x: x['start_date'],
        'date-asc': lambda x: x['start_date'],
        'alpha-asc': lambda x: x['name'].lower(),
        'alpha-desc': lambda x: x['name'].lower(),
        'progress-asc': lambda x: x['progress'],
        'progress-desc': lambda x: x['progress'],
        'deadline-asc': lambda x: x['end_date'],
        'deadline-desc': lambda x: x['end_date']
    }
    if sort_by in sort_keys:
        projects_with_data.sort(key=sort_keys[sort_by], reverse='desc' in sort_by)

    context = {
        'projects': projects_with_data,
        'filter_type': filter_type,
        'status_filter': status_filter,
        'sort_by': sort_by,
        'search_term': search_term,
        'today': today,
    }
    return render(request, 'main/pages/projects/all_projects.html', context)

@login_required
def project_detail(request, project_id):
    try:
        project = get_object_or_404(Projects.objects.prefetch_related('team_members', 'manager', 'tasks__task_assignments__user'), id=project_id)
        is_member = request.user in project.team_members.all()
        is_manager = request.user == project.manager

        if not is_member and not is_manager and not request.user.is_superuser:
            return JsonResponse({'success': False, 'error': 'Bạn không có quyền xem dự án này'}, status=403)

        members = []
        for user in project.team_members.all():
            assignments = TaskAssignments.objects.filter(task__project=project, user=user)
            user_tasks = Tasks.objects.filter(task_assignments__in=assignments).distinct()
            user_completed = assignments.filter(status='Completed').count()
            user_time = assignments.aggregate(total=Sum('actual_time'))['total'] or 0

            members.append({
                'id': user.id,
                'name': f"{user.first_name} {user.last_name}",
                'email': user.email,
                'role': 'Quản lý' if user == project.manager else assignments.first().role if assignments.exists() else 'Thành viên',
                'tasks_count': user_tasks.count(),
                'completed_tasks': user_completed,
                'total_time': round(user_time, 2)
            })

        tasks = []
        for task in project.tasks.all():
            assignees = task.task_assignments.all()
            assignee_info = [{'name': f"{a.user.first_name} {a.user.last_name}", 'role': a.role} for a in assignees]
            tasks.append({
                'id': task.id,
                'title': task.title,
                'status': task.status,
                'deadline': task.deadline,
                'assignees': assignee_info,
                'assignee_count': len(assignee_info)
            })

        total_tasks = project.tasks.count()
        completed_tasks = project.tasks.filter(status='Completed').count()
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        status, status_display = get_project_status(project)
        task_statuses = dict(project.tasks.values('status').annotate(count=Count('status')).values_list('status', 'count'))

        return JsonResponse({
            'success': True,
            'project': {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'start_date': project.start_date.strftime('%d/%m/%Y'),
                'end_date': project.end_date.strftime('%d/%m/%Y'),
                'manager': {
                    'id': project.manager.id if project.manager else None,
                    'name': f"{project.manager.first_name} {project.manager.last_name}" if project.manager else 'Chưa phân công'
                },
                'status': status,
                'status_display': status_display,
                'progress': round(progress, 1),
                'member_count': project.team_members.count(),
                'task_count': total_tasks,
                'completed_tasks': completed_tasks
            },
            'members': members,
            'tasks': tasks,
            'task_statuses': task_statuses,
            'is_member': is_member,
            'is_manager': is_manager
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def team_members_data(request):
    project_id = request.GET.get('project_id')
    members_data = calculate_team_member_data(project_id) if project_id else []
    return JsonResponse({'members': members_data})

@login_required
def project_progress(request):
    projects = get_user_projects(request.user)
    context = {'projects': projects}
    return render(request, 'main/pages/projects/project_progress.html', context)

@login_required
def project_progress_data(request):
    project_id = request.GET.get('project_id')
    if not project_id:
        return JsonResponse({'success': False, 'error': 'Thiếu project_id'}, status=400)
    try:
        project = Projects.objects.get(id=project_id)
        tasks = project.tasks.all()
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='Completed').count()
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        task_counts = dict(tasks.values('status').annotate(count=Count('status')).values_list('status', 'count'))
        return JsonResponse({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'progress': round(progress, 1),
            'task_counts': task_counts
        })
    except Projects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Dự án không tồn tại'}, status=404)

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
    assignments = TaskAssignments.objects.filter(user=request.user).select_related('task__project', 'user')
    tasks_with_details = []
    for assignment in assignments:
        task = assignment.task
        warning = check_deadline_warnings(task)
        time_entries = TimeEntries.objects.filter(task_assignment=assignment).order_by('-start_time')[:5]
        progress_percentage = (assignment.actual_time / assignment.estimated_time * 100) if assignment.estimated_time and assignment.estimated_time > 0 else 0
        progress_percentage = min(100, max(0, round(progress_percentage)))
        tasks_with_details.append({
            'task': task,
            'warning': warning,
            'time_entries': time_entries,
            'progress_percentage': progress_percentage,
            'task_assignment': assignment,
        })
    projects = Projects.objects.filter(tasks__task_assignments__user=request.user).distinct()
    return render(request, 'main/pages/projects/my_tasks.html', {
        'tasks_with_details': tasks_with_details,
        'status_choices': Tasks.STATUS_CHOICES,
        'difficulty_choices': Tasks.DIFFICULTY_CHOICES,
        'now': timezone.now().date(),
        'projects': projects,
    })

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Tasks.objects.select_related('project').prefetch_related('task_assignments__user', 'task_assignments__time_entries'), id=task_id)
    if not task.task_assignments.filter(user=request.user).exists() and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Bạn không có quyền xem task này'}, status=403)
    
    task.update_total_time()
    task.update_start_date()
    progress_percentage = (task.total_time / task.estimated_time * 100) if task.estimated_time and task.estimated_time > 0 else 0
    progress_percentage = min(100, max(0, round(progress_percentage)))

    assignment = task.task_assignments.filter(user=request.user).first()
    time_entries = TimeEntries.objects.filter(task_assignment__task=task).select_related('task_assignment__user').order_by('-start_time')

    context = {
        'task': task,
        'progress_percentage': progress_percentage,
        'status_choices': Tasks.STATUS_CHOICES,
        'difficulty_choices': Tasks.DIFFICULTY_CHOICES,
        'task_assignments': task.task_assignments.all(),
        'task_assignment': assignment,
        'time_entries': time_entries,
    }
    return render(request, 'main/pages/projects/task_detail.html', context)

@require_POST
@login_required
def update_status(request):
    try:
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')
        assignment = TaskAssignments.objects.get(task_id=task_id, user=request.user)
        if status not in dict(Tasks.STATUS_CHOICES):
            return JsonResponse({'success': False, 'error': 'Trạng thái không hợp lệ'}, status=400)
        
        assignment.status = status
        if task.deadline.date() < timezone.now().date() and status != "Completed":
            assignment.status = "Late"
        assignment.save()
        assignment.task.update_status_from_assignments()
        return JsonResponse({
            'success': True,
            'new_status': assignment.status
        })
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task assignment không tồn tại hoặc không có quyền'}, status=404)
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
        
        assignment = TaskAssignments.objects.get(task_id=task_id, user=request.user)
        task = assignment.task

        if action == 'start':
            active_entries = TimeEntries.objects.filter(task_assignment__user=request.user, end_time__isnull=True)
            if active_entries.exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Bạn đang tracking một task khác. Hãy dừng nó trước.'
                }, status=400)
            
            time_entry = TimeEntries.objects.create(
                task_assignment=assignment,
                start_time=timezone.now()
            )
            task.is_tracking = True
            task.update_start_date()
            if assignment.status == "To-do":
                assignment.status = "In progress"
                assignment.save()
                task.update_status_from_assignments()
            task.save()
            return JsonResponse({
                'success': True,
                'action': 'started',
                'entry_id': time_entry.id
            })
            
        elif action == 'stop':
            entry = TimeEntries.objects.get(task_assignment=assignment, end_time__isnull=True)
            entry.end_time = timezone.now()
            entry.save()
            assignment.update_actual_time()
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
        task = Tasks.objects.get(id=task_id)
        if not task.task_assignments.filter(user=request.user).exists() and not request.user.is_superuser:
            return JsonResponse({'success': False, 'error': 'Bạn không có quyền chỉnh sửa task này'}, status=403)
        
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.difficulty = request.POST.get('difficulty', task.difficulty)
        task.github_link = request.POST.get('github_link', task.github_link)
        task.notes = request.POST.get('notes', task.notes)

        assignment = task.task_assignments.filter(user=request.user).first()
        if assignment:
            estimated_time = request.POST.get(f'estimated_time_{assignment.user.id}')
            if estimated_time:
                assignment.estimated_time = float(estimated_time)
                assignment.save()

        task.save()
        return JsonResponse({'success': True, 'message': 'Cập nhật task thành công!'})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task không tồn tại'}, status=404)
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
        
        task = Tasks.objects.get(id=task_id)
        if not task.task_assignments.filter(user=request.user).exists():
            return JsonResponse({'success': False, 'error': 'Bạn không được gán cho task này'}, status=403)
        
        DeadlineExtensionRequest.objects.create(
            task=task,
            requested_by=request.user,
            requested_deadline=timezone.make_aware(datetime.fromisoformat(requested_deadline.replace('T', ' '))),
            reason=reason
        )
        return JsonResponse({'success': True, 'message': 'Yêu cầu gia hạn đã được gửi!'})
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task không tồn tại'}, status=404)
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Ngày không hợp lệ'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_POST
@login_required
def extend_deadline(request, task_id):
    try:
        task = Tasks.objects.get(id=task_id)
        if not task.project.manager == request.user and not request.user.is_superuser:
            return JsonResponse({'success': False, 'error': 'Chỉ quản lý hoặc admin có thể gia hạn deadline'}, status=403)
        
        new_deadline = request.POST.get('new_deadline')
        if not new_deadline:
            return JsonResponse({'success': False, 'error': 'Vui lòng chọn ngày gia hạn'}, status=400)
        
        task.deadline = timezone.make_aware(datetime.fromisoformat(new_deadline.replace('T', ' ')))
        task.save()
        task.update_status_from_assignments()
        return JsonResponse({
            'success': True,
            'new_deadline': task.deadline.strftime('%d/%m/%Y'),
            'new_status': task.status
        })
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task không tồn tại'}, status=404)
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Ngày không hợp lệ'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def time_tracking(request):
    assignments = TaskAssignments.objects.filter(user=request.user).select_related('task__project')
    time_entries = TimeEntries.objects.filter(task_assignment__in=assignments).select_related('task_assignment__task').order_by('-start_time')
    time_totals = calculate_time_totals(request.user)
    time_by_day = calculate_time_by_day(request.user)
    time_by_task = calculate_time_by_task(request.user)

    context = {
        'time_entries': time_entries,
        'total_time_today': time_totals['today'],
        'total_time_week': time_totals['week'],
        'total_time_month': time_totals['month'],
        'time_by_day': json.dumps(time_by_day),  # Serialize to JSON string
        'time_by_task': json.dumps(time_by_task),  # Serialize to JSON string
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

        entry = TimeEntries.objects.get(id=entry_id, task_assignment__user=request.user)
        entry.start_time = timezone.make_aware(datetime.fromisoformat(start_time.replace('T', ' ')))
        entry.end_time = timezone.make_aware(datetime.fromisoformat(end_time.replace('T', ' '))) if end_time else None
        entry.save()
        entry.task_assignment.update_actual_time()

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
        assignment.task.update_status_from_assignments()
        return JsonResponse({
            'success': True,
            'message': 'Cập nhật trạng thái thành công!'
        })
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'Task assignment không tồn tại hoặc không có quyền'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def project_calendar(request):
    user_projects = get_user_projects(request.user)
    context = {
        'projects': user_projects,
        'current_month': timezone.now().month,
        'current_year': timezone.now().year
    }
    return render(request, 'main/pages/projects/project_calendar.html', context)

@login_required
def project_calendar_events(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    project_id = request.GET.get('project_id')

    try:
        start_date = timezone.make_aware(datetime.fromisoformat(start_date.replace('Z', '')))
        end_date = timezone.make_aware(datetime.fromisoformat(end_date.replace('Z', '')))
    except (ValueError, TypeError):
        today = timezone.now()
        start_date = timezone.datetime(today.year, today.month, 1)
        end_date = start_date + timedelta(days=31)

    projects = get_user_projects(request.user)
    if project_id:
        projects = projects.filter(id=project_id)

    tasks = Tasks.objects.filter(project__in=projects, deadline__range=(start_date, end_date))
    events = []
    for task in tasks:
        events.append({
            'id': f'task_{task.id}',
            'title': f'Deadline: {task.title}',
            'start': task.deadline.isoformat(),
            'end': task.deadline.isoformat(),
            'backgroundColor': '#dc3545',
            'borderColor': '#dc3545',
            'textColor': '#ffffff',
            'url': f'/projects/tasks/{task.id}/',
            'extendedProps': {
                'type': 'task',
                'project': task.project.name,
                'description': task.description[:100] + '...' if len(task.description) > 100 else task.description,
                'status': task.status
            }
        })

    for project in projects:
        if project.start_date:
            events.append({
                'id': f'project_start_{project.id}',
                'title': f'Bắt đầu: {project.name}',
                'start': project.start_date.isoformat(),
                'backgroundColor': '#28a745',
                'borderColor': '#28a745',
                'textColor': '#ffffff',
                'extendedProps': {
                    'type': 'project',
                    'project': project.name,
                    'description': f'Ngày bắt đầu dự án {project.name}'
                }
            })
        if project.end_date:
            events.append({
                'id': f'project_end_{project.id}',
                'title': f'Kết thúc: {project.name}',
                'start': project.end_date.isoformat(),
                'backgroundColor': '#ffc107',
                'borderColor': '#ffc107',
                'textColor': '#000000',
                'extendedProps': {
                    'type': 'project',
                    'project': project.name,
                    'description': f'Ngày kết thúc dự án {project.name}'
                }
            })

    return JsonResponse({'events': events}, safe=False)

@login_required
def project_statistics(request):
    user_projects = get_user_projects(request.user)
    context = {'projects': user_projects, 'today': timezone.now().date()}
    return render(request, 'main/pages/projects/project_statistics.html', context)

@login_required
def project_statistics_data(request):
    project_id = request.GET.get('project_id')
    if not project_id:
        return JsonResponse({'success': False, 'error': 'Thiếu project_id'}, status=400)

    try:
        project = Projects.objects.get(id=project_id)
        today = timezone.now().date()
        tasks = project.tasks.all()
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='Completed').count()
        in_progress_tasks = tasks.filter(status='In progress').count()
        late_tasks = tasks.filter(status='Late').count()
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        status = get_project_status(project)[0]
        total_time = TaskAssignments.objects.filter(task__project=project).aggregate(total=Sum('actual_time'))['total'] or 0

        user_statistics = []
        memberships = TeamProjectMembership.objects.filter(project=project).select_related('user')
        for membership in memberships:
            user = membership.user
            assignments = TaskAssignments.objects.filter(task__project=project, user=user)
            user_tasks = tasks.filter(task_assignments__in=assignments).distinct()
            user_time = assignments.aggregate(total=Sum('actual_time'))['total'] or 0
            user_completed = assignments.filter(status='Completed').count()
            user_progress = (user_completed / assignments.count() * 100) if assignments.count() > 0 else 0

            user_statistics.append({
                'user_id': user.id,
                'user_name': f"{user.first_name} {user.last_name}",
                'role': 'Quản lý' if user == project.manager else assignments.first().role if assignments.exists() else 'Thành viên',
                'tasks_count': user_tasks.count(),
                'completed_tasks': user_completed,
                'total_time': round(user_time, 2),
                'progress': round(user_progress, 1)
            })

        task_status_distribution = {
            'Completed': completed_tasks,
            'In progress': in_progress_tasks,
            'Late': late_tasks,
            'To-do': total_tasks - completed_tasks - in_progress_tasks - late_tasks
        }

        month_start = today.replace(day=1)
        tasks_by_date = {}
        for i in range(31):
            date = month_start + timedelta(days=i)
            if date > today:
                break
            completed_by_date = tasks.filter(status='Completed', completed_date__date__lte=date).count()
            progress_by_date = (completed_by_date / total_tasks * 100) if total_tasks > 0 else 0
            tasks_by_date[date.strftime('%d/%m')] = round(progress_by_date, 1)

        return JsonResponse({
            'success': True,
            'project_name': project.name,
            'project_description': project.description,
            'start_date': project.start_date.strftime('%d/%m/%Y'),
            'end_date': project.end_date.strftime('%d/%m/%Y'),
            'status': status,
            'progress': round(progress, 1),
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'late_tasks': late_tasks,
            'total_time': round(total_time, 2),
            'task_status_distribution': task_status_distribution,
            'user_statistics': user_statistics,
            'progress_by_date': tasks_by_date
        })
    except Projects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Dự án không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)