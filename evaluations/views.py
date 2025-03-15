from django.shortcuts import render
from django.http import HttpResponse

def evaluation_list(request):
  return HttpResponse("Danh sách đánh giá.")

def evaluation_detail(request, evaluation_id):
  return HttpResponse(f"Chi tiết đánh giá có ID: {evaluation_id}")