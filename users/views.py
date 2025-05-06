from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.http import require_POST
from .models import Goals, Users, UserFaceImage, CheckInCheckOut
from .utils import (
    get_task_counts,
    get_time_tracking,
    get_kpi_snapshot,
    get_project_progress,
    get_recent_tasks,
    get_personal_goals,
    get_project_time_allocation,
    get_goals_progress,
    handle_check_in,
    handle_check_out,
    get_goals_summary,
    get_goals_stats,
    get_project_data,
)


def admin_required(view_func):
    @login_required(login_url="users:login")
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return HttpResponseForbidden("Bạn không có quyền truy cập.")
        return view_func(request, *args, **kwargs)
    return wrapper


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Đăng nhập thành công!")
            return redirect("users:index")
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")
    return render(request, "main/pages/users/login.html")


@login_required(login_url="users:login")
def logout_view(request):
    logout(request)
    messages.success(request, "Bạn đã đăng xuất!")
    return redirect("home")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = Users.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse("users:reset_password", kwargs={"uidb64": uid, "token": token})
            )
            send_mail(
                subject="Đặt lại mật khẩu của bạn",
                message=f"Nhấp vào liên kết sau để đặt lại mật khẩu: {reset_url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(
                request, "Liên kết đặt lại mật khẩu đã được gửi vào email của bạn."
            )
        except Users.DoesNotExist:
            messages.error(request, "Email không tồn tại!")
        except Exception as e:
            messages.error(request, "Có lỗi xảy ra! Vui lòng thử lại sau")
    return render(request, "main/pages/users/forgot_password.html")


@login_required(login_url="users:login")
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        user = request.user

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if not user.check_password(current_password):
            if is_ajax:
                return JsonResponse({"success": False, "message": "Mật khẩu hiện tại không chính xác!"})
            messages.error(request, "Mật khẩu hiện tại không chính xác!")
            return redirect("users:profile")
        elif new_password != confirm_password:
            if is_ajax:
                return JsonResponse({"success": False, "message": "Mật khẩu mới không khớp!"})
            messages.error(request, "Mật khẩu mới không khớp!")
            return redirect("users:profile")
        else:
            user.set_password(new_password)
            user.save()
            logout(request)
            if is_ajax:
                return JsonResponse({"success": True, "message": "Mật khẩu đã được thay đổi. Vui lòng đăng nhập lại!"})
            messages.success(request, "Mật khẩu đã được thay đổi. Vui lòng đăng nhập lại!")
            return redirect("users:login")

    return render(request, "main/pages/users/change_password.html")


def reset_password(request, uidb64, token):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Users.objects.get(pk=uid)
            if PasswordResetTokenGenerator().check_token(user, token):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Mật khẩu đã được đặt lại!")
                    return redirect("users:login")
                else:
                    messages.error(request, "Mật khẩu không khớp!")
            else:
                messages.error(request, "Liên kết không hợp lệ!")
        except (Users.DoesNotExist, ValueError):
            messages.error(request, "Liên kết không hợp lệ!")
    return render(request, "main/pages/users/reset_password.html")


@admin_required
def user_list(request):
    users = Users.objects.all()
    return render(request, "main/pages/users/list.html", {"users": users})


@admin_required
def create_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if Users.objects.filter(username=username).exists():
            messages.error(request, "Tên đăng nhập đã tồn tại!")
        elif Users.objects.filter(email=email).exists():
            messages.error(request, "Email đã tồn tại!")
        else:
            user = Users(username=username, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, "Tài khoản đã được tạo!")
            return redirect("users:user_list")
    return render(request, "users/create_user.html")


@login_required
@require_POST
def check_in(request):
    """
    Xử lý check-in của người dùng, lưu thời gian, địa điểm và hình ảnh.
    """
    try:
        location = request.POST.get('checkin_location', '')
        image_data = request.POST.get('checkin_image', '')

        if not location or not image_data:
            messages.error(request, "Thiếu thông tin vị trí hoặc ảnh check-in.")
            return JsonResponse({
                "success": False,
                "message": "Thiếu thông tin vị trí hoặc ảnh check-in.",
                "redirect": False
            })

        success, message = handle_check_in(request.user, location, image_data)

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return JsonResponse({
            "success": success,
            "message": message,
            "redirect": True,
            "redirect_url": reverse('users:profile')
        })
    except Exception as e:
        import traceback
        print(f"Check-in error: {str(e)}")
        print(traceback.format_exc())
        messages.error(request, f"Lỗi hệ thống: {str(e)}")
        return JsonResponse({
            "success": False,
            "message": f"Lỗi hệ thống: {str(e)}",
            "redirect": True,
            "redirect_url": reverse('users:profile')
        })


