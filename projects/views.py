# projects/views.py
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Count
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
from datetime import timedelta, datetime


@login_required
def all_projects(request):
    # Lấy tất cả dự án, cả dự án người dùng tham gia và tất cả dự án
    all_projects = Projects.objects.all().prefetch_related('team_members')
    my_projects = Projects.objects.filter(team_members=request.user).distinct()
    managed_projects = Projects.objects.filter(manager=request.user).distinct()

    # Lấy filter từ query params
    filter_type = request.GET.get('filter', 'all')
    status_filter = request.GET.get('status', 'all')
    sort_by = request.GET.get('sort', 'date-desc')
    search_term = request.GET.get('search', '')

    # Áp dụng filter theo loại dự án
    if filter_type == 'my':
        projects = my_projects
    elif filter_type == 'managed':
        projects = managed_projects
    else:
        projects = all_projects

    # Áp dụng tìm kiếm nếu có
    if search_term:
        projects = projects.filter(name__icontains=search_term) | projects.filter(description__icontains=search_term)

    # Tính toán tiến độ cho mỗi dự án
    projects_with_data = []
    today = timezone.now().date()

    for project in projects:
        # Tính toán tiến độ
        progress = get_project_progress(project)

        # Đếm số thành viên
        member_count = project.team_members.count()

        # Lấy các task của dự án
        tasks = Tasks.objects.filter(project=project)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='Completed').count()
        in_progress_tasks = tasks.filter(status='In Progress').count()
        late_tasks = tasks.filter(status='Late').count()

        # Xác định trạng thái dự án
        if total_tasks > 0 and completed_tasks == total_tasks:
            status = 'completed'
        elif project.end_date.date() < today and (total_tasks == 0 or completed_tasks < total_tasks):
            status = 'delayed'
        else:
            # Kiểm tra xem có task nào đang tạm dừng không
            paused_tasks = tasks.filter(status='Paused').count()
            if paused_tasks > 0 and paused_tasks == total_tasks:
                status = 'paused'
            else:
                status = 'active'

        # Lọc theo trạng thái
        if status_filter != 'all' and status != status_filter:
            continue

        # Tạo đối tượng dự án với dữ liệu bổ sung
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
            'status_display': 'Hoàn thành' if status == 'completed' else 'Trễ hạn' if status == 'delayed' else 'Tạm dừng' if status == 'paused' else 'Đang thực hiện',
            'is_member': request.user in project.team_members.all(),
            'is_manager': request.user == project.manager,
            'team_members': project.team_members.all()
        }

        projects_with_data.append(project_data)

    # Sắp xếp dự án theo các tiêu chí
    if sort_by == 'date-desc':
        projects_with_data = sorted(projects_with_data, key=lambda x: x['start_date'], reverse=True)
    elif sort_by == 'date-asc':
        projects_with_data = sorted(projects_with_data, key=lambda x: x['start_date'])
    elif sort_by == 'alpha-asc':
        projects_with_data = sorted(projects_with_data, key=lambda x: x['name'])
    elif sort_by == 'alpha-desc':
        projects_with_data = sorted(projects_with_data, key=lambda x: x['name'], reverse=True)
    elif sort_by == 'progress-asc':
        projects_with_data = sorted(projects_with_data, key=lambda x: x['progress'])
    elif sort_by == 'progress-desc':
        projects_with_data = sorted(projects_with_data, key=lambda x: x['progress'], reverse=True)
    elif sort_by == 'deadline-asc':
        projects_with_data = sorted(projects_with_data, key=lambda x: x['end_date'])
    elif sort_by == 'deadline-desc':
        projects_with_data = sorted(projects_with_data, key=lambda x: x['end_date'], reverse=True)

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
    # Lấy danh sách dự án duy nhất
    projects = Projects.objects.filter(tasks__task_assignments__user=request.user).distinct()
    return render(request, 'main/pages/projects/my_tasks.html', {
        'tasks_with_details': tasks_with_details,
        'status_choices': Tasks.STATUS_CHOICES,
        'difficulty_choices': Tasks.DIFFICULTY_CHOICES,
        'now': timezone.now().date(),
        'projects': projects,  # Thêm projects vào context
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
        if task.deadline.date() < timezone.now().date() and status != "Completed":
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
        entry.start_time = timezone.make_aware(datetime.fromisoformat(start_time.replace('T', ' ')))
        if end_time:
            entry.end_time = timezone.make_aware(datetime.fromisoformat(end_time.replace('T', ' ')))
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

@login_required
def project_calendar(request):
    """
    Hiển thị lịch dự án với các sự kiện từ các dự án và task
    """
    # Lấy danh sách dự án của người dùng để hiển thị bộ lọc
    user_projects = get_user_projects(request.user)

    context = {
        'projects': user_projects,
        'current_month': timezone.now().month,
        'current_year': timezone.now().year
    }

    return render(request, 'main/pages/projects/project_calendar.html', context)


@login_required
def project_calendar_events(request):
    """
    API trả về dữ liệu sự kiện lịch dự án dưới dạng JSON
    """
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    project_id = request.GET.get('project_id')

    # Chuyển đổi string date thành datetime
    if start_date and end_date:
        try:
            start_date = timezone.datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            end_date = timezone.datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Định dạng ngày không hợp lệ'}, status=400)

    # Lọc dự án nếu có project_id
    projects = get_user_projects(request.user)
    if project_id:
        projects = projects.filter(id=project_id)

    # Lấy các task trong khoảng thời gian
    tasks = Tasks.objects.filter(project__in=projects)
    if start_date and end_date:
        tasks = tasks.filter(deadline__range=(start_date, end_date))

    # Định dạng dữ liệu sự kiện
    events = []
    for task in tasks:
        # Thêm deadline task
        events.append({
            'id': f'task_{task.id}',
            'title': f'Deadline: {task.title}',
            'start': task.deadline.isoformat(),
            'end': task.deadline.isoformat(),
            'backgroundColor': '#dc3545',  # Màu đỏ cho deadline
            'borderColor': '#dc3545',
            'textColor': '#ffffff',
            'url': f'/projects/tasks/{task.id}/',
            'extendedProps': {
                'type': 'task',
                'project': task.project.name
            }
        })

    # Thêm ngày bắt đầu và kết thúc dự án
    for project in projects:
        if project.start_date:
            events.append({
                'id': f'project_start_{project.id}',
                'title': f'Bắt đầu: {project.name}',
                'start': project.start_date.isoformat(),
                'backgroundColor': '#28a745',  # Màu xanh cho ngày bắt đầu
                'borderColor': '#28a745',
                'textColor': '#ffffff',
                'extendedProps': {
                    'type': 'project',
                    'project': project.name
                }
            })

        if project.end_date:
            events.append({
                'id': f'project_end_{project.id}',
                'title': f'Kết thúc: {project.name}',
                'start': project.end_date.isoformat(),
                'backgroundColor': '#ffc107',  # Màu vàng cho ngày kết thúc
                'borderColor': '#ffc107',
                'textColor': '#000000',
                'extendedProps': {
                    'type': 'project',
                    'project': project.name
                }
            })

    return JsonResponse(events, safe=False)


@login_required
def project_statistics(request):
    """
    Hiển thị trang thống kê và tiến độ dự án
    """
    # Lấy danh sách dự án của người dùng để hiển thị bộ lọc
    user_projects = get_user_projects(request.user)

    context = {
        'projects': user_projects,
        'today': timezone.now().date()
    }

    return render(request, 'main/pages/projects/project_statistics.html', context)


@login_required
def project_statistics_data(request):
    """
    API trả về dữ liệu thống kê và tiến độ dự án dưới dạng JSON
    """
    project_id = request.GET.get('project_id')
    if not project_id:
        return JsonResponse({'success': False, 'error': 'Thiếu project_id'}, status=400)

    try:
        project = Projects.objects.get(id=project_id)
        today = timezone.now().date()

        # Lấy thống kê về task
        tasks = Tasks.objects.filter(project=project)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='Completed').count()
        in_progress_tasks = tasks.filter(status='In progress').count()
        late_tasks = tasks.filter(status='Late').count()

        # Tính tiến độ
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Xác định trạng thái dự án
        status = 'In progress'
        if completed_tasks == total_tasks and total_tasks > 0:
            status = 'Completed'
        elif project.end_date.date() < today:
            status = 'Late'

        # Tính tổng thời gian làm việc
        time_entries = TimeEntries.objects.filter(task__project=project)
        total_time = time_entries.aggregate(total=Sum('duration'))['total'] or 0

        # Thống kê theo người dùng
        user_statistics = []
        memberships = TeamProjectMembership.objects.filter(project=project).select_related('user')
        for membership in memberships:
            user = membership.user
            user_tasks = tasks.filter(task_assignments__user=user)
            user_time = time_entries.filter(user=user).aggregate(total=Sum('duration'))['total'] or 0
            user_completed = user_tasks.filter(task_assignments__status='Completed').count()
            user_progress = (user_completed / user_tasks.count() * 100) if user_tasks.count() > 0 else 0

            user_statistics.append({
                'user_id': user.id,
                'user_name': f"{user.first_name} {user.last_name}",
                'role': 'Quản lý' if user == project.manager else 'Thành viên',
                'tasks_count': user_tasks.count(),
                'completed_tasks': user_completed,
                'total_time': round(user_time, 2),
                'progress': round(user_progress, 1)
            })

        # Biểu đồ phân phối task theo trạng thái
        task_status_distribution = {
            'Completed': completed_tasks,
            'In progress': in_progress_tasks,
            'Late': late_tasks,
            'To-do': total_tasks - completed_tasks - in_progress_tasks - late_tasks
        }

        # Dữ liệu tiến độ theo thời gian (tháng hiện tại)
        month_start = today.replace(day=1)
        tasks_by_date = {}
        for i in range(31):  # Tối đa 31 ngày/tháng
            date = month_start + timedelta(days=i)
            if date > today:
                break
            completed_by_date = tasks.filter(
                status='Completed',
                completed_date__date__lte=date
            ).count()
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
def project_detail(request, project_id):
    """
    API trả về chi tiết dự án dưới dạng JSON
    """
    try:
        project = Projects.objects.get(id=project_id)

        # Kiểm tra quyền truy cập
        is_member = request.user in project.team_members.all()
        is_manager = request.user == project.manager

        if not is_member and not is_manager and not request.user.is_superuser:
            return JsonResponse({'success': False, 'error': 'Bạn không có quyền xem dự án này'}, status=403)

        # Lấy danh sách thành viên
        members = []
        for user in project.team_members.all():
            user_tasks = Tasks.objects.filter(project=project, task_assignments__user=user)
            user_completed = user_tasks.filter(task_assignments__status='Completed').count()
            user_time = TimeEntries.objects.filter(
                task__project=project,
                user=user
            ).aggregate(total=Sum('duration'))['total'] or 0

            members.append({
                'id': user.id,
                'name': f"{user.first_name} {user.last_name}",
                'email': user.email,
                'role': 'Quản lý' if user == project.manager else 'Thành viên',
                'tasks_count': user_tasks.count(),
                'completed_tasks': user_completed,
                'total_time': round(user_time, 2)
            })

        # Lấy danh sách task
        tasks = []
        for task in Tasks.objects.filter(project=project):
            assignees = task.task_assignments.all().select_related('user')
            assignee_names = [f"{a.user.first_name} {a.user.last_name}" for a in assignees]

            tasks.append({
                'id': task.id,
                'title': task.title,
                'status': task.status,
                'deadline': task.deadline,
                'assignees': assignee_names,
                'assignee_count': len(assignee_names)
            })

        # Tính toán tiến độ
        total_tasks = Tasks.objects.filter(project=project).count()
        completed_tasks = Tasks.objects.filter(project=project, status='Completed').count()
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Trạng thái dự án
        today = timezone.now().date()
        status = 'In progress'
        if completed_tasks == total_tasks and total_tasks > 0:
            status = 'Completed'
        elif project.end_date.date() < today:
            status = 'Late'

        # Dữ liệu task theo trạng thái
        task_statuses = dict(Tasks.objects.filter(project=project).values('status').annotate(count=Count('status')).values_list('status', 'count'))

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
    except Projects.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Dự án không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
