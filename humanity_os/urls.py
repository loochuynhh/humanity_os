from django.contrib import admin
from django.urls import path, include
from .views import index
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", index, name="home"),
    path("admin/", admin.site.urls),
    path(
        "dashboard/",
        include(("custom_admin.urls", "custom_admin"), namespace="custom_admin"),
    ),
    path("companies/", include(("companies.urls", "companies"), namespace="companies")),
    path(
        "evaluations/",
        include(("evaluations.urls", "evaluations"), namespace="evaluations"),
    ),
    path("kpis/", include(("kpis.urls", "kpis"), namespace="kpis")),
    path("projects/", include(("projects.urls", "projects"), namespace="projects")),
    path("users/", include(("users.urls", "users"), namespace="users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
