from django.shortcuts import render
from django.http import HttpResponse

def user_list(request):
  return HttpResponse("Danh sách người dùng.")

def user_detail(request, user_id):
  return HttpResponse(f"Chi tiết người dùng có ID: {user_id}")
