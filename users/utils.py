from django.db.models import Count, Sum
from django.utils import timezone
import json
from projects.models import Tasks, TaskAssignments, TimeEntries, Projects
from kpis.models import EmployeeKPIs
from users.models import Users, CheckInCheckOut, UserFaceImage, AIChatMessage
import base64
import io
from PIL import Image
from django.core.files.base import ContentFile
from django.utils.safestring import mark_safe
import face_recognition
import numpy as np
import os
from math import sin, cos, sqrt, atan2, radians
import time
import google.generativeai as genai
from django.conf import settings
import re

def get_task_counts(user_id, as_json=False):
    task_counts = TaskAssignments.objects.filter(user_id=user_id).values('status').annotate(count=Count('id'))
    task_status = {'To_do': 0, 'In_progress': 0, 'Completed': 0}
    for item in task_counts:
        status = item['status'].replace(' ', '_').replace('-', '_')
        if status in task_status:
            task_status[status] = item['count']
    if as_json:
        return mark_safe(json.dumps(list(task_status.values()), ensure_ascii=False))
    return task_status

def get_time_tracking(user_id, period='today', as_json=False):
    from users.models import CheckInCheckOut
    from django.utils import timezone
    from datetime import timedelta

    today = timezone.now().date()
    now = timezone.now()
    week_start = today - timedelta(days=today.weekday())

    if period == 'today':
        checkin = CheckInCheckOut.objects.filter(user_id=user_id, date=today).first()
        if checkin and checkin.checkin_time:
            if checkin.checkout_time:
                duration = checkin.checkout_time - checkin.checkin_time
            else:
                duration = now - checkin.checkin_time
            total_hours = duration.total_seconds() / 3600
        else:
            total_hours = 0
        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)
        return f"{hours}h {minutes}m" if not as_json else mark_safe(json.dumps([float(total_hours)], ensure_ascii=False))

    elif period == 'week':
        week_data = [0] * 7
        total_hours = 0
        for i in range(7):
            day = week_start + timedelta(days=i)
            checkin = CheckInCheckOut.objects.filter(user_id=user_id, date=day).first()
            if checkin and checkin.checkin_time:
                if checkin.checkout_time:
                    duration = checkin.checkout_time - checkin.checkin_time
                elif day == today:
                    duration = now - checkin.checkin_time
                else:
                    duration = timedelta(0)
                hours = duration.total_seconds() / 3600
            else:
                hours = 0
            week_data[i] = float(hours)
            total_hours += hours
        if as_json:
            return mark_safe(json.dumps(week_data, ensure_ascii=False))
        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)
        return f"{hours}h {minutes}m"

def get_kpi_snapshot(user_id, metric='completion'):
    from kpis.models import EmployeeKPIs
    # Lấy tất cả KPI của user (có thể lọc theo thời gian nếu muốn)
    kpis = EmployeeKPIs.objects.filter(user_id=user_id)
    if not kpis.exists():
        return "0/0" if metric == 'completion' else 0
    total = kpis.count()
    achieved = kpis.filter(evaluation__in=['Achieved', 'Exceeded', 'Partially Achieved']).count()
    if metric == 'completion':
        return f"{achieved}/{total}"
    else:
        percentage = (achieved / total * 100) if total > 0 else 0
        return round(percentage, 2)

def get_project_data(user):
    projects = Projects.objects.filter(team_members=user).distinct()
    project_data = []
    for project in projects:
        total_tasks = project.tasks.count() # type: ignore
        completed_tasks = project.tasks.filter(status='Completed').count() # type: ignore
        progress = round((completed_tasks / total_tasks * 100), 2) if total_tasks else 0
        project_data.append({
            'id': project.id, # type: ignore
            'name': project.name,
            'progress': progress
        })
    return project_data

def get_project_statistics(user_id):
    return [
        {'name': project['name'], 'progress': project['progress']}
        for project in get_project_data(Users.objects.get(id=user_id))
    ]

def get_project_progress(user_id):
    return get_project_statistics(user_id)

def get_ai_suggestions(user_id):
    return Tasks.objects.filter(
        task_assignments__user_id=user_id,
        status__in=['To-do', 'In progress']
    ).values('title', 'difficulty', 'estimated_time')[:2]

def get_recent_tasks(user_id):
    return Tasks.objects.filter(task_assignments__user_id=user_id).select_related('project').order_by('-deadline')[:5]

def get_project_time_allocation(user_id, as_json=False):
    # Lấy tất cả task_assignments của user
    assignments = TaskAssignments.objects.filter(user_id=user_id)
    
    # Lấy time_entries thông qua task_assignment
    entries = TimeEntries.objects.filter(
        task_assignment__in=assignments
    ).select_related('task_assignment__task__project')
    
    project_times = {}
    for entry in entries:
        if entry.task_assignment and entry.task_assignment.task and entry.task_assignment.task.project:
            project_name = entry.task_assignment.task.project.name.strip()
            duration = entry.duration or 0
            project_times[project_name] = project_times.get(project_name, 0) + duration
    
    # Làm tròn tất cả giá trị thời gian đến 2 chữ số thập phân
    project_times = {k: round(v, 2) for k, v in project_times.items()}
    data = {
        'labels': list(project_times.keys()) or ['Không có dự án'],
        'data': list(project_times.values()) or [1]
    }
    if as_json:
        json_str = json.dumps(data, ensure_ascii=False)
        return mark_safe(json_str)
    return project_times

def get_task_stats(user):
    from projects.models import Tasks
    tasks = Tasks.objects.filter(task_assignments__user=user).distinct()
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()
    return {
        'total': total_tasks,
        'completed': completed_tasks,
        'completion_rate': round(completed_tasks / total_tasks * 100, 2) if total_tasks else 0
    }


def verify_face(check_image, user):
    """
    So sánh ảnh check-in/check-out với các ảnh khuôn mặt đã đăng ký của user.
    """
    try:
        # Đọc ảnh check-in/check-out
        check_img = Image.open(check_image)
        check_img = np.array(check_img.convert('RGB'))

        # Tìm khuôn mặt trong ảnh check-in/check-out
        check_encodings = face_recognition.face_encodings(check_img)

        if not check_encodings:
            print("Không tìm thấy khuôn mặt trong ảnh check-in/check-out")
            return False

        # Lấy tất cả ảnh khuôn mặt của user
        face_images = UserFaceImage.objects.filter(user=user)

        if not face_images:
            print("Người dùng chưa đăng ký ảnh khuôn mặt")
            return False

        for face_image in face_images:
            try:
                known_img = Image.open(face_image.face_image)
                known_img = np.array(known_img.convert('RGB'))
                known_encodings = face_recognition.face_encodings(known_img)

                if not known_encodings:
                    print(f"Không tìm thấy khuôn mặt trong ảnh đã đăng ký: {face_image.id}")
                    continue

                # So sánh khuôn mặt
                results = face_recognition.compare_faces(
                    [known_encodings[0]], check_encodings[0], tolerance=0.6
                )

                if results and results[0]:
                    return True  # Khuôn mặt khớp
            except Exception as e:
                print(f"Lỗi khi xử lý ảnh đã đăng ký {face_image.id}: {str(e)}")
                continue

        return False  # Không khớp với bất kỳ ảnh nào
    except Exception as e:
        print(f"Face recognition error: {str(e)}")
        return False


