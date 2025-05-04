from django.urls import path
from . import views

app_name = 'kpis'

urlpatterns = [
    path('performance-dashboard/', views.performance_dashboard, name='performance_dashboard'),
    path('update/', views.update_kpi, name='update_kpi'),
    path('kpi-detail/<int:kpi_id>/', views.kpi_detail, name='kpi_detail'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]