@login_required
@require_POST
def check_out(request):
    """
    Xử lý check-out của người dùng, lưu thời gian, địa điểm và hình ảnh.
    """
    try:
        location = request.POST.get('checkout_location', '')
        image_data = request.POST.get('checkout_image', '')

        if not location:
            return JsonResponse({
                "success": False,
                "message": "Vui lòng cung cấp vị trí của bạn.",
                "redirect": False
            })

        if not image_data:
            return JsonResponse({
                "success": False,
                "message": "Vui lòng chụp ảnh để check-out.",
                "redirect": False
            })

        # Thêm log để debug
        print(f"Check-out request received - Location: {location[:20]}..., Image data length: {len(image_data)}")

        success, message = handle_check_out(request.user, location, image_data)

        # Thêm log kết quả
        print(f"Check-out result: Success={success}, Message={message}")

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return JsonResponse({
            "success": success,
            "message": message,
            "redirect": True,
            "redirect_url": reverse('users:profile')
        })
    except Exception as e:
        import traceback
        print(f"Check-out error: {str(e)}")
        print(traceback.format_exc())
        messages.error(request, f"Lỗi hệ thống: {str(e)}")
        return JsonResponse({
            "success": False,
            "message": f"Lỗi hệ thống: {str(e)}",
            "redirect": False
        })


@login_required
def index(request):
    user = request.user
    context = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "avatar_url": user.avatar_url,
        "task_counts": get_task_counts(user.id),
        "task_chart_data": get_task_counts(user.id, as_json=True),
        "today_time": get_time_tracking(user.id, period="today"),
        "week_time": get_time_tracking(user.id, period="week"),
        "week_chart_data": get_time_tracking(user.id, period="week", as_json=True),
        "kpi_completion": get_kpi_snapshot(user.id, "completion"),
        "kpi_percentage": round(float(get_kpi_snapshot(user.id, "percentage")), 2),
        "project_progress": get_project_progress(user.id),
        "recent_tasks": get_recent_tasks(user.id),
        "personal_goals": get_personal_goals(user.id),
        "project_time_allocation": get_project_time_allocation(user.id, as_json=True),
        "goals_progress": get_goals_progress(user.id, as_json=True),
    }
    return render(request, "main/pages/index.html", context)


def set_goal(request):
    if request.method == "POST":
        return render(request, "users/action_success.html", {"message": "Đặt mục tiêu thành công!"})
    return redirect("users:index")


@login_required
def goals(request):
    goals = Goals.objects.filter(user=request.user)
    context = {
        "goals": goals,
        **get_goals_summary(request.user),
        "today": timezone.now().date(),
    }
    return render(request, "main/pages/users/goals.html", context)


@require_POST
@login_required
def add_goal(request):
    try:
        Goals.objects.create(
            user=request.user,
            name=request.POST.get("goal_name"),
            description=request.POST.get("goal_description"),
            deadline=request.POST.get("goal_deadline"),
            priority=request.POST.get("goal_priority"),
            achieved_percentage=0,
            status="Pending",
        )
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@require_POST
@login_required
def update_goal(request):
    try:
        goal_id = request.POST.get("goal_id")
        goal = Goals.objects.get(id=goal_id, user=request.user)
        goal.name = request.POST.get("goal_name")
        goal.description = request.POST.get("goal_description")
        goal.deadline = request.POST.get("goal_deadline")
        goal.priority = request.POST.get("goal_priority")
        goal.achieved_percentage = float(request.POST.get("goal_achieved_percentage"))
        goal.status = request.POST.get("goal_status")
        goal.save()
        return JsonResponse({"success": True})
    except Goals.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Mục tiêu không tồn tại"}, status=404
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@login_required
def profile(request):
    """
    Hiển thị trang hồ sơ cá nhân của người dùng.
    """
    user = request.user

    # Lấy dữ liệu cho trang profile
    recent_tasks = get_recent_tasks(user)
    personal_goals = get_personal_goals(user)
    face_images = UserFaceImage.objects.filter(user=user).order_by('-uploaded_at')

    # Lấy lịch sử check-in/check-out (7 ngày gần nhất)
    end_date = timezone.now().date()
    start_date = end_date - timezone.timedelta(days=7)
    checkin_history = CheckInCheckOut.objects.filter(
        user=user,
        date__range=[start_date, end_date]
    ).order_by('-date')

    # Lấy danh sách dự án tham gia
    projects = get_project_data(user)

    context = {
        'user': user,
        'recent_tasks': recent_tasks,
        'personal_goals': personal_goals,
        'face_images': face_images,
        'checkin_history': checkin_history,
        'projects': projects,
    }

    return render(request, "main/pages/users/profile.html", context)


