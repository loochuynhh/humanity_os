from django.contrib import admin
from django.urls import path, include
from .views import index
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", index, name="home"),
    path("admin/", admin.site.urls),
    path("dashboard/", include("custom_admin.urls")),
    path("companies/", include("companies.urls")),
    path("evaluations/", include("evaluations.urls")),
    path("kpis/", include("kpis.urls")),
    path("projects/", include("projects.urls")),
    path("users/", include("users.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
