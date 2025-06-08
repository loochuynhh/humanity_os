from django.db.models import Q
from .models import FormResponses

def calculate_feedback_metrics(responses):
    # Sửa lỗi khi responses là list thay vì queryset
    total_reviews = len(responses)
    positive_rate = 0
    average_score = 0
    valid_responses = 0
    scores = []
    
    # Chỉ tính các response có numeric answer
    for response in [r for r in responses if r.answer_type == "numeric"]:
        try:
            score = float(response.answer)
            scores.append(score)
            average_score += score
            valid_responses += 1
            if score >= 3:
                positive_rate += 1
        except ValueError:
            pass

    positive_rate = (positive_rate / total_reviews * 100) if total_reviews > 0 else 0
    average_score = (average_score / valid_responses) if valid_responses > 0 else None
    highest_score = max(scores) if scores else None
    lowest_score = min(scores) if scores else None

    return {
        'total_reviews': total_reviews,
        'positive_rate': round(positive_rate, 1),
        'feedback_score': average_score,  # Thay average_score thành feedback_score
        'highest_score': highest_score,
        'lowest_score': lowest_score,
        'responses': responses,  # Trả về danh sách responses
    }

def get_staff_feedback_queryset(user, is_received=True, start_date=None, end_date=None):
    """Lấy danh sách đánh giá theo loại, loại bỏ các bản ghi trùng lặp"""
    if is_received:
        # Chỉ lấy review từ quản lý dành cho user
        base_query = FormResponses.objects.filter(
            target_user=user,
            form__type='review',
            answer_type='numeric'
        ).select_related('form', 'user', 'question')
    else:
        # Chỉ lấy peer và feedback mà user đã gửi
        base_query = FormResponses.objects.filter(
            user=user,
            form__type__in=['peer', 'feedback'],
            answer_type='numeric'
        ).select_related('form', 'target_user', 'question')

    # Lọc theo khoảng thời gian nếu có
    if start_date and end_date:
        base_query = base_query.filter(created_at__range=[start_date, end_date])

    # Loại bỏ trùng lặp bằng cách chỉ lấy một bản ghi cho mỗi (form, user, target_user)
    distinct_responses = {}
    for response in base_query:
        key = (response.form_id, response.user_id, response.target_user_id)
        if key not in distinct_responses:
            distinct_responses[key] = response

    return list(distinct_responses.values())

def is_anonymous_response(response):
    """Kiểm tra xem đánh giá có cần ẩn danh không"""
    return response.form.type == 'feedback'  # Chỉ feedback ẩn danh