def handle_check_in(user, location, image_data):
    """
    Xử lý logic check-in, lưu thông tin và kiểm tra nhận diện khuôn mặt.
    """
    try:
        today = timezone.now().date()
        now = timezone.now()

        # Xử lý hình ảnh
        image_content = None
        try:
            if ',' in image_data:
                image_data = image_data.split(',')[1]

            # Giải mã base64
            image_binary = base64.b64decode(image_data)
            img = Image.open(io.BytesIO(image_binary))

            # Kiểm tra định dạng ảnh
            if img.format not in ['JPEG', 'PNG']:
                print(f"Định dạng ảnh không hỗ trợ: {img.format}")
                return False, "Định dạng ảnh không hỗ trợ. Vui lòng sử dụng JPEG hoặc PNG."

            # Resize và nén ảnh
            img = img.resize((320, 240), Image.Resampling.LANCZOS)
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=70)

            timestamp = int(time.time())
            image_name = f"checkin_{user.username}_{today.strftime('%Y-%m-%d')}_{timestamp}.jpg"
            image_content = ContentFile(buffer.getvalue(), name=image_name)
            print(f"Check-in image processed: {image_name}, size={len(buffer.getvalue())/1024:.2f}KB")

        except Exception as e:
            print(f"Error processing check-in image: {str(e)}")
            return False, f"Lỗi xử lý hình ảnh: {str(e)}"

        # Kiểm tra vị trí cố định
        is_valid_location = True
        distance = None

        if user.fixed_location:
            try:
                fixed_lat, fixed_lng = map(float, user.fixed_location.split(','))
                current_lat, current_lng = map(float, location.split(','))

                # Tính khoảng cách bằng công thức Haversine
                R = 6371  # Bán kính trái đất (km)
                lat1, lng1 = radians(fixed_lat), radians(fixed_lng)
                lat2, lng2 = radians(current_lat), radians(current_lng)
                dlat = lat2 - lat1
                dlng = lng2 - lng1
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
                c = 2 * atan2(sqrt(a), sqrt(1-a))
                distance = R * c

                is_valid_location = distance <= 0.5  # Cho phép trong vòng 500m
                print(f"Location check: Distance={distance:.2f}km, Valid={is_valid_location}")

            except Exception as e:
                print(f"Location validation error: {str(e)}")
                is_valid_location = False
                return False, f"Lỗi kiểm tra vị trí: {str(e)}"

        from django.db import transaction

        with transaction.atomic():
            # Khóa bản ghi của user để ngăn các giao dịch song song
            user_locked = Users.objects.select_for_update().get(id=user.id)

            # Kiểm tra xem đã có check-in hôm nay chưa
            existing_checkin = CheckInCheckOut.objects.filter(
                user=user_locked,
                date=today,
                checkin_time__isnull=False
            ).first()

            if existing_checkin:
                print(f"Check-in already exists for user {user_locked.username} on {today}, ID={existing_checkin.id}")
                return False, "Bạn đã check-in hôm nay."

            # Xóa các bản ghi trùng lặp (nếu có) trước khi tạo mới
            CheckInCheckOut.objects.filter(user=user_locked, date=today).delete()

            # Tạo bản ghi check-in mới
            checkin = CheckInCheckOut(
                user=user_locked,
                date=today,
                checkin_time=now,
                checkin_location=location
            )

            if image_content:
                checkin.checkin_image.save(image_content.name, image_content, save=False)
                is_valid_face = verify_face(checkin.checkin_image, user_locked)
                checkin.is_valid_checkin = is_valid_face and is_valid_location
                print(f"Face recognition: Valid={is_valid_face}, Overall check-in valid={checkin.is_valid_checkin}")
            else:
                checkin.is_valid_checkin = False
                print("No image provided, marking check-in as invalid")

            # Lưu bản ghi
            checkin.save()
            print(f"Check-in record saved: ID={checkin.id}, User={user_locked.username}, Date={today}")

        # Chuẩn bị thông báo trả về
        if not is_valid_location:
            message = f"Check-in không hợp lệ: Vị trí cách quá xa ({distance:.2f}km)."
        elif not is_valid_face:
            message = "Check-in không hợp lệ: Không nhận diện được khuôn mặt."
        elif not checkin.is_valid_checkin:
            message = "Check-in không hợp lệ: Dữ liệu không đầy đủ."
        else:
            message = "Check-in thành công!"

        return checkin.is_valid_checkin, message

    except Exception as e:
        import traceback
        print(f"Check-in error: {str(e)}")
        print(traceback.format_exc())
        return False, f"Lỗi hệ thống khi check-in: {str(e)}"


def handle_check_out(user, location, image_data):
    """
    Xử lý logic check-out, cập nhật thông tin và kiểm tra nhận diện khuôn mặt.
    """
    try:
        today = timezone.now().date()
        now = timezone.now()

        # Xử lý hình ảnh
        image_content = None
        try:
            if ',' in image_data:
                image_data = image_data.split(',')[1]

            # Giải mã base64
            image_binary = base64.b64decode(image_data)
            img = Image.open(io.BytesIO(image_binary))

            # Kiểm tra định dạng ảnh
            if img.format not in ['JPEG', 'PNG']:
                print(f"Định dạng ảnh không hỗ trợ: {img.format}")
                return False, "Định dạng ảnh không hỗ trợ. Vui lòng sử dụng JPEG hoặc PNG."

            # Resize và nén ảnh
            img = img.resize((320, 240), Image.Resampling.LANCZOS)
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=70)

            timestamp = int(time.time())
            image_name = f"checkout_{user.username}_{today.strftime('%Y-%m-%d')}_{timestamp}.jpg"
            image_content = ContentFile(buffer.getvalue(), name=image_name)
            print(f"Check-out image processed: {image_name}, size={len(buffer.getvalue())/1024:.2f}KB")

        except Exception as e:
            print(f"Error processing check-out image: {str(e)}")
            return False, f"Lỗi xử lý hình ảnh: {str(e)}"

        # Kiểm tra vị trí cố định
        is_valid_location = True
        distance = None

        if user.fixed_location:
            try:
                fixed_lat, fixed_lng = map(float, user.fixed_location.split(','))
                current_lat, current_lng = map(float, location.split(','))

                # Tính khoảng cách bằng công thức Haversine
                R = 6371  # Bán kính trái đất (km)
                lat1, lng1 = radians(fixed_lat), radians(fixed_lng)
                lat2, lng2 = radians(current_lat), radians(current_lng)
                dlat = lat2 - lat1
                dlng = lng2 - lng1
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
                c = 2 * atan2(sqrt(a), sqrt(1-a))
                distance = R * c

                is_valid_location = distance <= 0.5  # Cho phép trong vòng 500m
                print(f"Location check: Distance={distance:.2f}km, Valid={is_valid_location}")

            except Exception as e:
                print(f"Location validation error: {str(e)}")
                is_valid_location = False
                return False, f"Lỗi kiểm tra vị trí: {str(e)}"

        from django.db import transaction

        with transaction.atomic():
            # Tìm bản ghi check-in hôm nay
            checkin = CheckInCheckOut.objects.filter(user=user, date=today).first()

            if not checkin:
                print("No check-in record found for today")
                return False, "Không tìm thấy bản ghi check-in hôm nay."

            if checkin.checkout_time:
                print(f"Duplicate check-out attempt for {today}")
                return False, "Bạn đã check-out hôm nay."

            # Cập nhật bản ghi check-out
            checkin.checkout_time = now
            checkin.checkout_location = location

            if image_content:
                checkin.checkout_image.save(image_content.name, image_content, save=False)
                is_valid_face = verify_face(checkin.checkout_image, user)
                checkin.is_valid_checkout = is_valid_face and is_valid_location
                print(f"Face recognition: Valid={is_valid_face}, Overall check-out valid={checkin.is_valid_checkout}")
            else:
                checkin.is_valid_checkout = False
                print("No image provided, marking check-out as invalid")

            # Lưu bản ghi
            checkin.save()
            print(f"Check-out record saved: ID={checkin.id}, User={user.username}, Date={today}")

        # Chuẩn bị thông báo trả về
        if not is_valid_location:
            message = f"Check-out không hợp lệ: Vị trí cách quá xa ({distance:.2f}km)."
        elif not is_valid_face:
            message = "Check-out không hợp lệ: Không nhận diện được khuôn mặt."
        elif not checkin.is_valid_checkout:
            message = "Check-out không hợp lệ: Dữ liệu không đầy đủ."
        else:
            message = "Check-out thành công!"

        return checkin.is_valid_checkout, message

    except Exception as e:
        import traceback
        print(f"Check-out error: {str(e)}")
        print(traceback.format_exc())
        return False, f"Lỗi hệ thống khi check-out: {str(e)}"


def get_today_work_hours(user):
    """
    Tính số giờ làm việc hôm nay.
    """
    today = timezone.now().date()
    checkin = CheckInCheckOut.objects.filter(user=user, date=today).first()
    if not checkin:
        return None
    if checkin.checkout_time:
        duration = checkin.checkout_time - checkin.checkin_time
    else:
        duration = timezone.now() - checkin.checkin_time
    hours = duration.total_seconds() / 3600
    return f"{hours:.2f} giờ"

