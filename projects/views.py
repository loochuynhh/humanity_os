from django.shortcuts import render
from django.http import HttpResponse


def project_list(request):
    return HttpResponse("Danh sách dự án.")


def project_detail(request, project_id):
    return HttpResponse(f"Chi tiết dự án có ID: {project_id}")
