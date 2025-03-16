from django.urls import path
from . import views

urlpatterns = [
    path("", views.kpi_list, name="kpi_list"),
    path("<int:kpi_id>/", views.kpi_detail, name="kpi_detail"),
]
