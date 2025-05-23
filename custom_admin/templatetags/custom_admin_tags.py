import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='get_td_class')
def get_td_class(value):
    """
    Trích xuất thuộc tính class từ một chuỗi HTML <td>.
    Giả sử 'value' là một chuỗi dạng '<td class="..." ...>...</td>'.
    """
    if not isinstance(value, str):
        value = str(value)
    match = re.search(r'<td[^>]*class="([^"]*)"', value)
    if match:
        return match.group(1)
    return ''

@register.filter(name='get_rendered_content')
def get_rendered_content(value):
    """
    Trích xuất nội dung bên trong một chuỗi HTML <td>.
    Giả sử 'value' là một chuỗi dạng '<td ...>(.*?)</td>'.
    """
    if not isinstance(value, str):
        value = str(value)
    # Sử dụng non-greedy match (.*?) và DOTALL (re.S) để xử lý nội dung trên nhiều dòng
    match = re.search(r'<td[^>]*>(.*)</td>', value, re.DOTALL | re.S)
    if match:
        return mark_safe(match.group(1).strip())
    return value # Trả về giá trị gốc nếu không khớp 