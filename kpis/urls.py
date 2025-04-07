from django.urls import path
from . import views

urlpatterns = [
    path("", views.kpi_list, name="kpi_list"),
    path("<int:kpi_id>/", views.kpi_detail, name="kpi_detail"),
    path("personal/", views.personal_kpis, name="personal_kpis"),
    path("update/", views.update_kpi, name="update_kpi"),
]
