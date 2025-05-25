from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Count, Q
import json
from django.views.decorators.http import require_POST
from .models import Tasks, Projects, TimeEntries, TeamProjectMembership, DeadlineExtensionRequest, TaskAssignments
from datetime import timedelta, datetime
from kpis.models import EmployeeKPIs
from users.models import CheckInCheckOut
import google.generativeai as genai
from django.conf import settings
from django.db.models import Avg
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
        'assignments': assignments
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

    events = []

    time_entries = TimeEntries.objects.filter(
        task_assignment__user=request.user,
        task_assignment__task__project__in=projects,
        start_time__range=(start_date, end_date)
    ).select_related('task_assignment__task', 'task_assignment__user')


    for entry in time_entries:
        task = entry.task_assignment.task
        user = entry.task_assignment.user
        local_tz = timezone.get_current_timezone()
        
        start_time = entry.start_time.astimezone(local_tz)
        end_time = entry.end_time.astimezone(local_tz) if entry.end_time else None

        events.append({
            'id': f'time_entry_{entry.id}',
            'title': task.title,
            'start': start_time.isoformat(),
            'end': end_time.isoformat() if end_time else None,
            'backgroundColor': 'rgba(13, 110, 253, 0.2)',
            'borderColor': '#0d6efd',
            'textColor': '#0d6efd',
            'extendedProps': {
                'type': 'time_entry',
                'project': task.project.name,
                'task_id': task.id,
                'task_title': task.title,
                'user': f'{user.first_name} {user.last_name}',
                'duration': entry.duration or 0,
                'start_time_formatted': start_time.strftime('%H:%M'),
                'end_time_formatted': end_time.strftime('%H:%M') if end_time else 'Đang thực hiện',
                'role': entry.task_assignment.role
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
    

@login_required
def create_time_entry(request):
    if request.method == 'POST':
        task_assignment_id = request.POST.get('task_assignment')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')

        try:
            task_assignment = TaskAssignments.objects.get(id=task_assignment_id, user=request.user)
        except TaskAssignments.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task không hợp lệ hoặc bạn không có quyền!'}, status=403)

        try:
            start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
            start_time = timezone.make_aware(start_time)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Thời gian bắt đầu không hợp lệ!'})

        end_time = None
        if end_time_str:
            try:
                end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
                end_time = timezone.make_aware(end_time)
                if end_time <= start_time:
                    return JsonResponse({'success': False, 'error': 'Thời gian kết thúc phải sau thời gian bắt đầu!'})
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Thời gian kết thúc không hợp lệ!'})

        time_entry = TimeEntries.objects.create(
            task_assignment=task_assignment,
            start_time=start_time,
            end_time=end_time
        )

        return JsonResponse({'success': True, 'id': time_entry.id})
    return JsonResponse({'success': False, 'error': 'Yêu cầu không hợp lệ!'}, status=400)

@login_required
@require_POST
def suggest_user_for_task(request):
    """
    API endpoint để đề xuất người dùng phù hợp cho một task
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Yêu cầu đăng nhập.'}, status=401)
    
    try:
        # Đọc dữ liệu từ JSON body thay vì form data
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
        except json.JSONDecodeError:
            # Fallback cho form data nếu không phải JSON
            task_id = request.POST.get('task_id')
        
        if not task_id:
            return JsonResponse({'error': 'Thiếu task_id trong yêu cầu.'}, status=400)
        
        task = Tasks.objects.get(id=task_id)
        project = task.project
        
        if not project:
            return JsonResponse({'error': 'Task không thuộc dự án nào.'}, status=400)
        
        # Lấy danh sách thành viên trong dự án
        team_members = project.team_members.all()
        
        if not team_members.exists():
            return JsonResponse({'error': 'Không có thành viên nào trong dự án.'}, status=400)
            
        # Thu thập thông tin chi tiết cho AI gợi ý
        ai_suggestion_prompt = build_ai_suggestion_prompt(task, project, team_members)
        
        # Gọi AI để đề xuất người dùng phù hợp
        suggestion_result = get_ai_suggestion(ai_suggestion_prompt)
        
        if not suggestion_result:
            return JsonResponse({'error': 'Không thể lấy đề xuất từ AI.'}, status=500)
        
        return JsonResponse(suggestion_result)
        
    except Tasks.DoesNotExist:
        return JsonResponse({'error': 'Không tìm thấy task.'}, status=404)
    except Exception as e:
        import traceback
        print(f"Lỗi trong suggest_user_for_task: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'error': f'Đã xảy ra lỗi: {str(e)}'}, status=500)


def build_ai_suggestion_prompt(task, project, team_members):
    """
    Xây dựng prompt cho AI để đề xuất người dùng phù hợp
    """
    today = timezone.now().date()
    one_month_ago = today - timezone.timedelta(days=30)
    
    # Tạo thông tin chi tiết về task
    task_info = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'deadline': task.deadline.strftime('%Y-%m-%d %H:%M') if task.deadline else 'Chưa có deadline',
        'status': task.status,
        'difficulty': task.difficulty,
        'estimated_time': f"{task.estimated_time} giờ" if task.estimated_time else 'Chưa ước tính',
        'github_link': task.github_link,
        'notes': task.notes,
        'start_date': task.start_date.strftime('%Y-%m-%d %H:%M') if task.start_date else 'Chưa bắt đầu',
    }
    
    # Tạo thông tin chi tiết về dự án
    project_info = {
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'start_date': project.start_date.strftime('%Y-%m-%d %H:%M'),
        'end_date': project.end_date.strftime('%Y-%m-%d %H:%M'),
        'manager': project.manager.get_full_name() if project.manager else 'Chưa có quản lý',
        'total_team_members': project.team_members.count(),
    }
    
    # Thu thập thông tin về tất cả thành viên trong dự án
    members_data = []
    
    for user in team_members:
        # Thông tin cơ bản
        user_data = {
            'id': user.id,
            'username': user.username,
            'full_name': user.get_full_name() or user.username,
            'role': user.role,
            'department': user.department or 'Chưa xác định',
            'status': user.status,
            'date_of_joining': user.date_of_joining.strftime('%Y-%m-%d') if user.date_of_joining else 'Không có thông tin',
        }
        
        # Thông tin công việc hiện tại
        current_tasks = Tasks.objects.filter(
            task_assignments__user=user, 
            status__in=['To-do', 'In progress']
        ).count()
        
        user_data['current_tasks_count'] = current_tasks
        
        # Thống kê công việc đã hoàn thành trong 1 tháng qua
        completed_tasks = Tasks.objects.filter(
            task_assignments__user=user,
            status='Completed',
            completed_date__gte=one_month_ago
        ).count()
        
        user_data['completed_tasks_last_month'] = completed_tasks
        
        # Thời gian làm việc theo dõi trong 1 tuần qua
        week_start = today - timezone.timedelta(days=today.weekday())
        time_entries = TimeEntries.objects.filter(
            task_assignment__user=user,
            start_time__gte=week_start
        )
        
        total_hours = time_entries.aggregate(total=Sum('duration'))['total'] or 0
        user_data['hours_worked_this_week'] = round(total_hours, 2)
        
        # Điểm danh hôm nay
        attendance_today = CheckInCheckOut.objects.filter(
            user=user, 
            date=today
        ).first()
        
        user_data['checked_in_today'] = attendance_today is not None and attendance_today.checkin_time is not None
        
        # KPI và đánh giá
        user_kpis = EmployeeKPIs.objects.filter(user=user)
        avg_kpi = user_kpis.aggregate(avg=Avg('achieved_percentage'))['avg'] or 0
        
        user_data['avg_kpi_percentage'] = round(avg_kpi, 2)
        
        # Đánh giá năng lực dựa trên công việc tương tự
        similar_tasks = Tasks.objects.filter(
            Q(difficulty=task.difficulty) |
            Q(title__icontains=task.title) |
            Q(description__icontains=task.description)
        )
        
        similar_task_performance = TaskAssignments.objects.filter(
            user=user,
            task__in=similar_tasks,
            status='Completed'
        ).count()
        
        user_data['similar_tasks_completed'] = similar_task_performance
        
        # Tổng hợp
        members_data.append(user_data)
    
    # Xây dựng prompt
    prompt = f"""
Tôi cần bạn đề xuất người dùng phù hợp nhất để gán cho một nhiệm vụ trong dự án, dựa trên dữ liệu chi tiết về người dùng và yêu cầu nhiệm vụ. Vai trò của bạn là một trợ lý AI chuyên nghiệp về phân bổ nguồn lực dự án.

## Thông tin Nhiệm vụ (Task)
- **ID**: {task_info['id']}
- **Tiêu đề**: {task_info['title']}
- **Mô tả**: {task_info['description']}
- **Deadline**: {task_info['deadline']}
- **Độ khó**: {task_info['difficulty']}
- **Thời gian ước tính**: {task_info['estimated_time']}
- **Ghi chú**: {task_info['notes'] or 'Không có'}

## Thông tin Dự án
- **Tên**: {project_info['name']}
- **Mô tả**: {project_info['description']}
- **Thời gian**: {project_info['start_date']} đến {project_info['end_date']}
- **Quản lý**: {project_info['manager']}
- **Số thành viên**: {project_info['total_team_members']}

## Thông tin các thành viên trong dự án
{json.dumps(members_data, indent=2, ensure_ascii=False)}

## Yêu cầu
1. Phân tích thông tin của tất cả thành viên và chọn ra người phù hợp nhất để thực hiện nhiệm vụ này.
2. Cân nhắc các yếu tố sau:
   - Kinh nghiệm với các nhiệm vụ tương tự (similar_tasks_completed)
   - Tải công việc hiện tại (current_tasks_count)
   - Hiệu suất KPI (avg_kpi_percentage)
   - Sự có mặt hôm nay (checked_in_today)
   - Hoạt động gần đây (completed_tasks_last_month)
   - Phù hợp với độ khó của nhiệm vụ
   - Khả năng hoàn thành công việc đúng deadline

3. Trả về JSON với định dạng sau:
{{
  "suggested_user_id": [id người dùng được đề xuất],
  "suggested_user_name": "[tên đầy đủ hoặc username của người dùng được đề xuất]",
  "reasoning": "[phân tích chi tiết dưới dạng HTML với định dạng ul/li, bao gồm hết các điểm sau:]
    <ul>
      <li><strong>Lý do chọn người này:</strong> [Phân tích ưu điểm chính của người được chọn, tối thiểu 3 lý do]</li>
      <li><strong>Về kinh nghiệm:</strong> [Chi tiết về kinh nghiệm liên quan của họ]</li>
      <li><strong>Về tình trạng hiện tại:</strong> [Thông tin về tải công việc hiện tại, điểm danh hôm nay]</li>
      <li><strong>So sánh với các ứng viên tiềm năng:</strong> [So sánh với 2 ứng viên tiềm năng khác, phân tích tại sao họ không được chọn]</li>
      <li><strong>Khuyến nghị phân công:</strong> [Đề xuất thêm về cách phân công tối ưu]</li>
    </ul>"
}}

QUAN TRỌNG: Phản hồi của bạn PHẢI LÀ MỘT JSON HỢP LỆ có thể phân tích cú pháp bởi Python, không có bất kỳ ký tự markdown, tag, hoặc chú thích nào khác. Không thêm các ký tự "```json" hoặc "```" vào đầu và cuối.
"""
    
    return prompt


def get_ai_suggestion(prompt):
    """
    Gọi API Gemini để lấy đề xuất người dùng phù hợp
    """
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Cấu hình parameters
        generation_config = {
            "temperature": 0.1,  # Giảm temperature để có kết quả nhất quán hơn
            "top_p": 0.8,
            "top_k": 16,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",  # Yêu cầu phản hồi dạng JSON
        }
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Lấy phản hồi dạng văn bản
        response_text = response.text
        
        # Xử lý phản hồi để loại bỏ các tag markdown và làm sạch JSON
        # Loại bỏ ```json hoặc ``` hoặc kí tự không cần thiết từ đầu và cuối
        cleaned_response = response_text.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:]
        elif cleaned_response.startswith('```'):
            cleaned_response = cleaned_response[3:]
            
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]
            
        cleaned_response = cleaned_response.strip()
        
        # Log phản hồi cho debugging
        print(f"Response từ AI (đã làm sạch): {cleaned_response[:100]}...")
        
        # Parse JSON từ kết quả trả về
        try:
            suggestion = json.loads(cleaned_response)
            
            # Kiểm tra định dạng phản hồi
            if not isinstance(suggestion, dict) or 'suggested_user_id' not in suggestion:
                raise ValueError("Phản hồi từ AI không đúng định dạng JSON")
                
            return suggestion
            
        except json.JSONDecodeError as e:
            print(f"Lỗi khi phân tích JSON từ phản hồi AI: {str(e)}")
            print(f"Phản hồi gốc: {response_text}")
            # Thử phân tích lại sau khi làm sạch triệt để hơn
            try:
                # Tìm vị trí bắt đầu của JSON (tìm dấu { đầu tiên)
                start_pos = response_text.find('{')
                # Tìm vị trí kết thúc của JSON (tìm dấu } cuối cùng)
                end_pos = response_text.rfind('}') + 1
                
                if start_pos >= 0 and end_pos > start_pos:
                    json_content = response_text[start_pos:end_pos]
                    suggestion = json.loads(json_content)
                    
                    # Kiểm tra định dạng phản hồi
                    if not isinstance(suggestion, dict) or 'suggested_user_id' not in suggestion:
                        raise ValueError("Phản hồi từ AI không đúng định dạng JSON")
                        
                    return suggestion
            except:
                # Nếu tất cả cách khác đều thất bại, thử cung cấp một phản hồi phòng hờ
                return {
                    'suggested_user_id': None,
                    'suggested_user_name': 'Không thể đề xuất',
                    'reasoning': '<ul><li>Không thể phân tích phản hồi từ AI</li><li>Vui lòng thử lại hoặc chọn thủ công</li></ul>'
                }
            
            return None
            
    except Exception as e:
        import traceback
        print(f"Lỗi khi gọi API Gemini: {str(e)}")
        print(traceback.format_exc())
        return None