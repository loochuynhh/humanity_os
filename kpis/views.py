from django.shortcuts import render
from django.http import HttpResponse


def kpi_list(request):
    return HttpResponse("Danh sách KPI.")


def kpi_detail(request, kpi_id):
    return HttpResponse(f"Chi tiết KPI có ID: {kpi_id}")
