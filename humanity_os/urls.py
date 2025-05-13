"""humanity_os URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from .views import index, home
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path(
        "dashboard/",
        include(("custom_admin.urls", "custom_admin"), namespace="custom_admin"),
    ),
    path(
        "evaluations/",
        include(("evaluations.urls", "evaluations"), namespace="evaluations"),
    ),
    path("kpis/", include(("kpis.urls", "kpis"), namespace="kpis")),
    path("projects/", include(("projects.urls", "projects"), namespace="projects")),
    path("users/", include(("users.urls", "users"), namespace="users")),
    # API routes
    path("api/projects/", include("projects.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
