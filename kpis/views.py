from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Count, Q
from .models import EmployeeKPIs


def kpi_list(request):
    return HttpResponse("Danh sách KPI.")


def kpi_detail(request, kpi_id):
    return HttpResponse(f"Chi tiết KPI có ID: {kpi_id}")


@login_required
def personal_kpis(request):
    """Hiển thị trang KPI cá nhân"""
    kpis = EmployeeKPIs.objects.filter(user=request.user).select_related('kpi')

    today = timezone.now()
    current_month = f"{today.strftime('%Y-%m')}"
    monthly_kpis = kpis.filter(time_period__startswith=current_month)

    total_kpis = monthly_kpis.count()
    achieved_kpis = monthly_kpis.filter(evaluation="Achieved").count()
    monthly_completion_rate = (achieved_kpis / total_kpis * 100) if total_kpis > 0 else 0

    average_score = 0
    valid_kpis = 0
    for kpi in monthly_kpis:
        try:
            if kpi.actual_value and kpi.target_value:
                actual = float(kpi.actual_value)
                target = float(kpi.target_value)
                score = min(actual / target * 100, 100)
                average_score += score
                valid_kpis += 1
        except ValueError:
            pass
    average_score = average_score / valid_kpis if valid_kpis > 0 else 0

    periods = kpis.values_list('time_period', flat=True).distinct()

    context = {
        'kpis': kpis,
        'monthly_completion_rate': round(monthly_completion_rate, 1),
        'achieved_kpis': achieved_kpis,
        'total_kpis': total_kpis,
        'average_score': average_score,
        'periods': periods,
    }
    return render(request, 'main/pages/kpis/personal_kpis.html', context)

@require_POST
@login_required
def update_kpi(request):
    """Cập nhật giá trị thực tế của KPI"""
    try:
        kpi_id = request.POST.get('kpi_id')
        actual_value = request.POST.get('actual_value')

        kpi = EmployeeKPIs.objects.get(id=kpi_id, user=request.user)
        if kpi.evaluation: 
            return JsonResponse({'success': False, 'error': 'KPI đã được đánh giá, không thể chỉnh sửa'}, status=403)

        kpi.actual_value = actual_value
        kpi.evaluate()  
        kpi.save()

        return JsonResponse({
            'success': True,
            'actual_value': kpi.actual_value,
            'evaluation': kpi.evaluation,
        })
    except EmployeeKPIs.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'KPI không tồn tại hoặc không có quyền'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)