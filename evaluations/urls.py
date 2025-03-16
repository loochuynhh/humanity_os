from django.urls import path
from . import views

urlpatterns = [
    path("", views.evaluation_list, name="evaluation_list"),
    path("<int:evaluation_id>/", views.evaluation_detail, name="evaluation_detail"),
]
