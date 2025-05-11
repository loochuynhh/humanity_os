from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models import Avg, Count, Q
from .models import Forms, FormQuestions, FormResponses
from users.models import Users
from projects.models import TeamProjectMembership
from .utils import calculate_feedback_metrics, get_staff_feedback_queryset, is_anonymous_response


@login_required
def feedback_detail(request):
    response_id = request.GET.get('response_id')
    if not response_id or not response_id.isdigit():
        return JsonResponse({'success': False, 'error': 'ID đánh giá không hợp lệ'}, status=400)
    try:
        response = FormResponses.objects.filter(id=response_id).first()
        if not response:
            return JsonResponse({'success': False, 'error': 'Không tìm thấy đánh giá'}, status=404)

        # Kiểm tra quyền truy cập: người dùng phải là target_user hoặc user của response
        if response.target_user != request.user and response.user != request.user:
            return JsonResponse({'success': False, 'error': 'Không có quyền xem đánh giá này'}, status=403)

        # Lấy tất cả câu hỏi trong form
        questions = FormQuestions.objects.filter(form=response.form)

        # Lấy tất cả câu trả lời của response này
        answers = FormResponses.objects.filter(
            form=response.form,
            user=response.user,
            target_user=response.target_user
        ).select_related('question')

        # Tạo map câu hỏi -> câu trả lời
        answer_map = {answer.question_id: answer.answer for answer in answers}

        context = {
            'response': response,
            'questions': questions,
            'answer_map': answer_map,
            'is_anonymous': is_anonymous_response(response),
        }
        html = render_to_string('main/pages/evaluations/feedback_detail.html', context)
        return JsonResponse({'success': True, 'html': html})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
def submit_form(request):
    if request.method == "GET":
        form_id = request.GET.get('form_id')
        try:
            form = Forms.objects.get(id=form_id, status="open", deadline__gte=timezone.now())

            # Kiểm tra quyền truy cập form review
            if form.type == 'review' and not (request.user.role == 'Admin' or request.user.role == 'Manager'):
                return JsonResponse({
                    'success': False,
                    'error': 'Chỉ quản lý mới có quyền thực hiện đánh giá review'
                }, status=403)

            questions = FormQuestions.objects.filter(form=form)

            # Lấy danh sách người dùng target dựa trên loại form và vai trò
            if form.type == 'review':
                # Quản lý/Admin chỉ có thể đánh giá nhân viên
                target_users = Users.objects.filter(
                    status='Active',
                    role='Employee'
                ).exclude(id=request.user.id).distinct()
            else:
                # Với form peer và feedback, tất cả người dùng đều có thể đánh giá
                target_users = Users.objects.filter(
                    status='Active'
                ).exclude(id=request.user.id).distinct()

                # Nếu là form peer, chỉ lấy các thành viên cùng dự án
                if form.type == 'peer':
                    user_projects = TeamProjectMembership.objects.filter(
                        user=request.user
                    ).values_list('project_id', flat=True)

                    if user_projects:
                        target_users = target_users.filter(
                            teamprojectmembership__project_id__in=user_projects
                        ).distinct()

            context = {
                'form': form,
                'questions': questions,
                'target_users': target_users,
            }
            html = render_to_string('main/pages/evaluations/submit_form.html', context)
            return JsonResponse({'success': True, 'html': html})
        except Forms.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Form không tồn tại hoặc đã đóng'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    if request.method != "POST":
        return JsonResponse({'success': False, 'error': 'Phương thức không hợp lệ'}, status=400)

    form_id = request.POST.get('form_id')
    target_user_id = request.POST.get('target_user_id')

    try:
        form = Forms.objects.get(id=form_id, status="open", deadline__gte=timezone.now())

        # Kiểm tra quyền truy cập form review
        if form.type == 'review' and not (request.user.role == 'Admin' or request.user.role == 'Manager'):
            return JsonResponse({
                'success': False,
                'error': 'Chỉ quản lý mới có quyền thực hiện đánh giá review'
            }, status=403)

        target_user = Users.objects.get(id=target_user_id)

        # Kiểm tra quyền đánh giá đúng loại đối tượng
        if form.type == 'review' and target_user.role != 'Employee':
            return JsonResponse({
                'success': False,
                'error': 'Quản lý chỉ có thể đánh giá review cho nhân viên'
            }, status=400)

        if target_user == request.user:
            return JsonResponse({'success': False, 'error': 'Không thể đánh giá bản thân'}, status=400)

        # Kiểm tra đã gửi đánh giá cho target_user trong form này chưa
        if FormResponses.objects.filter(
            form=form,
            user=request.user,
            target_user=target_user
        ).exists():
            return JsonResponse({'success': False, 'error': 'Bạn đã gửi đánh giá cho người này trong form này'}, status=400)

        questions = FormQuestions.objects.filter(form=form)
        for question in questions:
            answer_key = f'answer_{question.id}'
            answer = request.POST.get(answer_key, '')
            if answer:
                FormResponses.objects.create(
                    form=form,
                    question=question,
                    user=request.user,
                    target_user=target_user,
                    answer=answer,
                    answer_type='numeric' if question.question_type == 'rating' else 'text',
                )

        return JsonResponse({'success': True, 'message': 'Đánh giá đã được gửi!'})
    except Forms.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Form không tồn tại hoặc đã đóng'}, status=404)
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Người dùng không tồn tại'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def evaluations(request):
    # Đánh giá từ Quản lý - chỉ lấy unique responses theo form, user, target_user
    responses = get_staff_feedback_queryset(request.user, is_received=True)
    metrics = calculate_feedback_metrics(responses)

    # Lịch sử đánh giá
    received_responses = FormResponses.objects.filter(
        target_user=request.user,
        form__type__in=['peer', 'feedback']
    ).select_related('form', 'user')

    # Loại bỏ trùng lặp trong received_responses
    distinct_received = {}
    for resp in received_responses:
        key = (resp.form_id, resp.user_id, resp.target_user_id)
        if key not in distinct_received:
            distinct_received[key] = resp

    received_responses = list(distinct_received.values())

    # Đánh giá đã gửi
    sent_responses = get_staff_feedback_queryset(request.user, is_received=False)

    # Gửi đánh giá - Lọc các form theo quyền hạn người dùng
    if request.user.role == 'Admin' or request.user.role == 'Manager':
        # Admin và Manager có thể thấy tất cả các loại form
        forms = Forms.objects.filter(
            status="open",
            deadline__gte=timezone.now()
        ).order_by('deadline')
    else:
        # Nhân viên bình thường chỉ thấy form peer và feedback
        forms = Forms.objects.filter(
            status="open",
            deadline__gte=timezone.now(),
            type__in=['peer', 'feedback']
        ).order_by('deadline')

    # Danh sách form đã hoàn thành (chỉ lấy mỗi form 1 lần)
    completed_forms = FormResponses.objects.filter(
        user=request.user,
        form__status="open"
    ).values('form_id', 'target_user_id').distinct()

    # Chỉ lấy các form_id duy nhất
    unique_completed_forms = set(form['form_id'] for form in completed_forms)

    context = {
        'responses': responses,
        'periods': Forms.objects.values_list('period', flat=True).distinct(),
        **metrics,
        'received_responses': received_responses,
        'sent_responses': sent_responses,
        'forms': forms,
        'total_forms': forms.count(),
        'completed_forms_count': len(unique_completed_forms),
        'completed_forms': list(unique_completed_forms),
    }
    return render(request, 'main/pages/evaluations/evaluations.html', context)
