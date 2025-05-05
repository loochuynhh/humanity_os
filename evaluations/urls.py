from django.urls import path
from . import views

urlpatterns = [
    path("", views.evaluations, name="evaluations"),
    path("feedback-detail/", views.feedback_detail, name="feedback_detail"),
    path("submit-form/", views.submit_form, name="submit_form"),
]