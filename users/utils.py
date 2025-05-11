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
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    if period == 'today':
        entries = TimeEntries.objects.filter(user_id=user_id, start_time__date=today)
    elif period == 'week':
        entries = TimeEntries.objects.filter(user_id=user_id, start_time__gte=week_start)
    total_hours = entries.filter(duration__isnull=False).aggregate(total=Sum('duration'))['total'] or 0
    if period == 'week' and as_json:
        week_data = [0] * 7
        for i in range(7):
            day = week_start + timedelta(days=i)
            day_entries = entries.filter(start_time__date=day, duration__isnull=False)
            day_hours = day_entries.aggregate(total=Sum('duration'))['total'] or 0
            week_data[i] = float(day_hours)
        return mark_safe(json.dumps(week_data, ensure_ascii=False))
    hours = int(total_hours)
    minutes = int((total_hours - hours) * 60)
    return f"{hours}h {minutes}m" if not as_json else mark_safe(json.dumps([float(total_hours)], ensure_ascii=False))

def get_kpi_snapshot(user_id, metric='completion'):
    kpi = EmployeeKPIs.objects.filter(user_id=user_id, time_period='monthly').first()
    if not kpi or not kpi.target_value:
        return "0/0" if metric == 'completion' else 0
    try:
        actual = int(kpi.actual_value) if kpi.actual_value else 0
        target = int(kpi.target_value)
        completion = f"{actual}/{target}"
        percentage = (actual / target * 100) if target != 0 else 0
    except ValueError:
        completion = "0/0"
        percentage = 0
    return completion if metric == 'completion' else percentage

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

def get_project_progress(user_id):
    return [
        {'name': project['name'], 'progress': project['progress']}
        for project in get_project_data(Users.objects.get(id=user_id))
    ]

def get_ai_suggestions(user_id):
    return Tasks.objects.filter(
        task_assignments__user_id=user_id,
        status__in=['To-do', 'In progress']
    ).values('title', 'difficulty', 'estimated_time')[:2]

def get_recent_tasks(user_id):
    return Tasks.objects.filter(task_assignments__user_id=user_id).select_related('project').order_by('-deadline')[:5]

def get_project_time_allocation(user_id, as_json=False):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    entries = TimeEntries.objects.filter(
        user_id=user_id,
        start_time__gte=week_start
    ).select_related('task__project')

    project_times = {}
    for entry in entries:
        if entry.task and entry.task.project:
            project_name = escape(entry.task.project.name.strip())
            project_name = slugify(project_name, allow_unicode=True)
            duration = entry.duration or 0
            project_times[project_name] = project_times.get(project_name, 0) + duration
    data = {
        'labels': list(project_times.keys()) or ['Không có dự án'],
        'data': list(project_times.values()) or [1]
    }
    if as_json:
        json_str = json.dumps(data, ensure_ascii=False)
        return mark_safe(json_str)
    return project_times


def get_task_stats(user):
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

# Sửa hàm handle_check_in trong users/utils.py
def handle_check_in(user, location, image_data):
    """
    Xử lý logic check-in, lưu thông tin và kiểm tra nhận diện khuôn mặt.
    """
    today = timezone.now().date()

    # Sử dụng transaction để tránh tạo nhiều bản ghi
    from django.db import transaction

    with transaction.atomic():
        # Kiểm tra một lần nữa và xóa các bản ghi check-in trùng lặp (nếu có)
        existing_checkins = CheckInCheckOut.objects.filter(user=user, date=today)

        if existing_checkins.exists():
            # Nếu đã có bản ghi, không tạo thêm bản ghi mới
            return False, "Bạn đã check-in hôm nay rồi."

        # Tạo bản ghi check-in mới
        checkin = CheckInCheckOut(
            user=user,
            checkin_time=timezone.now(),
            date=today,
            checkin_location=location,
        )

        if image_data:
            try:
                # Xử lý ảnh
                if ',' in image_data:
                    image_data = image_data.split(',')[1]
                img_bytes = base64.b64decode(image_data)
                img = Image.open(io.BytesIO(img_bytes))
                img = img.resize((320, 240), Image.Resampling.LANCZOS)
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=70)

                # Tạo tên file với timestamp để tránh trùng lặp
                timestamp = int(time.time())
                img_name = f"checkin_{user.username}_{today}_{timestamp}.jpg"

                # Lưu ảnh
                checkin.checkin_image.save(img_name, ContentFile(buffer.getvalue()), save=False)

                # Kiểm tra nhận diện khuôn mặt
                checkin.is_valid_checkin = verify_face(checkin.checkin_image, user)
            except Exception as e:
                print(f"Error processing check-in image: {str(e)}")
                checkin.is_valid_checkin = False
                return False, f"Lỗi xử lý ảnh: {str(e)}"

        # Lưu bản ghi check-in
        checkin.save()

        if not checkin.is_valid_checkin:
            return True, "Check-in thành công nhưng ảnh không hợp lệ. Vui lòng chụp lại nếu cần."

        return True, "Check-in thành công."

