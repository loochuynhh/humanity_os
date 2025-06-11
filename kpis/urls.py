from django.urls import path
from . import views

app_name = 'kpis'

urlpatterns = [
    path('performance-dashboard/', views.performance_dashboard, name='performance_dashboard'),
    path('kpi-detail/<int:kpi_id>/', views.kpi_detail, name='kpi_detail'),
]