def generate_user_report_data(user, period='monthly'):
    today = timezone.now()
    
    # Set date range based on period
    if period == 'monthly':
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if start_date.month == 12:
            end_date = timezone.datetime(start_date.year + 1, 1, 1) - timezone.timedelta(seconds=1)
        else:
            end_date = timezone.datetime(start_date.year, start_date.month + 1, 1) - timezone.timedelta(seconds=1)
        period_display = f"Tháng {start_date.month}/{start_date.year}"
    else:  # quarterly
        quarter = (today.month - 1) // 3
        start_month = quarter * 3 + 1
        start_date = today.replace(month=start_month, day=1, hour=0, minute=0, second=0, microsecond=0)
        if start_month > 9:
            end_date = timezone.datetime(start_date.year + 1, 1, 1) - timezone.timedelta(seconds=1)
        else:
            end_date = timezone.datetime(start_date.year, start_month + 3, 1) - timezone.timedelta(seconds=1)
        quarter_names = {0: "I", 1: "II", 2: "III", 3: "IV"}
        period_display = f"Quý {quarter_names[quarter]} năm {start_date.year}"

    # Get basic user info
    user_info = {
        'full_name': user.get_full_name(),
        'username': user.username,
        'email': user.email,
        'role': user.get_role_display(),
        'department': user.department or "Chưa cập nhật",
        'phone': user.phone or "Chưa cập nhật",
        'status': user.get_status_display(),
        'date_of_joining': user.date_of_joining,
        'avatar_url': user.avatar_url,
        'bio': user.bio or ""
    }
    
    # Get attendance data
    attendance_records = CheckInCheckOut.objects.filter(
        user=user,
        date__range=[start_date.date(), end_date.date()]
    ).order_by('-date')
    
    total_days = (end_date.date() - start_date.date()).days + 1
    present_days = attendance_records.filter(checkin_time__isnull=False).count()
    valid_checkins = attendance_records.filter(is_valid_checkin=True).count()
    valid_checkouts = attendance_records.filter(is_valid_checkout=True).count()
    
    attendance_stats = {
        'records': attendance_records,
        'start_date': start_date.date(),
        'end_date': end_date.date(),
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': total_days - present_days,
        'valid_checkins': valid_checkins,
        'valid_checkouts': valid_checkouts,
        'attendance_rate': round(present_days / total_days * 100, 2) if total_days > 0 else 0,
    }
    
    # Get tasks data
    tasks = Tasks.objects.filter(
        task_assignments__user=user,
        deadline__range=[start_date, end_date]
    ).select_related('project')
    
    # Count tasks by status
    completed_tasks = tasks.filter(status='Completed').count()
    in_progress_tasks = tasks.filter(status='In progress').count()
    todo_tasks = tasks.filter(status='To-do').count()
    late_tasks = tasks.filter(status='Late').count()
    
    completion_rate = round(completed_tasks / tasks.count() * 100, 2) if tasks.count() > 0 else 0
    
    # Time tracking data
    time_entries = TimeEntries.objects.filter(
        task_assignment__user=user,
        start_time__range=[start_date, end_date]
    ).select_related('task_assignment__task')
    
    total_hours = time_entries.aggregate(total=Sum('duration'))['total'] or 0
    
    # Time by day
    time_by_day = {}
    current_date = start_date.date()
    while current_date <= end_date.date():
        day_entries = time_entries.filter(start_time__date=current_date)
        day_total = day_entries.aggregate(total=Sum('duration'))['total'] or 0
        time_by_day[current_date.strftime('%d/%m/%Y')] = round(day_total, 2)
        current_date += timezone.timedelta(days=1)
    
    # Time by project
    task_assignments = TaskAssignments.objects.filter(user=user)
    tasks_with_assignments = Tasks.objects.filter(task_assignments__in=task_assignments)
    projects = Projects.objects.filter(tasks__in=tasks_with_assignments).distinct()
    
    time_by_project = {}
    for project in projects:
        project_time = time_entries.filter(
            task_assignment__task__project=project
        ).aggregate(total=Sum('duration'))['total'] or 0
        if project_time > 0:
            time_by_project[project.name] = round(project_time, 2)
    
    # Calculate productivity metrics
    working_days = len([d for d in time_by_day if time_by_day[d] > 0])
    avg_daily_hours = round(total_hours / working_days, 2) if working_days > 0 else 0
    expected_hours = working_days * 8
    productivity_rate = round((total_hours / expected_hours * 100), 2) if expected_hours > 0 else 0
    
    # Get KPI data if available
    from kpis.models import EmployeeKPIs
    kpis = EmployeeKPIs.objects.filter(
        user=user,
        start_date__lte=end_date,
        end_date__gte=start_date
    ).select_related('kpi', 'kpi__project')
    
    for kpi in kpis:
        kpi.update_from_project()
    
    total_kpis = kpis.count()
    achieved_kpis = kpis.filter(evaluation__in=['Achieved', 'Exceeded']).count()
    completion_kpi_rate = round(achieved_kpis / total_kpis * 100, 2) if total_kpis > 0 else 0
    
    # Group tasks by project for the report
    projects_with_tasks = {}
    for project in projects:
        project_tasks = tasks_with_assignments.filter(project=project)
        if project_tasks.exists():
            projects_with_tasks[project] = {
                'tasks': project_tasks,
                'completed': project_tasks.filter(status='Completed').count(),
                'total': project_tasks.count(),
                'time': time_by_project.get(project.name, 0)
            }
    
    # Evaluations data if available
    from evaluations.models import FormResponses
    from evaluations.utils import calculate_feedback_metrics, get_staff_feedback_queryset

    evaluations = get_staff_feedback_queryset(user, is_received=True, start_date=start_date, end_date=end_date)
    evaluation_metrics = calculate_feedback_metrics(evaluations)
    
    # Combine all data
    report_data = {
        'period': period,
        'period_display': period_display,
        'start_date': start_date,
        'end_date': end_date,
        'user_info': user_info,
        'attendance': attendance_stats,
        'tasks': {
            'all_tasks': tasks,
            'completed': completed_tasks,
            'in_progress': in_progress_tasks,
            'todo': todo_tasks,
            'late': late_tasks,
            'completion_rate': completion_rate,
            'total': tasks.count()
        },
        'time_tracking': {
            'entries': time_entries,
            'total_hours': round(total_hours, 2),
            'by_day': time_by_day,
            'by_project': time_by_project,
            'working_days': working_days,
            'avg_daily_hours': avg_daily_hours,
            'productivity_rate': productivity_rate
        },
        'kpis': {
            'all_kpis': kpis,
            'total': total_kpis,
            'achieved': achieved_kpis,
            'completion_rate': completion_kpi_rate
        },
        'projects': {
            'all_projects': projects,
            'with_tasks': projects_with_tasks,
            'count': projects.count()
        },
        'evaluations': evaluation_metrics
    }
    
    # Thêm đánh giá từ AI
    try:
        ai_evaluation = get_ai_performance_evaluation(user, report_data)
        report_data['ai_evaluation'] = ai_evaluation
    except Exception as e:
        print(f"Không thể tạo đánh giá AI: {str(e)}")
        report_data['ai_evaluation'] = None
    
    return report_data

def get_ai_performance_evaluation(user, report_data):
    """
    Sử dụng AI để tạo đánh giá hiệu suất nhân viên dựa trên dữ liệu báo cáo
    
    Args:
        user: Đối tượng user cần đánh giá
        report_data: Dữ liệu báo cáo hiệu suất đã được tạo từ generate_user_report_data
    
    Returns:
        Phần đánh giá HTML được định dạng
    """
    import google.generativeai as genai
    from django.conf import settings
    import re
    
    try:
        # Chuẩn bị prompt cho AI
        prompt = build_performance_evaluation_prompt(user, report_data)
        
        # Cấu hình và gọi Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        generation_config = genai.types.GenerationConfig(
            temperature=0.2,          # Giảm tính ngẫu nhiên để có đánh giá khách quan
            top_p=0.8,                # Lọc theo xác suất cao
            top_k=40,                 # Lọc theo xếp hạng
            max_output_tokens=1500,   # Giới hạn độ dài phản hồi
        )
        
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
        
        # Xóa tiêu đề nếu có
        evaluation_text = response.text
        lines = evaluation_text.strip().split('\n')
        if len(lines) > 2 and not lines[0].startswith('**') and not '**' in lines[0]:
            # Có thể đây là tiêu đề báo cáo, bỏ qua dòng đầu
            evaluation_text = '\n'.join(lines[1:])
        
        # Định dạng phản hồi dạng HTML
        # 1. Chuyển đổi markdown sang HTML
        # Thay thế các dấu **text** thành <strong>text</strong> (định dạng Markdown cho in đậm)
        evaluation_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', evaluation_text)

        # 2. Xử lý định dạng đặc biệt như "Điểm mạnh:**" -> "Điểm mạnh:<strong>"
        evaluation_html = re.sub(r'([^*]+)\*\*', r'\1<strong>', evaluation_html)
        
        # 3. Chuyển đổi xuống dòng kép thành đoạn văn mới
        evaluation_html = evaluation_html.replace('\n\n', '</p><p>')
        
        # 4. Chuyển đổi xuống dòng đơn thành <br>
        evaluation_html = evaluation_html.replace('\n', '<br>')
        
        # 5. Đảm bảo toàn bộ nội dung được bọc trong thẻ <p>
        if not evaluation_html.startswith('<p>'):
            evaluation_html = f'<p>{evaluation_html}</p>'
        
        # 6. Xử lý các trường hợp đặc biệt còn lại
        evaluation_html = evaluation_html.replace('<p><strong>', '<p><strong>')
        evaluation_html = evaluation_html.replace('</strong></p>', '</strong></p>')
        evaluation_html = evaluation_html.replace('</strong><br>', '</strong><br>')
        evaluation_html = evaluation_html.replace('<br><strong>', '<br><strong>')
        
        # 7. Định dạng cho danh sách nếu có
        evaluation_html = re.sub(r'<br>(\d+)\.\s+', r'<br><strong>\1.</strong> ', evaluation_html)
        
        return evaluation_html
        
    except Exception as e:
        import traceback
        print(f"Lỗi khi tạo đánh giá hiệu suất AI: {str(e)}")
        print(traceback.format_exc())
        return f"<p>Không thể tạo đánh giá tự động. Lỗi: {str(e)}</p>"

