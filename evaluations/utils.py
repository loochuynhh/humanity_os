from django.db.models import Q
from .models import FormResponses

def calculate_feedback_metrics(responses):
    total_reviews = responses.count()
    positive_rate = 0
    average_score = 0
    valid_responses = 0

    for response in responses.filter(answer_type="numeric"):
        try:
            score = float(response.answer)
            average_score += score
            valid_responses += 1
            if score >= 3:
                positive_rate += 1
        except ValueError:
            pass

    positive_rate = (positive_rate / total_reviews * 100) if total_reviews > 0 else 0
    average_score = (average_score / valid_responses) if valid_responses > 0 else 0

    return {
        'total_reviews': total_reviews,
        'positive_rate': round(positive_rate, 1),
        'average_score': average_score,
    }

def get_staff_feedback_queryset(user, is_received=True):
    if is_received:
        return FormResponses.objects.filter(
            target_user=user,
            form__type='review'  # Chỉ lấy review cho Đánh giá từ Quản lý
        ).select_related('form', 'user', 'question')
    return FormResponses.objects.filter(
        user=user,
        form__type__in=['peer', 'feedback']  # Chỉ lấy peer và feedback cho Đã gửi
    ).select_related('form', 'target_user', 'question')

def is_anonymous_response(response):
    """Kiểm tra xem đánh giá có cần ẩn danh không"""
    return response.form.type == 'feedback'  # Chỉ feedback ẩn danh