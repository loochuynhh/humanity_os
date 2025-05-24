from django.urls import path
from .views import (
    all_projects,
    project_detail,
    all_tasks,
    my_tasks,
    task_detail,
    update_status,
    toggle_time,
    update_task_details,
    request_deadline_extension,
    extend_deadline,
    time_tracking,
    update_time_entry,
    update_assignment_status,
    team_members_data,
    project_calendar,
    project_calendar_events,
    project_statistics,
    project_statistics_data,
    project_progress,
    project_progress_data,
    create_time_entry,
    update_time_entry,
    update_assignment_status,
    suggest_user_for_task,
)

urlpatterns = [
    # Các route dự án
    path("projects/", all_projects, name="all_projects"),
    path("projects/<int:project_id>/", project_detail, name="project_detail"),
    path("project-statistics/", project_statistics, name="project_statistics"),
    path("project-statistics-data/", project_statistics_data, name="project_statistics_data"),
    path("project-progress/", project_progress, name="project_progress"),
    path("project-progress-data/", project_progress_data, name="project_progress_data"),
    path("team-members-data/", team_members_data, name="team_members_data"),

    # Calendar
    path("project-calendar/", project_calendar, name="project_calendar"),
    path("project-calendar-events/", project_calendar_events, name="project_calendar_events"),

    # Các route task
    path("tasks/", all_tasks, name="all_tasks"),
    path("my-tasks/", my_tasks, name="my_tasks"),
    path("task/<int:task_id>/", task_detail, name="task_detail"),
    path("update-status/", update_status, name="update_status"),
    path("toggle-time/", toggle_time, name="toggle_time"),
    path("update-task-details/", update_task_details, name="update_task_details"),
    path("request-deadline-extension/", request_deadline_extension, name="request_deadline_extension"),
    path("extend-deadline/<int:task_id>/", extend_deadline, name="extend_deadline"),

    # Thời gian làm việc
    path("time-tracking/", time_tracking, name="time_tracking"),
    path("update-time-entry/", update_time_entry, name="update_time_entry"),
    path("update-assignment-status/", update_assignment_status, name="update_assignment_status"),
    path('create_time_entry/', create_time_entry, name='create_time_entry'),
    path('update_time_entry/', update_time_entry, name='update_time_entry'),
    path('update_assignment_status/', update_assignment_status, name='update_assignment_status'),

    # API
    path("api/suggest-user-for-task/", suggest_user_for_task, name="suggest_user_for_task"),
]