def build_performance_evaluation_prompt(user, report_data):
    """
    Xây dựng prompt chi tiết cho đánh giá hiệu suất
    
    Args:
        user: Đối tượng user
        report_data: Dữ liệu báo cáo
    
    Returns:
        Prompt cho Gemini AI
    """
    # Thông tin cá nhân
    user_info = report_data.get('user_info', {})
    full_name = user_info.get('full_name', user.get_full_name())
    role = user_info.get('role', user.get_role_display())
    department = user_info.get('department', 'Chưa xác định')
    
    # Khoảng thời gian
    period_display = report_data.get('period_display', 'Không xác định')
    start_date = report_data.get('start_date', None)
    end_date = report_data.get('end_date', None)
    start_date_str = start_date.strftime('%d/%m/%Y') if start_date else 'Không xác định'
    end_date_str = end_date.strftime('%d/%m/%Y') if end_date else 'Không xác định'
    
    # Dữ liệu điểm danh
    attendance = report_data.get('attendance', {})
    present_days = attendance.get('present_days', 0)
    total_days = attendance.get('total_days', 0)
    attendance_rate = attendance.get('attendance_rate', 0)
    valid_checkins = attendance.get('valid_checkins', 0)
    valid_checkouts = attendance.get('valid_checkouts', 0)
    
    # Dữ liệu công việc
    tasks = report_data.get('tasks', {})
    total_tasks = tasks.get('total', 0)
    completed_tasks = tasks.get('completed', 0)
    in_progress = tasks.get('in_progress', 0)
    late_tasks = tasks.get('late', 0)
    completion_rate = tasks.get('completion_rate', 0)
    
    # Dữ liệu KPI
    kpis = report_data.get('kpis', {})
    total_kpis = kpis.get('total', 0)
    achieved_kpis = kpis.get('achieved', 0)
    kpi_completion_rate = kpis.get('completion_rate', 0)
    
    # Dữ liệu đánh giá
    evaluations = report_data.get('evaluations', {})
    feedback_score = evaluations.get('feedback_score', None)
    feedback_score_str = f"{feedback_score:.1f}/5" if feedback_score is not None else "Chưa có"
    
    # Dữ liệu về thời gian làm việc
    time_tracking = report_data.get('time_tracking', {})
    total_hours = time_tracking.get('total_hours', 0)
    productivity_rate = time_tracking.get('productivity_rate', 0)
    avg_daily_hours = time_tracking.get('avg_daily_hours', 0)
    
    # Dữ liệu dự án
    projects = report_data.get('projects', {})
    project_count = projects.get('count', 0)
    
    # Tạo prompt cho AI
    prompt = f"""
    Bạn là một trợ lý AI chuyên nghiệp đánh giá hiệu suất nhân viên. Hãy tạo một báo cáo đánh giá tổng thể ngắn gọn, khách quan và chi tiết cho nhân viên dựa trên các dữ liệu sau. Báo cáo nên chỉ ra điểm mạnh, điểm cần cải thiện và đề xuất cho sự phát triển trong tương lai.

    # THÔNG TIN NHÂN VIÊN
    - Họ và tên: {full_name}
    - Vai trò: {role}
    - Phòng ban: {department}
    - Khoảng thời gian đánh giá: {period_display} ({start_date_str} đến {end_date_str})

    # DỮ LIỆU HIỆU SUẤT

    ## Điểm danh và thời gian làm việc
    - Số ngày làm việc: {present_days}/{total_days} ngày ({attendance_rate}%)
    - Check-in hợp lệ: {valid_checkins}/{present_days}
    - Check-out hợp lệ: {valid_checkouts}/{present_days}
    - Tổng số giờ làm việc: {total_hours} giờ
    - Giờ làm việc trung bình mỗi ngày: {avg_daily_hours} giờ
    - Hiệu suất thời gian: {productivity_rate}%

    ## Công việc và dự án
    - Số dự án tham gia: {project_count}
    - Tổng số công việc: {total_tasks}
    - Hoàn thành: {completed_tasks} ({completion_rate}%)
    - Đang thực hiện: {in_progress}
    - Trễ hạn: {late_tasks}

    ## KPI và đánh giá
    - KPI đạt được: {achieved_kpis}/{total_kpis} ({kpi_completion_rate}%)
    - Điểm đánh giá trung bình: {feedback_score_str}

    # YÊU CẦU ĐÁNH GIÁ
    1. Tạo một đánh giá tổng thể ngắn gọn (1-3 đoạn) dưới 200 từ, khách quan về hiệu suất làm việc của nhân viên dựa trên các số liệu trên.
    2. Sau đó, dưới tiêu đề "**Điểm mạnh:**", liệt kê các điểm mạnh (sử dụng chính xác định dạng "**Điểm mạnh:**")
    3. Dưới tiêu đề "**Điểm cần cải thiện:**", liệt kê các điểm cần cải thiện (sử dụng chính xác định dạng "**Điểm cần cải thiện:**")
    4. Dưới tiêu đề "**Đề xuất:**", đưa ra 2-3 đề xuất cụ thể để nhân viên cải thiện hiệu suất (đánh số 1., 2., 3.)
    5. Ở cuối đánh giá, đưa ra đánh giá mức hiệu suất tổng thể (Xuất sắc, Tốt, Đạt yêu cầu, hoặc Cần cải thiện).
    6. Viết bằng tiếng Việt, chuyên nghiệp, có định dạng rõ ràng.
    7. KHÔNG bao gồm tiêu đề hay mở đầu kiểu "Đánh giá hiệu suất cho" hoặc kết thúc kiểu "Kết luận"
    8. Giới hạn đánh giá trong khoảng 200-300 từ.
    9. Đảm bảo định dạng markdown rõ ràng và nhất quán.
    
    Hãy viết đánh giá hiệu suất theo định dạng yêu cầu.
    """
    
    return prompt

def summarize_chat(user_msg, max_length=250):
    """
    Tóm tắt tin nhắn người dùng nếu quá dài
    """
    if len(user_msg) <= max_length:
        return user_msg
    
    # Tìm dấu câu để cắt tại vị trí phù hợp
    punctuation_marks = ['.', '!', '?', ';']
    cut_index = max_length - 3  # -3 cho dấu "..."
    
    # Cố gắng cắt tại dấu câu gần nhất
    for i in range(cut_index, max(0, cut_index - 50), -1):
        if i < len(user_msg) and user_msg[i] in punctuation_marks:
            cut_index = i + 1
            break
    
    return user_msg[:cut_index] + "..."

