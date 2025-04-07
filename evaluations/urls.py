from django.urls import path
from . import views

urlpatterns = [
    path("", views.evaluation_list, name="evaluation_list"),
    path("<int:evaluation_id>/", views.evaluation_detail, name="evaluation_detail"),
    path("manager-feedback/", views.manager_feedback, name="manager_feedback"),
    path("feedback-detail/", views.feedback_detail, name="feedback_detail"),
]
