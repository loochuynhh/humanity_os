from django.urls import path
from . import views

urlpatterns = [
    path('tasks/all/', views.all_tasks, name='all_tasks'),
    path('tasks/my-tasks/', views.my_tasks, name='my_tasks'),
    path('tasks/update-status/', views.update_status, name='update_status'),
    path('tasks/toggle-time/', views.toggle_time, name='toggle_time'),
    path('tasks/update-details/', views.update_task_details, name='update_task_details'),
    path('tasks/request-deadline-extension/', views.request_deadline_extension, name='request_deadline_extension'),
    path('tasks/extend-deadline/<int:task_id>/', views.extend_deadline, name='extend_deadline'),
    path("time-tracking/", views.time_tracking, name="time_tracking"),
    
    path('all/', views.all_projects, name='all_projects'),
    path('my-projects/', views.my_projects, name='my_projects'),
    path('team-members/', views.team_members, name='team_members'),
    path('team-members/data/', views.team_members_data, name='team_members_data'),
    path('progress/', views.project_progress, name='project_progress'),
    path('progress/data/', views.project_progress_data, name='project_progress_data'),
]