from django.urls import path
from projects import views

app_name = 'projects'

urlpatterns = [
    # Existing paths
    path('', views.project_list, name='project_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    # Task assignments
    path('assignments/', views.task_assignment_list, name='task_assignment_list'),
    path('assignments/<int:assignment_id>/', views.task_assignment_detail, name='task_assignment_detail'),
    # APIs
    path('api/start-task-timer/', views.start_task_timer, name='start_task_timer'),
    path('api/stop-task-timer/', views.stop_task_timer, name='stop_task_timer'),
    # New API endpoint for AI suggestion
    path('api/suggest-user-for-task/', views.suggest_user_for_task, name='suggest_user_for_task'),
] 