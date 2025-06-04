from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Nhân hai giá trị với nhau"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
    
@register.filter
def divide(value, arg):
    """Chia hai giá trị cho nhau"""
    try:
        return float(value) / float(arg) if float(arg) != 0 else 0
    except (ValueError, TypeError):
        return 0

@register.filter
def calculate_progress(completed, total):
    """Tính phần trăm hoàn thành"""
    try:
        if int(total) > 0:
            return round(float(completed) / float(total) * 100, 1)
        return 0
    except (ValueError, TypeError):
        return 0 