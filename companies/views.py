from django.shortcuts import render
from django.http import HttpResponse


def company_list(request):
    return HttpResponse("Company List Page - Update later")


def company_detail(request, id):
    return HttpResponse(f"Company Detail Page - ID: {id}")
