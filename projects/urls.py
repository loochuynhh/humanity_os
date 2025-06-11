from django.urls import path
from .views import (
    all_projects,
    project_detail,
    all_tasks,
    my_tasks,
    task_detail,
    update_task_details,
    request_deadline_extension,
    time_tracking,
    update_assignment_status,
    project_calendar,
    project_calendar_events,
    create_time_entry,
    suggest_user_for_task,
    suggest_time_for_task,
)

urlpatterns = [
    path("projects/", all_projects, name="all_projects"),
    path("projects/<int:project_id>/", project_detail, name="project_detail"),
    path("project-calendar/", project_calendar, name="project_calendar"),
    path("project-calendar-events/", project_calendar_events, name="project_calendar_events"),

    path("tasks/", all_tasks, name="all_tasks"),
    path("my-tasks/", my_tasks, name="my_tasks"),
    path("task/<int:task_id>/", task_detail, name="task_detail"),
    path("update-task-details/", update_task_details, name="update_task_details"),
    path("request-deadline-extension/", request_deadline_extension, name="request_deadline_extension"),

    path("time-tracking/", time_tracking, name="time_tracking"),
    path("create_time_entry/", create_time_entry, name="create_time_entry"),
    path("update_assignment_status/", update_assignment_status, name="update_assignment_status"),

    path("api/suggest-user-for-task/", suggest_user_for_task, name="suggest_user_for_task"),
    path("api/suggest-time-for-task/", suggest_time_for_task, name="suggest_time_for_task"),
]
