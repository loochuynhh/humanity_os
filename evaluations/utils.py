from django.db.models import Q
from .models import FormResponses

def calculate_feedback_metrics(responses):
    total_reviews = 0
    positive_count = 0
    normalized_score_sum = 0
    valid_responses = 0
    scores = []
    
    for response in responses:
        if response.answer_type == "numeric" and response.question.question_type == "rating":
            try:
                score = float(response.answer)
                max_score = response.question.max_score or 100  
                if max_score <= 0:
                    continue  
                total_reviews += 1
                scores.append(score)
                normalized_score = (score / max_score) * 100  
                normalized_score_sum += normalized_score
                valid_responses += 1
                if score >= 0.6 * max_score:  
                    positive_count += 1
            except (ValueError, TypeError):
                pass

    positive_rate = (positive_count / total_reviews * 100) if total_reviews > 0 else 0
    average_score = (normalized_score_sum / valid_responses) if valid_responses > 0 else 0
    highest_score = max(scores) if scores else None
    lowest_score = min(scores) if scores else None

    return {
        'total_reviews': total_reviews,
        'positive_rate': round(positive_rate, 1),
        'feedback_score': round(average_score, 1) if average_score else None,
        'highest_score': highest_score,
        'lowest_score': lowest_score,
        'responses': responses,
    }

def get_staff_feedback_queryset(user, is_received=True, start_date=None, end_date=None):
    """Lấy danh sách đánh giá theo loại, loại bỏ các bản ghi trùng lặp"""
    if is_received:
        base_query = FormResponses.objects.filter(
            target_user=user,
            form__type='review',
            answer_type='numeric'
        ).select_related('form', 'user', 'question')
    else:
        base_query = FormResponses.objects.filter(
            user=user,
            form__type__in=['peer', 'feedback'],
            answer_type='numeric'
        ).select_related('form', 'target_user', 'question')

    if start_date and end_date:
        base_query = base_query.filter(created_at__range=[start_date, end_date])

    distinct_responses = {}
    for response in base_query:
        key = (response.form_id, response.user_id, response.target_user_id)
        if key not in distinct_responses:
            distinct_responses[key] = response

    return list(distinct_responses.values())

def is_anonymous_response(response):
    """Kiểm tra xem đánh giá có cần ẩn danh không"""
    return response.form.type == 'feedback' 