# Sửa hàm handle_check_out trong users/utils.py
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
            # Xử lý hình ảnh
            if ',' in image_data:
                image_data = image_data.split(',')[1]

            # Giải mã base64
            image_binary = base64.b64decode(image_data)

            # Xử lý ảnh để giảm kích thước
            img = Image.open(io.BytesIO(image_binary))
            img = img.resize((320, 240), Image.Resampling.LANCZOS)
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=70)

            # Tạo tên file với timestamp để tránh trùng lặp
            timestamp = int(time.time())
            image_name = f"checkout_{user.username}_{today.strftime('%Y-%m-%d')}_{timestamp}.jpg"

            # Tạo ContentFile từ ảnh đã xử lý
            image_content = ContentFile(buffer.getvalue(), name=image_name)

        except Exception as e:
            print(f"Error processing check-out image: {str(e)}")
            return False, f"Lỗi xử lý hình ảnh: {str(e)}"

        # Kiểm tra vị trí cố định
        is_valid_location = True
        is_valid_face = False

        if user.fixed_location:
            try:
                # Phân tích vị trí
                parts = user.fixed_location.split(',')
                if len(parts) != 2:
                    raise ValueError("Định dạng vị trí không hợp lệ")

                fixed_lat = float(parts[0].strip())
                fixed_lng = float(parts[1].strip())

                parts = location.split(',')
                if len(parts) != 2:
                    raise ValueError("Định dạng vị trí không hợp lệ")

                current_lat = float(parts[0].strip())
                current_lng = float(parts[1].strip())

                # Tính khoảng cách
                R = 6371  # Bán kính trái đất (km)

                lat1, lng1 = radians(fixed_lat), radians(fixed_lng)
                lat2, lng2 = radians(current_lat), radians(current_lng)

                dlat = lat2 - lat1
                dlng = lng2 - lng1

                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
                c = 2 * atan2(sqrt(a), sqrt(1-a))
                distance = R * c

                # Kiểm tra khoảng cách (cho phép sai lệch 0.5km)
                is_valid_location = distance <= 0.5

            except Exception as e:
                print(f"Location validation error: {str(e)}")
                is_valid_location = False

        # Sử dụng transaction để đảm bảo tính nhất quán
        from django.db import transaction

        with transaction.atomic():
            # Xử lý trường hợp có nhiều bản ghi check-in trong cùng một ngày
            checkin_records = CheckInCheckOut.objects.filter(user=user, date=today).order_by('-checkin_time')

            if checkin_records.exists():
                # Giữ lại bản ghi đầu tiên, xóa các bản ghi còn lại
                main_record = checkin_records.first()

                if len(checkin_records) > 1:
                    checkin_records.exclude(id=main_record.id).delete()

                # Cập nhật thông tin check-out
                main_record.checkout_time = now
                main_record.checkout_location = location

                if image_content:
                    main_record.checkout_image.save(image_content.name, image_content, save=False)

                    # Kiểm tra nhận diện khuôn mặt
                    is_valid_face = verify_face(main_record.checkout_image, user)
                    main_record.is_valid_checkout = is_valid_location and is_valid_face

                main_record.save()

                if not is_valid_location or not is_valid_face:
                    return True, "Check-out thành công nhưng có thể có vấn đề về vị trí hoặc nhận diện. Quản lý sẽ kiểm tra sau."

                return True, "Check-out thành công!"
            else:
                # Tạo bản ghi mới nếu không có check-in trước đó
                checkout = CheckInCheckOut(
                    user=user,
                    date=today,
                    checkout_time=now,
                    checkout_location=location,
                )

                if image_content:
                    checkout.checkout_image.save(image_content.name, image_content, save=False)

                    # Kiểm tra nhận diện khuôn mặt
                    is_valid_face = verify_face(checkout.checkout_image, user)

                checkout.is_valid_checkout = is_valid_location and is_valid_face
                checkout.save()

                if not is_valid_location or not is_valid_face:
                    return True, "Check-out thành công nhưng có thể có vấn đề về vị trí hoặc nhận diện. Quản lý sẽ kiểm tra sau."

                return True, "Check-out thành công! (Không có check-in trước đó)"

    except Exception as e:
        import traceback
        print(f"Handle check-out error: {str(e)}")
        print(traceback.format_exc())
        return False, f"Lỗi khi xử lý check-out: {str(e)}"


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