def build_gemini_prompt(user, user_message):
    """
    Build an optimized prompt for Gemini AI that provides comprehensive context about the Humanity OS system,
    the user's data, and supports a conversational AI experience.
    
    Args:
        user: The user object
        user_message: The current message from the user
    
    Returns:
        A structured prompt for Gemini AI
    """
    if not user or not user_message:
        return "Lỗi: Thiếu thông tin người dùng hoặc câu hỏi."

    # Retrieve user's chat history for context
    chat_history = AIChatMessage.objects.filter(user=user).order_by('-timestamp')[:20]  # Lấy tối đa 10 cặp hội thoại
    conversation_context = ""
    
    if chat_history.exists():
        # Tạo danh sách mới và sắp xếp lại theo thời gian
        chat_messages = list(reversed(chat_history))
        
        # Nhóm thành cặp hội thoại người dùng-AI
        conversation_pairs = []
        i = 0
        
        while i < len(chat_messages):
            # Tìm tin nhắn người dùng
            if i < len(chat_messages) and chat_messages[i].role == 'user':
                user_msg = chat_messages[i].content
                ai_msg = ""
                
                # Tìm phản hồi tương ứng của AI
                if i + 1 < len(chat_messages) and chat_messages[i + 1].role == 'model':
                    ai_msg = chat_messages[i + 1].content
                    i += 2  # Tiến tới cặp tiếp theo
                else:
                    i += 1  # Chỉ tiến một bước nếu không tìm thấy phản hồi AI
                
                # Thêm cặp hội thoại nếu có đủ cả hai phần
                if user_msg and ai_msg:
                    conversation_pairs.append({
                        'user_msg': user_msg,
                        'ai_msg': ai_msg
                    })
            else:
                i += 1  # Bỏ qua tin nhắn không phải từ người dùng
        
        # Chỉ giữ lại 5 cặp hội thoại gần nhất
        if conversation_pairs:
            # Lấy 5 cuộc hội thoại gần nhất
            recent_pairs = conversation_pairs[-5:] if len(conversation_pairs) > 5 else conversation_pairs
            
            # Tính tổng độ dài của hội thoại
            total_length = sum(len(pair['user_msg']) + len(pair['ai_msg']) for pair in recent_pairs)
            max_length = 10000  # Giới hạn tổng độ dài
            
            conversation_blocks = []
            
            # Nếu tổng độ dài vượt quá giới hạn, sử dụng phương pháp tóm tắt
            if total_length > max_length:
                # Giảm dần độ dài tóm tắt dựa trên độ xa của cuộc hội thoại
                for i, pair in enumerate(recent_pairs[:-1]):
                    # Cuộc hội thoại càng cũ thì tóm tắt càng ngắn
                    user_max_length = max(100, 300 - (len(recent_pairs) - i - 1) * 50)
                    ai_max_length = max(200, 500 - (len(recent_pairs) - i - 1) * 100)
                    
                    user_msg = summarize_chat(pair['user_msg'], user_max_length)
                    ai_msg = summarize_chat(pair['ai_msg'], ai_max_length)
                    
                    block = f"### Hội thoại {i+1}\n**Người dùng**: {user_msg}\n\n**Trợ lý**: {ai_msg}"
                    conversation_blocks.append(block)
                
                # Giữ nguyên cuộc hội thoại gần nhất hoặc tóm tắt nhẹ nếu quá dài
                latest = recent_pairs[-1]
                user_msg = summarize_chat(latest['user_msg'], 400)
                ai_msg = summarize_chat(latest['ai_msg'], 800)
                
                block = f"### Hội thoại gần nhất\n**Người dùng**: {user_msg}\n\n**Trợ lý**: {ai_msg}"
                conversation_blocks.append(block)
            else:
                # Nếu không vượt quá giới hạn, hiển thị đầy đủ
                for i, pair in enumerate(recent_pairs):
                    block = f"### Hội thoại {i+1}\n**Người dùng**: {pair['user_msg']}\n\n**Trợ lý**: {pair['ai_msg']}"
                    conversation_blocks.append(block)
            
            conversation_context = "## Lịch sử hội thoại gần đây\n\n" + "\n\n".join(conversation_blocks)

    # User Information
    user_info = {
        'username': user.username,
        'full_name': user.get_full_name() or user.username,
        'role': user.get_role_display(),
        'department': user.department or 'Chưa cập nhật',
        'phone': user.phone or 'Chưa cập nhật',
        'bio': user.bio or 'Chưa cập nhật',
        'date_of_joining': user.date_of_joining.strftime('%d/%m/%Y') if user.date_of_joining else 'Chưa cập nhật',
        'status': user.get_status_display(),
        'fixed_location': user.fixed_location or 'Chưa cài đặt',
    }

    # Attendance Data
    today = timezone.now().date()
    today_checkin = CheckInCheckOut.objects.filter(user=user, date=today).first()
    checkin_status = "Đã check-in lúc " + today_checkin.checkin_time.strftime('%H:%M:%S') if today_checkin and today_checkin.checkin_time else "Chưa check-in"
    checkout_status = "Đã check-out lúc " + today_checkin.checkout_time.strftime('%H:%M:%S') if today_checkin and today_checkin.checkout_time else "Chưa check-out"
    
    # Recent check-in history
    checkin_data = CheckInCheckOut.objects.filter(user=user).order_by('-date')[:5]
    checkin_history = [
        {
            'date': c.date.strftime('%d/%m/%Y'),
            'checkin_time': c.checkin_time.strftime('%H:%M:%S') if c.checkin_time else 'Chưa check-in',
            'checkout_time': c.checkout_time.strftime('%H:%M:%S') if c.checkout_time else 'Chưa check-out',
            'checkin_location': c.checkin_location or 'Không có',
            'is_valid_checkin': 'Hợp lệ' if c.is_valid_checkin else 'Không hợp lệ',
            'duration': f"{((c.checkout_time - c.checkin_time).total_seconds() / 3600):.2f}h" if c.checkin_time and c.checkout_time else 'N/A'
        }
        for c in checkin_data
    ]

    # Tasks data with detailed status
    tasks = Tasks.objects.filter(task_assignments__user=user).select_related('project')[:8]
    overdue_tasks = Tasks.objects.filter(
        task_assignments__user=user,
        status__in=['To-do', 'In progress'],
        deadline__lt=timezone.now()
    )[:5]
    
    # Detailed task counts by status
    task_stats = get_task_stats(user)
    
    task_list = [
        {
            'title': t.title,
            'project': t.project.name if t.project else 'Không có dự án',
            'status': t.status,
            'deadline': t.deadline.strftime('%d/%m/%Y %H:%M') if t.deadline else 'Không có hạn',
            'estimated_time': f"{t.estimated_time}h" if t.estimated_time else 'Chưa xác định',
            'difficulty': t.difficulty,
            'is_overdue': t.is_overdue,
            'days_until_deadline': t.days_until_deadline if hasattr(t, 'days_until_deadline') else 'N/A',
        }
        for t in tasks
    ]
    
    overdue_task_list = [
        {
            'title': t.title,
            'project': t.project.name if t.project else 'Không có dự án',
            'deadline': t.deadline.strftime('%d/%m/%Y %H:%M') if t.deadline else 'N/A',
            'days_overdue': abs(t.days_until_deadline) if hasattr(t, 'days_until_deadline') else 'N/A',
        }
        for t in overdue_tasks
    ]

    # Project data with detailed metrics
    projects = Projects.objects.filter(team_members=user).distinct()[:5]
    project_list = []
    for p in projects:
        total_tasks = p.tasks.count()
        completed_tasks = p.tasks.filter(status='Completed').count()
        progress = round((completed_tasks / total_tasks * 100), 2) if total_tasks else 0
        team_size = p.team_members.count()
        
        # Get time spent on this project
        # Get time spent on this project
        time_entries = TimeEntries.objects.filter(
            task_assignment__user=user,
            task_assignment__task__project=p
        )
        total_time = time_entries.aggregate(Sum('duration'))['duration__sum'] or 0
        
        project_list.append({
            'name': p.name,
            'description': p.description or 'Không có mô tả',
            'progress': progress,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'start_date': p.start_date.strftime('%d/%m/%Y') if p.start_date else 'N/A',
            'end_date': p.end_date.strftime('%d/%m/%Y') if p.end_date else 'N/A',
            'team_size': team_size,
            'time_spent': f"{total_time:.2f}h",
            'manager': p.manager.get_full_name() if p.manager else 'Chưa phân công',
        })

    # KPI data with more detailed metrics
    kpis = EmployeeKPIs.objects.filter(user=user).order_by('-end_date')[:5]
    kpi_list = []
    for k in kpis:
        project_name = 'Không có dự án'
        if k.kpi:
            try:
                project_name = k.kpi.project.name if k.kpi.project else 'Không có dự án'
            except Projects.DoesNotExist:
                project_name = 'Dự án không tồn tại'

        kpi_list.append({
            'title': k.kpi.name if k.kpi else 'Không có tiêu đề',
            'project': project_name,
            'evaluation': k.evaluation or 'Chưa đánh giá',
            'score': f"{k.achieved_percentage:.2f}%" if k.achieved_percentage is not None else 'Chưa đánh giá',
            'target_value': k.target_value,
            'actual_value': k.actual_value if k.actual_value is not None else 'Chưa cập nhật',
            'kpi_type': k.kpi.kpi_type if k.kpi else 'N/A',
            'unit': k.kpi.unit if k.kpi and k.kpi.unit else '',
            'start_date': k.start_date.strftime('%d/%m/%Y') if k.start_date else 'N/A',
            'end_date': k.end_date.strftime('%d/%m/%Y') if k.end_date else 'N/A',
            'time_period': k.time_period,
        })

    # Evaluation data
    try:
        from evaluations.models import FormResponses
        from evaluations.utils import calculate_feedback_metrics
        evaluations = FormResponses.objects.filter(target_user=user).order_by('-created_at')[:5]
        evaluation_list = [
            {
                'evaluator': e.user.get_full_name() if e.user else 'Ẩn danh',
                'form_name': e.form.name if e.form else 'N/A',
                'question': e.question.question_text if e.question else 'N/A',
                'answer': e.answer,
                'answer_type': e.answer_type,
                'created_at': e.created_at.strftime('%d/%m/%Y %H:%M') if e.created_at else 'N/A',
            }
            for e in evaluations
        ]
        
        # Get evaluations the user has given to others
        evaluations_given = FormResponses.objects.filter(user=user).order_by('-created_at')[:3]
        evaluations_given_list = [
            {
                'target': e.target_user.get_full_name() if e.target_user else 'N/A',
                'form_name': e.form.name if e.form else 'N/A',
                'question': e.question.question_text if e.question else 'N/A',
                'answer': e.answer,
                'created_at': e.created_at.strftime('%d/%m/%Y %H:%M') if e.created_at else 'N/A',
            }
            for e in evaluations_given
        ]
    except ImportError:
        evaluation_list = []
        evaluations_given_list = []

    # Time tracking data with more detailed metrics
    today_time = get_time_tracking(user.id, period='today')
    week_time = get_time_tracking(user.id, period='week')
    project_time = get_project_time_allocation(user.id)
    
    # Calculate average daily hours and productivity metrics
    week_data = json.loads(get_time_tracking(user.id, period='week', as_json=True))
    working_days = len([d for d in week_data if d > 0])
    avg_daily_hours = round(sum(week_data) / working_days, 2) if working_days > 0 else 0
    expected_hours = working_days * 8  # Assuming 8-hour workday
    productivity_rate = round((sum(week_data) / expected_hours * 100), 2) if expected_hours > 0 else 0

    # Get AI suggestions for prioritization
    suggestions = get_ai_suggestions(user.id)
    suggestion_list = [
        {
            'title': s['title'],
            'difficulty': s['difficulty'] or 'Trung bình',
            'estimated_time': f"{s['estimated_time']}h" if s['estimated_time'] else 'Chưa xác định',
        }
        for s in suggestions
    ]

    # Customize response based on user role
    role_guidance = {
        'Employee': """
        - Vai trò: Nhân viên - tập trung vào hoàn thành công việc, theo dõi KPI cá nhân, và check-in/check-out đúng giờ.
        - Quyền hạn: Xem và cập nhật công việc được giao, theo dõi thời gian làm việc, xem KPI cá nhân, check-in/check-out.
        - Lưu ý: Cần tuân thủ quy trình check-in/check-out, cập nhật tiến độ công việc thường xuyên để các chỉ số KPI được tính chính xác.
        """,
        'Manager': """
        - Vai trò: Quản lý - phụ trách quản lý dự án, phân công công việc, đánh giá nhân viên.
        - Quyền hạn: Tạo và quản lý dự án, phân công công việc, đánh giá nhân viên, xem báo cáo tổng hợp.
        - Lưu ý: Bạn có thể sử dụng chức năng phân công công việc và đánh giá KPI để quản lý nhóm hiệu quả hơn.
        """,
        'Admin': """
        - Vai trò: Quản trị viên - quản lý toàn bộ hệ thống, tài khoản người dùng, cấu hình hệ thống.
        - Quyền hạn: Tạo tài khoản, phân quyền, quản lý cấu hình hệ thống, xem tất cả báo cáo.
        - Lưu ý: Bạn có đầy đủ quyền trong hệ thống, bao gồm tạo người dùng mới, cấu hình KPI và quản lý đánh giá.
        """
    }
    role_specific = role_guidance.get(user_info['role'], role_guidance['Employee'])

    # Build comprehensive system description
    system_description = """
# Humanity OS - Hệ thống quản lý nhân sự và công việc toàn diện

## Mô tả hệ thống
Humanity OS là một nền tảng quản lý nhân sự và công việc toàn diện, được thiết kế để tối ưu hóa quy trình làm việc, theo dõi hiệu suất và tăng cường sự hợp tác trong tổ chức. Hệ thống cung cấp các công cụ để quản lý dự án, phân công và theo dõi công việc, đánh giá hiệu suất nhân viên thông qua KPI, và tính năng check-in/check-out với nhận diện khuôn mặt và vị trí địa lý.

## Chức năng chính
1. **Quản lý người dùng và điểm danh**
   - Đăng nhập/đăng xuất, quản lý hồ sơ cá nhân
   - Check-in/check-out với nhận diện khuôn mặt và vị trí địa lý
   - Thống kê thời gian làm việc theo ngày, tuần, tháng
   - Báo cáo điểm danh chi tiết

2. **Quản lý dự án và công việc**
   - Tạo và quản lý dự án với tiến độ, thời hạn
   - Phân công công việc cho nhân viên
   - Theo dõi trạng thái công việc (To-do, In progress, Completed, Late)
   - Tích hợp với GitHub cho mã nguồn và issues
   - Lịch dự án và công việc theo thời gian thực

3. **Theo dõi thời gian làm việc**
   - Theo dõi thời gian làm việc cho từng công việc
   - Phân tích thời gian theo dự án, công việc
   - Thống kê hiệu suất làm việc theo thời gian

4. **Đánh giá hiệu suất**
   - Thiết lập và theo dõi KPI cho nhân viên
   - Đánh giá đồng nghiệp và nhận phản hồi
   - Báo cáo hiệu suất tổng hợp theo tháng/quý
   - Xuất báo cáo dưới dạng PDF

5. **Trợ lý AI**
   - Hỗ trợ người dùng với các câu hỏi về hệ thống
   - Gợi ý công việc ưu tiên và cải thiện hiệu suất
   - Phân tích dữ liệu và đưa ra insights

## Giao diện
- **Dashboard**: Tổng quan công việc, thời gian làm việc, KPI, tiến độ dự án
- **Sidebar**: Điều hướng đến các chức năng chính (Dự án, Công việc, KPI, Điểm danh, Hồ sơ)
- **Các trang chức năng**: Dự án, Công việc, KPI, Đánh giá, Điểm danh, Hồ sơ cá nhân
- **Trợ lý AI**: Chatbot hỗ trợ người dùng tương tác với hệ thống
"""

    # Current user status summary
    current_status = f"""
## Tổng quan hiện tại
- **Check-in hôm nay**: {checkin_status}
- **Check-out hôm nay**: {checkout_status}
- **Thời gian làm việc hôm nay**: {today_time}
- **Công việc đang làm**: {task_stats["total"]} công việc, {task_stats["completed"]} đã hoàn thành ({task_stats["completion_rate"]}%)
- **Công việc quá hạn**: {len(overdue_task_list)} công việc
- **Hiệu suất KPI**: {get_kpi_snapshot(user.id, "percentage")}%
"""

    # Build the main prompt
    prompt = f"""
{system_description}

# Thông tin người dùng
- **Tên đăng nhập**: {user_info['username']}
- **Họ tên**: {user_info['full_name']}
- **Vai trò**: {user_info['role']}
- **Bộ phận**: {user_info['department']}
- **Ngày tham gia**: {user_info['date_of_joining']}
- **Trạng thái**: {user_info['status']}
- **Vị trí làm việc**: {user_info['fixed_location']}

{role_specific}

{current_status}

## Dữ liệu chi tiết

### Điểm danh và thời gian làm việc
- **Lịch sử điểm danh gần đây**: 
{chr(10).join([f"  • {c['date']}: Check-in {c['checkin_time']} ({c['is_valid_checkin']}), Check-out {c['checkout_time']}, Thời gian làm việc: {c['duration']}" for c in checkin_history]) or '  • Không có dữ liệu'}
- **Thời gian làm việc hôm nay**: {today_time}
- **Thời gian làm việc tuần này**: {week_time}
- **Trung bình giờ làm việc mỗi ngày**: {avg_daily_hours}h
- **Tỷ lệ hiệu suất thời gian**: {productivity_rate}%
- **Phân bổ thời gian theo dự án**: {', '.join([f'{k}: {v}h' for k, v in project_time.items()]) or 'Không có dữ liệu'}

### Công việc
- **Công việc hiện tại**:
{chr(10).join([f"  • {t['title']} (Dự án: {t['project']}, Trạng thái: {t['status']}, Deadline: {t['deadline']}, Độ khó: {t['difficulty']})" for t in task_list]) or '  • Không có công việc'}

- **Công việc quá hạn**:
{chr(10).join([f"  • {t['title']} (Dự án: {t['project']}, Deadline: {t['deadline']}, Quá hạn: {t['days_overdue']} ngày)" for t in overdue_task_list]) or '  • Không có công việc quá hạn'}

- **Thống kê công việc**:
  • Tổng số: {task_stats["total"]} công việc
  • Đã hoàn thành: {task_stats["completed"]} công việc
  • Tỷ lệ hoàn thành: {task_stats["completion_rate"]}%

### Dự án
{chr(10).join([f"- **{p['name']}** (Tiến độ: {p['progress']}%)\n  • Mô tả: {p['description']}\n  • Thời gian: {p['start_date']} - {p['end_date']}\n  • Công việc: {p['completed_tasks']}/{p['total_tasks']} hoàn thành\n  • Quản lý: {p['manager']}\n  • Thành viên: {p['team_size']} người\n  • Thời gian đã dành: {p['time_spent']}" for p in project_list]) or '- Không có dự án'}

### KPI và Đánh giá hiệu suất
- **KPI gần đây**:
{chr(10).join([f"  • {k['title']} ({k['kpi_type']}): {k['actual_value']}/{k['target_value']} {k['unit']} - Đạt {k['score']} ({k['evaluation']})" for k in kpi_list]) or '  • Không có KPI'}

- **Đánh giá từ người khác**:
{chr(10).join([f"  • {e['evaluator']} ({e['form_name']}): {e['answer']} - {e['created_at']}" for e in evaluation_list]) or '  • Không có đánh giá'}

- **Đánh giá bạn đã gửi**:
{chr(10).join([f"  • Đến {e['target']} ({e['form_name']}): {e['answer']} - {e['created_at']}" for e in evaluations_given_list]) or '  • Không có đánh giá'}

### Gợi ý công việc ưu tiên
{chr(10).join([f"- {s['title']} (Độ khó: {s['difficulty']}, Thời gian ước tính: {s['estimated_time']})" for s in suggestion_list]) or '- Không có gợi ý'}

{conversation_context}

## Yêu cầu hiện tại
{user_message}

## Hướng dẫn trả lời
- Trả lời bằng **tiếng Việt**, sử dụng ngôn ngữ **thân thiện** và **chuyên nghiệp**, đầy đủ dấu tiếng Việt.
- Sử dụng **định dạng rõ ràng** (gạch đầu dòng, bôi đậm) cho câu trả lời dễ đọc.
- Ưu tiên trả lời ngắn gọn và đi thẳng vào vấn đề người dùng đang hỏi.
- Nếu phát hiện vấn đề trong dữ liệu (công việc quá hạn, KPI thấp, v.v.), hãy đưa ra gợi ý cải thiện.
- Thể hiện sự hiểu biết về Humanity OS và các tính năng của nó trong câu trả lời.
- Khi trả lời về cách sử dụng tính năng, hãy hướng dẫn cụ thể các bước thực hiện.
- Đưa ra những gợi ý phù hợp với vai trò của người dùng.
"""
    return prompt

