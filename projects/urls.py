from django.urls import path
from . import views

urlpatterns = [
    path('tasks/all/', views.all_tasks, name='all_tasks'),
    path('tasks/my-tasks/', views.my_tasks, name='my_tasks'),
    path('tasks/overdue/', views.overdue_tasks, name='overdue_tasks'),
    path('tasks/update-status/', views.update_status, name='update_status'),
    path('tasks/toggle-time/', views.toggle_time, name='toggle_time'),
    path('tasks/extend-deadline/<int:task_id>/', views.extend_deadline, name='extend_deadline'),
]