from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models import Avg, Count
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
        response = FormResponses.objects.get(id=response_id)
        # Kiểm tra quyền truy cập: người dùng phải là target_user hoặc user của response
        if response.target_user != request.user and response.user != request.user:
            return JsonResponse({'success': False, 'error': 'Không có quyền xem đánh giá này'}, status=403)
        questions = FormQuestions.objects.filter(form=response.form)
        context = {
            'response': response,
            'questions': questions,
            'is_anonymous': is_anonymous_response(response),
        }
        html = render_to_string('main/pages/evaluations/feedback_detail.html', context)
        return JsonResponse({'success': True, 'html': html})
    except FormResponses.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Không tìm thấy đánh giá'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    

@login_required
def submit_form(request):
    if request.method == "GET":
        form_id = request.GET.get('form_id')
        try:
            form = Forms.objects.get(id=form_id, status="open", deadline__gte=timezone.now())
            questions = FormQuestions.objects.filter(form=form)
            # Lấy danh sách dự án của người dùng hiện tại
            user_projects = TeamProjectMembership.objects.filter(user=request.user).values_list('project_id', flat=True)
            # Lấy danh sách user chung dự án, trừ người dùng hiện tại
            target_users = Users.objects.filter(
                projects__id__in=user_projects,
                role='staff'
            ).exclude(id=request.user.id).distinct()
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
        target_user = Users.objects.get(id=target_user_id, role='staff')
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
            answer_key = f'answer_{{question.id}}'
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
    # Đánh giá từ Quản lý
    responses = get_staff_feedback_queryset(request.user, is_received=True)
    metrics = calculate_feedback_metrics(responses)

    # Lịch sử đánh giá
    received_responses = FormResponses.objects.filter(
        target_user=request.user,
        form__type__in=['peer', 'feedback']
    ).select_related('form', 'user', 'question')
    sent_responses = get_staff_feedback_queryset(request.user, is_received=False)

    # Gửi đánh giá
    forms = Forms.objects.filter(
        status="open",
        deadline__gte=timezone.now()
    ).order_by('deadline')
    completed_forms = FormResponses.objects.filter(
        user=request.user,
        form__status="open"
    ).values('form_id').distinct()

    context = {
        'responses': responses,
        'periods': Forms.objects.values_list('period', flat=True).distinct(),
        **metrics,
        'received_responses': received_responses,
        'sent_responses': sent_responses,
        'forms': forms,
        'total_forms': forms.count(),
        'completed_forms_count': len(completed_forms),
        'completed_forms': [form['form_id'] for form in completed_forms],
    }
    return render(request, 'main/pages/evaluations/evaluations.html', context)