def build_admin_gemini_prompt(user, user_message):
    """
    Xây dựng prompt đặc biệt dành cho admin/superuser với đầy đủ thông tin về toàn bộ hệ thống.
    
    Args:
        user: Đối tượng user admin/superuser
        user_message: Tin nhắn từ admin/superuser
    
    Returns:
        Prompt đầy đủ thông tin cho Gemini AI
    """
    if not user or not user_message:
        return "Lỗi: Thiếu thông tin người dùng hoặc câu hỏi."

    # Lấy lịch sử chat để tạo ngữ cảnh
    from .models import AIChatMessage
    chat_history = AIChatMessage.objects.filter(user=user).order_by('-timestamp')[:20]
    conversation_context = ""
    
    if chat_history.exists():
        # Tạo danh sách mới và sắp xếp lại theo thời gian
        chat_messages = list(reversed(chat_history))
        
        # Nhóm thành cặp người dùng - AI
        for i in range(0, len(chat_messages) - 1, 2):
            if i + 1 < len(chat_messages):
                user_msg = chat_messages[i]
                ai_msg = chat_messages[i + 1]
                
                # Giới hạn độ dài để không vượt quá giới hạn token
                user_content = summarize_chat(user_msg.content, 250)
                ai_content = summarize_chat(ai_msg.content, 250)
                
                conversation_context += f"User: {user_content}\nAI: {ai_content}\n\n"
    
    # Lấy thông tin người dùng hiện tại
    user_info = f"""
    Thông tin người dùng:
    - Tên: {user.first_name} {user.last_name}
    - Email: {user.email}
    - Vai trò: {'Quản trị viên' if user.is_superuser else 'Quản lý' if user.is_staff else 'Người dùng'}
    - Phòng ban: {user.department or 'Chưa xác định'}
    - Ngày tham gia: {user.date_of_joining.strftime('%d/%m/%Y') if user.date_of_joining else 'Không có thông tin'}
    """
    
    # Lấy dữ liệu tổng quan về hệ thống
    from django.db.models import Count, Sum, Avg, Q
    from django.utils import timezone
    from datetime import timedelta
    from users.models import Users, CheckInCheckOut
    from projects.models import Tasks, TaskAssignments, TimeEntries, Projects
    from kpis.models import EmployeeKPIs
    
    # Khởi tạo các biến mặc định
    system_overview = ""
    priority_messages = ""
    
    try:
        # Thống kê người dùng
        total_users = Users.objects.count()
        active_users = Users.objects.filter(is_active=True).count()
        admins = Users.objects.filter(is_superuser=True).count()
        staff = Users.objects.filter(is_staff=True).count()
        
        # Thống kê dự án
        total_projects = Projects.objects.count()
        active_projects = Projects.objects.filter(
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date()
        ).count()
        
        # Tính số dự án hoàn thành dựa trên ngày kết thúc đã qua
        completed_projects = Projects.objects.filter(
            end_date__lt=timezone.now().date()
        ).count()
        
        # Thống kê công việc
        total_tasks = Tasks.objects.count()
        completed_tasks = Tasks.objects.filter(status='Completed').count()
        overdue_tasks = Tasks.objects.filter(
            status__in=['To-do', 'In progress'], 
            deadline__lt=timezone.now()
        ).count()
        
        # Thống kê KPI
        avg_kpi = EmployeeKPIs.objects.aggregate(avg=Avg('achieved_percentage'))['avg'] or 0
        
        # Thống kê thời gian làm việc
        today = timezone.now().date()
        total_hours_today = TimeEntries.objects.filter(
            start_time__date=today
        ).aggregate(
            total=Sum('duration')
        )['total'] or 0
        
        # Dữ liệu điểm danh
        checkin_today = CheckInCheckOut.objects.filter(
            date=today,
            checkin_time__isnull=False
        ).count()
        
        checkin_percentage = round((checkin_today / active_users) * 100, 1) if active_users > 0 else 0
        
        # Thông tin người dùng với nhiều task nhất
        user_tasks = Users.objects.annotate(
            task_count=Count('task_assignments__task', distinct=True)
        ).exclude(task_count=0).order_by('-task_count')
        
        most_tasks_info = ""
        least_tasks_info = ""
        
        most_tasks_user = user_tasks.first()
        if most_tasks_user:
            most_tasks_info = f"{most_tasks_user.first_name} {most_tasks_user.last_name}: {most_tasks_user.task_count} tasks"
        
        least_tasks_user = user_tasks.last()
        if least_tasks_user:
            least_tasks_info = f"{least_tasks_user.first_name} {least_tasks_user.last_name}: {least_tasks_user.task_count} tasks"
        
        # Người có giờ làm nhiều nhất
        most_hours_info = ""
        try:
            most_hours_user = Users.objects.annotate(
                work_hours=Sum('task_assignments__actual_time')
            ).exclude(work_hours__isnull=True).order_by('-work_hours').first()
            
            if most_hours_user and hasattr(most_hours_user, 'work_hours'):
                most_hours_info = f"{most_hours_user.first_name} {most_hours_user.last_name}: {round(most_hours_user.work_hours, 2)} giờ"
        except Exception:
            pass
        
        # Tìm những vấn đề ưu tiên cần chú ý
        priority_issues = []
        
        # 1. Dự án sắp hết hạn nhưng tiến độ thấp
        upcoming_deadline_projects = Projects.objects.filter(
            end_date__range=[today, today + timedelta(days=14)]
        )
        
        for project in upcoming_deadline_projects[:5]:  # Giới hạn 5 dự án để tránh quá tải
            try:
                # Lấy tất cả tasks của project thông qua relationship
                tasks = Tasks.objects.filter(project=project)
                total_proj_tasks = tasks.count()
                if total_proj_tasks > 0:
                    completed_proj_tasks = tasks.filter(status='Completed').count()
                    progress = (completed_proj_tasks / total_proj_tasks) * 100
                    
                    if progress < 50:
                        days_left = (project.end_date - today).days
                        priority_issues.append({
                            'type': 'project_deadline',
                            'severity': 'high' if days_left <= 7 else 'medium',
                            'message': f"Dự án '{project.name}' còn {days_left} ngày nhưng mới hoàn thành {round(progress, 1)}%"
                        })
            except Exception:
                # Skip projects with issues
                continue
        
        # 2. Người dùng với nhiều task quá hạn
        users_with_overdue = []
        try:
            # Tìm assignments quá hạn
            overdue_assignments = TaskAssignments.objects.filter(
                task__status__in=['To-do', 'In progress'],
                task__deadline__lt=timezone.now()
            ).select_related('user', 'task')
            
            # Đếm số lượng task quá hạn theo user
            user_overdue_counts = {}
            for assignment in overdue_assignments:
                user_id = assignment.user_id 
                if user_id not in user_overdue_counts:
                    user_overdue_counts[user_id] = {
                        'user': assignment.user,
                        'count': 0
                    }
                user_overdue_counts[user_id]['count'] += 1
            
            # Chuyển thành list và sắp xếp
            for user_data in user_overdue_counts.values():
                if user_data['count'] >= 3:  # Chỉ quan tâm người có >= 3 task quá hạn
                    users_with_overdue.append(user_data)
            
            users_with_overdue.sort(key=lambda x: x['count'], reverse=True)
            
            # Thêm top 5 người dùng có nhiều task quá hạn
            for user_data in users_with_overdue[:5]:
                u = user_data['user']
                count = user_data['count']
                priority_issues.append({
                    'type': 'overdue_tasks',
                    'severity': 'medium' if count >= 5 else 'low',
                    'message': f"{u.first_name} {u.last_name} có {count} công việc quá hạn"
                })
        except Exception:
            pass
        
        # 3. Người dùng không check-in/check-out trong 7 ngày qua
        try:
            week_ago = today - timedelta(days=7)
            # Lấy danh sách người dùng đã check-in trong 7 ngày qua
            checkin_user_ids = set(
                CheckInCheckOut.objects.filter(
                    date__gte=week_ago
                ).values_list('user_id', flat=True)
            )
            
            # Lấy người dùng active nhưng không có trong danh sách check-in
            inactive_users = Users.objects.filter(
                is_active=True
            ).exclude(
                id__in=checkin_user_ids
            ).exclude(
                is_superuser=True
            ).exclude(
                is_staff=True
            )[:5]  # Chỉ lấy 5 người
            
            for u in inactive_users:
                priority_issues.append({
                    'type': 'inactive_user',
                    'severity': 'low',
                    'message': f"{u.first_name} {u.last_name} không check-in trong 7 ngày qua"
                })
        except Exception:
            pass
        
        # Tạo tin nhắn vấn đề ưu tiên
        priority_messages = ""
        if priority_issues:
            priority_messages = "VẤN ĐỀ ƯU TIÊN CẦN CHÚ Ý:\n"
            for issue in sorted(priority_issues, key=lambda x: 0 if x['severity'] == 'high' else 1 if x['severity'] == 'medium' else 2):
                severity_symbol = "🔴" if issue['severity'] == 'high' else "🟠" if issue['severity'] == 'medium' else "🟡"
                priority_messages += f"{severity_symbol} {issue['message']}\n"
        
        # Thống kê tổng quan
        system_overview = f"""
        TỔNG QUAN HỆ THỐNG HUMANITY OS:
        
        👤 NGƯỜI DÙNG:
        - Tổng số: {total_users} người dùng ({active_users} đang hoạt động)
        - Quản trị viên: {admins}, Quản lý: {staff}
        - Điểm danh hôm nay: {checkin_today}/{active_users} người ({checkin_percentage}%)
        
        📊 DỰ ÁN:
        - Tổng số: {total_projects} dự án
        - Đang hoạt động: {active_projects}
        - Đã hoàn thành: {completed_projects}
        
        📝 CÔNG VIỆC:
        - Tổng số: {total_tasks} tasks
        - Đã hoàn thành: {completed_tasks} ({round(completed_tasks/total_tasks*100, 1) if total_tasks > 0 else 0}%)
        - Quá hạn: {overdue_tasks} tasks
        
        ⏱️ THỜI GIAN & HIỆU SUẤT:
        - Tổng giờ làm việc hôm nay: {round(total_hours_today, 2)} giờ
        - Điểm KPI trung bình: {round(avg_kpi, 2)}%
        - Người có nhiều task nhất: {most_tasks_info}
        - Người có ít task nhất: {least_tasks_info}
        - Người làm việc nhiều giờ nhất: {most_hours_info}
        """
    except Exception as e:
        # Fallback nếu có lỗi
        system_overview = f"Không thể tải thông tin hệ thống đầy đủ. Lỗi: {str(e)}"
        priority_messages = ""

    # Tạo prompt chính cho AI
    admin_system_prompt = f"""Bạn là Trợ Lý AI Quản Trị của hệ thống Humanity OS - một hệ thống quản lý dự án, công việc và nhân sự. 
    Bạn đang trò chuyện với {user.first_name} {user.last_name}, một {'quản trị viên' if user.is_superuser else 'quản lý'}. 
    Vai trò của bạn là hỗ trợ trong việc quản lý dự án, công việc, và nhân sự, đưa ra thống kê, đánh giá, và đề xuất hành động.

    {priority_messages}

    {system_overview}

    {user_info}

    Ngữ cảnh cuộc trò chuyện trước đó:
    {conversation_context}

    Khi trả lời:
    1. Ưu tiên phản hồi thông tin quản trị, đề cao góc nhìn tổng quan về dự án, nhân sự, hiệu suất
    2. Cung cấp phân tích chi tiết dựa trên dữ liệu hệ thống
    3. Tập trung vào quản lý, giám sát, tăng hiệu suất nhân sự và dự án
    4. Đề xuất giải pháp cho các vấn đề ưu tiên (nếu có)
    5. Trả lời chuyên nghiệp, súc tích và đầy đủ thông tin
    6. Đảm bảo thông tin bảo mật phù hợp với vai trò quản trị viên

    Câu hỏi/yêu cầu hiện tại của {user.first_name} {user.last_name}: "{user_message}"
    """
    
    return admin_system_prompt

# users/utils.py
def get_chat_messages(user, limit=20):
    """
    Hàm tiện ích lấy tin nhắn chat gần nhất của người dùng.
    """
    if not user or not user.is_authenticated:
        return []
        
    try:
        # Import để tránh circular import
        from .models import AIChatMessage
        
        # Đảm bảo truy vấn trên mô hình AIChatMessage với user là đối tượng Users
        messages = AIChatMessage.objects.filter(user=user).order_by('-timestamp')[:limit]
        return list(messages)[::-1]  # Đảo ngược danh sách để hiển thị tin nhắn cũ trước
    except Exception as e:
        print(f"Lỗi khi lấy chat messages: {str(e)}")
        return []