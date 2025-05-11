# projects/utils.py
from django.db.models import Sum, Count, Avg, Q, F, ExpressionWrapper, fields, Case, When, Value
from django.utils import timezone
from datetime import timedelta, datetime
import json
from .models import Tasks, Projects, TimeEntries, TeamProjectMembership, TaskAssignments


def filter_tasks(tasks, project_id=None, status=None):
    if project_id:
        tasks = tasks.filter(project_id=project_id)
    if status:
        tasks = tasks.filter(status=status)
    return tasks


def get_user_projects(user):
    managed_projects = Projects.objects.filter(manager=user)
    member_projects = Projects.objects.filter(
        id__in=TeamProjectMembership.objects.filter(user=user).values('project_id')
    )
    return (managed_projects | member_projects).distinct()


def update_task_tracking(task, user):
    task.is_tracking = TimeEntries.objects.filter(
        task=task,
        user=user,
        end_time__isnull=True
    ).exists()
    task.update_total_time()
    task.update_start_date()
    task.save()


def update_task_status(task, status):
    task.status = status
    if task.deadline.date() < timezone.now().date() and status != 'Completed' and not task.completed_date:
        task.status = 'Late'
    task.save()


def calculate_time_totals(user):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    # Chuyển đổi sang offset-aware DateTime
    today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
    week_start_dt = timezone.make_aware(timezone.datetime.combine(week_start, timezone.datetime.min.time()))
    month_start_dt = timezone.make_aware(timezone.datetime.combine(month_start, timezone.datetime.min.time()))

    total_time_today = TimeEntries.objects.filter(
        user=user,
        start_time__gte=today_start,
        start_time__lt=today_start + timedelta(days=1)
    ).aggregate(total=Sum('duration'))['total'] or 0
    total_time_week = TimeEntries.objects.filter(
        user=user,
        start_time__gte=week_start_dt
    ).aggregate(total=Sum('duration'))['total'] or 0
    total_time_month = TimeEntries.objects.filter(
        user=user,
        start_time__gte=month_start_dt
    ).aggregate(total=Sum('duration'))['total'] or 0

    def format_time(hours):
        if hours is None:
            return "0h 0m"
        h = int(hours)
        m = int((hours - h) * 60)
        return f"{h}h {m}m"

    return {
        'today': format_time(total_time_today),
        'week': format_time(total_time_week),
        'month': format_time(total_time_month)
    }


def get_project_progress(project):
    tasks = Tasks.objects.filter(project=project)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()
    return (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0


def calculate_team_member_data(project_id):
    members_data = []
    project = Projects.objects.get(id=project_id)
    memberships = TeamProjectMembership.objects.filter(project=project).select_related('user')
    for membership in memberships:
        user = membership.user
        task_count = Tasks.objects.filter(task_assignments__user=user, project=project).count()
        total_time = TimeEntries.objects.filter(user=user, task__project=project).aggregate(
            total=Sum('duration')
        )['total'] or 0
        total_time_str = f"{int(total_time)}h {int((total_time % 1) * 60)}m"
        members_data.append({
            'name': user.get_full_name(),
            'role': 'Quản lý' if user == project.manager else 'Thành viên',
            'join_date': membership.join_date.strftime('%d/%m/%Y'),
            'task_count': task_count,
            'total_time': total_time_str,
        })
    return members_data


def calculate_project_progress_data(project_id):
    project = Projects.objects.get(id=project_id)
    tasks = Tasks.objects.filter(project=project)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()
    task_counts = dict(tasks.values('status').annotate(count=Count('status')).values_list('status', 'count'))
    progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'progress': round(progress, 1),
        'task_counts': task_counts
    }


def check_deadline_warnings(task):
    days_until_deadline = task.days_until_deadline
    if task.is_overdue:
        return {'type': 'danger', 'message': 'Task đã quá hạn!'}
    elif 0 <= days_until_deadline <= 2:
        return {'type': 'warning', 'message': f'Task sắp đến hạn ({days_until_deadline} ngày còn lại)!'}
    return None


def get_project_progress_data(project_id):
    project = Projects.objects.get(id=project_id)
    tasks = Tasks.objects.filter(project=project)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()
    task_counts = dict(tasks.values('status').annotate(count=Count('status')).values_list('status', 'count'))
    progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'progress': round(progress, 1),
        'task_counts': task_counts
    }

