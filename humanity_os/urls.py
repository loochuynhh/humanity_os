"""humanity_os URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from .views import home
from django.conf.urls.static import static
from django.conf import settings
from projects.views import suggest_user_for_task

urlpatterns = [
    path("", home, name="home"),
    path("admin/dashboard/", include("custom_admin.urls")),
    path("admin/", admin.site.urls), 
    path("evaluations/", include(("evaluations.urls", "evaluations"), namespace="evaluations")),
    path("kpis/", include(("kpis.urls", "kpis"), namespace="kpis")),
    path("projects/", include(("projects.urls", "projects"), namespace="projects")),
    path("users/", include(("users.urls", "users"), namespace="users")),
    path("api/projects/", include("projects.urls")),
    path("api/suggest-user-for-task/", suggest_user_for_task, name="suggest_user_for_task"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
