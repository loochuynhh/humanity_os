from django.db import models
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
import json
from projects.models import Tasks, TaskAssignments, TimeEntries, Projects
from kpis.models import EmployeeKPIs
from users.models import Users, CheckInCheckOut, UserFaceImage
import base64
import io
from PIL import Image
from django.core.files.base import ContentFile
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.utils.text import slugify
import face_recognition
import numpy as np
import os
from math import sin, cos, sqrt, atan2, radians
from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordChangeView,
    PasswordResetConfirmView,
)
from custom_admin.forms import (
    RegistrationForm,
    LoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm,
)
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from custom_admin.utils import superuser_required
from django.contrib import messages
import time

def get_task_counts(user_id, as_json=False):
    task_counts = TaskAssignments.objects.filter(user_id=user_id).values('task__status').annotate(count=Count('task__id'))
    task_status = {'To_do': 0, 'In_progress': 0, 'Completed': 0}
    for item in task_counts:
        status = item['task__status'].replace(' ', '_').replace('-', '_')
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
    entries = TimeEntries.objects.filter(user_id=user_id).select_related('task__project')
    project_times = {}
    for entry in entries:
        if entry.task and entry.task.project:
            project_name = entry.task.project.name.strip()
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