def calculate_time_by_day(user):
    today = timezone.now().date()
    week_start = today - timedelta(days=6)  # 7 ngày gần nhất
    data = []

    for i in range(7):
        day = week_start + timedelta(days=i)
        # Đảm bảo day_start và day_end là offset-aware
        day_start = timezone.make_aware(timezone.datetime.combine(day, timezone.datetime.min.time()))
        day_end = day_start + timedelta(days=1)
        total_time = 0.0

        entries = TimeEntries.objects.filter(
            user=user,
            start_time__lte=day_end,
            end_time__gte=day_start
        ).exclude(end_time__isnull=True)

        for entry in entries:
            # Giới hạn thời gian trong ngày
            start = max(entry.start_time, day_start)
            end = min(entry.end_time, day_end)  # end_time đã được lọc không null
            if start < end:
                duration = (end - start).total_seconds() / 3600
                total_time += duration

        # Đảm bảo tổng thời gian không vượt quá 24 giờ
        total_time = min(total_time, 24.0)

        data.append({
            'day': day.strftime('%d/%m'),
            'total_time': round(total_time, 2)
        })

    return data

def calculate_time_by_task(user):
    data = []
    tasks = Tasks.objects.filter(
        task_assignments__user=user
    )
    for task in tasks:
        total_time = TimeEntries.objects.filter(
            user=user,
            task=task
        ).aggregate(total=Sum('duration'))['total'] or 0
        if total_time > 0:
            data.append({
                'task_title': task.title,
                'total_time': round(total_time, 2)
            })
    return data

# Các hàm mới cho chức năng dự án

def get_project_dashboard_data(user):
    """
    Lấy dữ liệu tổng quan cho dashboard dự án
    """
    # Lấy các dự án tham gia
    user_projects = get_user_projects(user)
    total_projects = user_projects.count()

    # Dự án đang hoạt động
    active_projects = user_projects.filter(end_date__gt=timezone.now()).count()

    # Tasks của user
    user_tasks = Tasks.objects.filter(task_assignments__user=user)
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(status='Completed').count()

    # Tổng thời gian làm việc trong tháng
    current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_time = TimeEntries.objects.filter(
        user=user,
        start_time__gte=current_month_start
    ).aggregate(total=Sum('duration'))['total'] or 0

    # Dự án gần đây
    recent_projects = user_projects.order_by('-start_date')[:5]

    # Tỉ lệ hoàn thành dự án
    project_completion_rates = []
    for project in recent_projects:
        tasks = Tasks.objects.filter(project=project)
        total = tasks.count()
        completed = tasks.filter(status='Completed').count()
        rate = (completed / total * 100) if total > 0 else 0

        # Tính deadline
        days_left = (project.end_date.date() - timezone.now().date()).days
        status = 'on_track'
        if days_left < 0:
            status = 'overdue'
        elif days_left <= 7:
            status = 'warning'

        project_completion_rates.append({
            'id': project.id,
            'name': project.name,
            'progress': round(rate, 1),
            'days_left': days_left,
            'status': status
        })

    # Tasks sắp đến hạn
    upcoming_tasks = user_tasks.filter(
        status__in=['To-do', 'In progress'],
        deadline__gte=timezone.now()
    ).order_by('deadline')[:5]

    upcoming_tasks_data = []
    for task in upcoming_tasks:
        upcoming_tasks_data.append({
            'id': task.id,
            'title': task.title,
            'project': task.project.name,
            'deadline': task.deadline.strftime('%d/%m/%Y'),
            'days_left': (task.deadline.date() - timezone.now().date()).days,
            'status': task.status
        })

    return {
        'total_projects': total_projects,
        'active_projects': active_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0,
        'month_time': round(month_time, 1),
        'recent_projects': project_completion_rates,
        'upcoming_tasks': upcoming_tasks_data
    }

