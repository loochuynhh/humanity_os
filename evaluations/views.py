from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import FormResponses, FormQuestions


def evaluation_list(request):
    return HttpResponse("Danh sách đánh giá.")


def evaluation_detail(request, evaluation_id):
    return HttpResponse(f"Chi tiết đánh giá có ID: {evaluation_id}")


@login_required
def manager_feedback(request):
    """Hiển thị trang đánh giá từ quản lý"""
    responses = FormResponses.objects.filter(
        target_user=request.user,
        form__type="peer"  # Chỉ lấy đánh giá từ người khác (quản lý)
    ).select_related('form', 'user')

    # Tính tổng hợp
    total_reviews = responses.count()
    positive_rate = 0
    average_score = 0
    valid_responses = 0

    for response in responses:
        try:
            score = float(response.answer) if response.answer.isdigit() else None
            if score:
                average_score += score
                valid_responses += 1
                if score >= 3:  # Giả sử điểm >= 3/5 là tích cực
                    positive_rate += 1
        except ValueError:
            pass

    positive_rate = (positive_rate / total_reviews * 100) if total_reviews > 0 else 0
    average_score = (average_score / valid_responses) if valid_responses > 0 else 0

    periods = responses.values_list('form__period', flat=True).distinct()

    context = {
        'responses': responses,
        'total_reviews': total_reviews,
        'positive_rate': round(positive_rate, 1),
        'average_score': average_score,
        'periods': periods,
    }
    return render(request, 'main/pages/evaluations/manager_feedback.html', context)


@login_required
def feedback_detail(request):
    """Trả về chi tiết đánh giá qua AJAX"""
    response_id = request.GET.get('response_id')
    try:
        response = FormResponses.objects.get(id=response_id, target_user=request.user)
        questions = FormQuestions.objects.filter(form=response.form)
        context = {
            'response': response,
            'questions': questions,
        }
        html = render_to_string('main/pages/evaluations/feedback_detail.html', context)
        return JsonResponse({'success': True, 'html': html})
    except FormResponses.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Không tìm thấy đánh giá'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)