@login_required
def update_profile(request):
    if request.method == "POST":
        user = request.user
        try:
            user.first_name = request.POST.get("first_name", user.first_name)
            user.last_name = request.POST.get("last_name", user.last_name)
            user.phone = request.POST.get("phone", user.phone)
            user.department = request.POST.get("department", user.department)
            user.bio = request.POST.get("bio", user.bio)
            date_of_joining = request.POST.get("date_of_joining")
            if date_of_joining:
                user.date_of_joining = date_of_joining
            if "avatar" in request.FILES:
                user.avatar = request.FILES["avatar"]
            user.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required
@require_POST
def upload_face_image(request):
    """
    Xử lý tải lên ảnh khuôn mặt cho nhận diện.
    """
    if 'face_image' not in request.FILES:
        return JsonResponse({"success": False, "error": "Không có ảnh được tải lên."})

    try:
        face_image = request.FILES['face_image']
        UserFaceImage.objects.create(
            user=request.user,
            face_image=face_image
        )
        return JsonResponse({"success": True, "message": "Tải ảnh khuôn mặt thành công."})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
@require_POST
def update_fixed_location(request):
    """
    Cập nhật vị trí cố định của người dùng.
    """
    try:
        fixed_location = request.POST.get('fixed_location', '')

        # Kiểm tra định dạng
        if fixed_location:
            try:
                lat, lng = map(float, fixed_location.split(','))
                if not (-90 <= lat <= 90 and -180 <= lng <= 180):
                    return JsonResponse({
                        "success": False,
                        "message": "Vị trí không hợp lệ. Vui lòng kiểm tra lại."
                    })
            except:
                return JsonResponse({
                    "success": False,
                    "message": "Định dạng vị trí không hợp lệ. Vui lòng sử dụng định dạng: latitude,longitude"
                })

        # Cập nhật vị trí
        user = request.user
        user.fixed_location = fixed_location
        user.save()

        messages.success(request, "Cập nhật vị trí làm việc thành công.")
        return redirect('profile')
    except Exception as e:
        messages.error(request, f"Lỗi khi cập nhật vị trí: {str(e)}")
        return redirect('profile')


@login_required
def attendance(request):
    """
    Hiển thị lịch sử điểm danh của người dùng trong 45 ngày gần nhất.
    """
    user = request.user

    # Lấy lịch sử check-in/check-out (45 ngày gần nhất)
    end_date = timezone.now().date()
    start_date = end_date - timezone.timedelta(days=45)

    # Lọc theo ngày nếu có
    filter_date = request.GET.get('date')
    if filter_date:
        try:
            filter_date = timezone.datetime.strptime(filter_date, '%Y-%m-%d').date()
            attendance_records = CheckInCheckOut.objects.filter(
                user=user,
                date=filter_date
            ).order_by('-date')
        except ValueError:
            messages.error(request, "Định dạng ngày không hợp lệ.")
            attendance_records = CheckInCheckOut.objects.filter(
                user=user,
                date__range=[start_date, end_date]
            ).order_by('-date')
    else:
        attendance_records = CheckInCheckOut.objects.filter(
            user=user,
            date__range=[start_date, end_date]
        ).order_by('-date')

    # Tính toán thống kê
    total_days = (end_date - start_date).days + 1
    present_days = attendance_records.filter(checkin_time__isnull=False).count()
    absent_days = total_days - present_days
    valid_checkins = attendance_records.filter(is_valid_checkin=True).count()
    valid_checkouts = attendance_records.filter(is_valid_checkout=True).count()

    context = {
        'attendance_records': attendance_records,
        'start_date': start_date,
        'end_date': end_date,
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'valid_checkins': valid_checkins,
        'valid_checkouts': valid_checkouts,
        'attendance_rate': round(present_days / total_days * 100, 2) if total_days > 0 else 0,
    }

    return render(request, "main/pages/users/attendance.html", context)