def get_project_detail_data(project_id):
    """
    Lấy thông tin chi tiết cho một dự án cụ thể
    """
    try:
        project = Projects.objects.get(id=project_id)

        # Tính số ngày còn lại
        days_passed = (timezone.now().date() - project.start_date.date()).days
        total_days = (project.end_date.date() - project.start_date.date()).days
        days_left = (project.end_date.date() - timezone.now().date()).days

        # Tính tiến độ theo thời gian
        time_progress = (days_passed / total_days * 100) if total_days > 0 else 0

        # Tính tiến độ theo tasks
        tasks = Tasks.objects.filter(project=project)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='Completed').count()
        task_progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Phân bố tasks theo trạng thái
        task_distribution = dict(tasks.values('status').annotate(count=Count('status')).values_list('status', 'count'))

        # Tổng thời gian làm việc
        total_time = TimeEntries.objects.filter(
            task__project=project
        ).aggregate(total=Sum('duration'))['total'] or 0

        # Thành viên dự án và phân bổ công việc
        team_members = project.team_members.all()
        team_data = []

        for member in team_members:
            member_tasks = tasks.filter(task_assignments__user=member)
            member_completed = member_tasks.filter(status='Completed').count()
            member_time = TimeEntries.objects.filter(
                user=member,
                task__project=project
            ).aggregate(total=Sum('duration'))['total'] or 0

            team_data.append({
                'id': member.id,
                'name': f"{member.first_name} {member.last_name}",
                'email': member.email,
                'avatar': member.avatar_url,
                'total_tasks': member_tasks.count(),
                'completed_tasks': member_completed,
                'work_time': round(member_time, 1)
            })

        # Lấy 5 task gần đây nhất
        recent_tasks = tasks.order_by('-start_date' if '-start_date' else 'id')[:5]
        recent_task_data = []

        for task in recent_tasks:
            recent_task_data.append({
                'id': task.id,
                'title': task.title,
                'status': task.status,
                'deadline': task.deadline.strftime('%d/%m/%Y'),
                'assignees': [
                    {
                        'id': assignment.user.id,
                        'name': f"{assignment.user.first_name} {assignment.user.last_name}",
                        'avatar': assignment.user.avatar_url
                    } for assignment in task.task_assignments.all() # type: ignore
                ]
            })

        return {
            'project': {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'start_date': project.start_date.strftime('%d/%m/%Y'),
                'end_date': project.end_date.strftime('%d/%m/%Y'),
                'days_passed': days_passed,
                'days_left': days_left,
                'total_days': total_days,
                'time_progress': round(time_progress, 1),
                'task_progress': round(task_progress, 1),
                'manager': f"{project.manager.first_name} {project.manager.last_name}" if project.manager else "Không có",
                'manager_avatar': project.manager.avatar_url if project.manager else None,
            },
            'task_stats': {
                'total': total_tasks,
                'completed': completed_tasks,
                'distribution': task_distribution
            },
            'time_stats': {
                'total_time': round(total_time, 1),
                'avg_time_per_task': round(total_time / total_tasks, 1) if total_tasks > 0 else 0
            },
            'team': team_data,
            'recent_tasks': recent_task_data
        }
    except Projects.DoesNotExist:
        return None
    except Exception as e:
        print(f"Lỗi khi lấy thông tin dự án: {str(e)}")
        return None

def get_task_board_data(user, project_id=None):
    """
    Lấy dữ liệu cho bảng Kanban
    """
    if project_id:
        tasks = Tasks.objects.filter(project_id=project_id)
    else:
        # Lấy tất cả tasks của các dự án mà user tham gia
        tasks = Tasks.objects.filter(
            Q(task_assignments__user=user) |
            Q(project__manager=user)
        ).distinct()

    # Lọc tasks theo trạng thái
    todo_tasks = tasks.filter(status='To-do')
    in_progress_tasks = tasks.filter(status='In progress')
    completed_tasks = tasks.filter(status='Completed')
    late_tasks = tasks.filter(status='Late')

    # Chuyển đổi thành định dạng Kanban
    def format_task(task):
        return {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'deadline': task.deadline.strftime('%d/%m/%Y'),
            'project_name': task.project.name,
            'project_id': task.project.id,
            'difficulty': task.difficulty,
            'assignees': [
                {
                    'id': assignment.user.id,
                    'name': f"{assignment.user.first_name} {assignment.user.last_name}",
                    'avatar': assignment.user.avatar_url
                } for assignment in task.task_assignments.all() # type: ignore
            ],
            'is_overdue': task.is_overdue,
            'days_until_deadline': task.days_until_deadline
        }

    return {
        'todo': [format_task(task) for task in todo_tasks],
        'in_progress': [format_task(task) for task in in_progress_tasks],
        'completed': [format_task(task) for task in completed_tasks],
        'late': [format_task(task) for task in late_tasks]
    }

def get_timeline_data(user, start_date=None, end_date=None):
    """
    Lấy dữ liệu cho timeline dự án
    """
    if not start_date:
        start_date = timezone.now().date() - timedelta(days=30)
    if not end_date:
        end_date = timezone.now().date() + timedelta(days=60)

    # Lấy các dự án của user
    user_projects = get_user_projects(user)

    timeline_data = []
    for project in user_projects:
        # Thêm mốc thời gian dự án
        timeline_data.append({
            'id': f"project_start_{project.id}",
            'title': f"Bắt đầu: {project.name}",
            'date': project.start_date.strftime('%Y-%m-%d'),
            'type': 'project_start',
            'project_id': project.id,
            'color': '#28a745'  # Màu xanh lá
        })

        timeline_data.append({
            'id': f"project_end_{project.id}",
            'title': f"Kết thúc: {project.name}",
            'date': project.end_date.strftime('%Y-%m-%d'),
            'type': 'project_end',
            'project_id': project.id,
            'color': '#dc3545'  # Màu đỏ
        })

        # Lấy các tasks quan trọng
        tasks = Tasks.objects.filter(
            project=project,
            deadline__gte=start_date,
            deadline__lte=end_date
        )

        for task in tasks:
            task_color = '#007bff'  # Màu xanh dương mặc định
            if task.status == 'Completed':
                task_color = '#28a745'  # Xanh lá
            elif task.status == 'Late':
                task_color = '#dc3545'  # Đỏ
            elif task.deadline.date() < timezone.now().date():
                task_color = '#ffc107'  # Vàng (quá hạn)

            timeline_data.append({
                'id': f"task_{task.id}",
                'title': task.title,
                'date': task.deadline.strftime('%Y-%m-%d'),
                'type': 'task',
                'project_id': project.id,
                'task_id': task.id,
                'status': task.status,
                'color': task_color
            })

    # Sắp xếp theo thời gian
    timeline_data.sort(key=lambda x: x['date'])

    return timeline_data

