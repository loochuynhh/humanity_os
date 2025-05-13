from django.shortcuts import render, redirect
from django.http import HttpResponse


def index(request):
    return render(request, "main/index.html")


def home(request):
    if request.user.is_authenticated:
        return redirect("users:index")
    else:
        return redirect("users:login")