def get_analytics_data(user):
    """
    Lấy dữ liệu phân tích về dự án
    """
    # Lấy các dự án của user
    user_projects = get_user_projects(user)

    # Tổng quan dự án
    project_overview = []
    for project in user_projects:
        tasks = Tasks.objects.filter(project=project)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='Completed').count()
        total_time = TimeEntries.objects.filter(
            task__project=project
        ).aggregate(total=Sum('duration'))['total'] or 0

        # Tính toán tiến độ
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Đánh giá hiệu suất
        time_estimated = tasks.aggregate(total=Sum('estimated_time'))['total'] or 0
        time_efficiency = (time_estimated / total_time * 100) if total_time > 0 else 0

        project_overview.append({
            'id': project.id,
            'name': project.name,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'progress': round(progress, 1),
            'total_time': round(total_time, 1),
            'time_efficiency': round(time_efficiency, 1)
        })

    # Phân bổ thời gian theo dự án
    time_allocation = []
    total_project_time = 0
    for project in user_projects:
        project_time = TimeEntries.objects.filter(
            task__project=project
        ).aggregate(total=Sum('duration'))['total'] or 0

        total_project_time += project_time

        time_allocation.append({
            'project': project.name,
            'time': round(project_time, 1)
        })

    # Tính phần trăm
    for item in time_allocation:
        item['percentage'] = round((item['time'] / total_project_time * 100), 1) if total_project_time > 0 else 0

    # Hiệu suất theo thời gian
    # Dữ liệu 6 tháng gần nhất
    months_data = []
    current_date = timezone.now().date()

    for i in range(5, -1, -1):
        month_date = (current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        if i > 0:
            month_date = month_date.replace(month=(current_date.month - i) % 12 or 12)
            if month_date.month > current_date.month:
                month_date = month_date.replace(year=current_date.year - 1)

        month_entries = TimeEntries.objects.filter(
            start_time__year=month_date.year,
            start_time__month=month_date.month
        )

        tasks_completed = Tasks.objects.filter(
            completed_date__year=month_date.year,
            completed_date__month=month_date.month
        ).count()

        month_time = month_entries.aggregate(total=Sum('duration'))['total'] or 0

        months_data.append({
            'month': month_date.strftime('%m/%Y'),
            'work_hours': round(month_time, 1),
            'tasks_completed': tasks_completed
        })

    # Hiệu suất của thành viên
    team_performance = []

    for project in user_projects:
        for member in project.team_members.all():
            member_tasks = Tasks.objects.filter(
                project=project,
                task_assignments__user=member
            )

            member_time = TimeEntries.objects.filter(
                user=member,
                task__project=project
            ).aggregate(total=Sum('duration'))['total'] or 0

            total_tasks = member_tasks.count()
            completed_tasks = member_tasks.filter(status='Completed').count()

            # Kiểm tra nếu đã có người này trong danh sách
            existing_member = next((m for m in team_performance if m['id'] == member.id), None)

            if existing_member:
                existing_member['total_tasks'] += total_tasks
                existing_member['completed_tasks'] += completed_tasks
                existing_member['work_time'] += member_time
            else:
                team_performance.append({
                    'id': member.id,
                    'name': f"{member.first_name} {member.last_name}",
                    'avatar': member.avatar_url,
                    'total_tasks': total_tasks,
                    'completed_tasks': completed_tasks,
                    'work_time': round(member_time, 1),
                    'completion_rate': round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0
                })

    # Sắp xếp theo tỷ lệ hoàn thành
    team_performance.sort(key=lambda x: x['completion_rate'], reverse=True)

    return {
        'project_overview': project_overview,
        'time_allocation': time_allocation,
        'months_data': months_data,
        'team_performance': team_performance
    }
