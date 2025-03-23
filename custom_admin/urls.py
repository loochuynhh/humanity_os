from django.urls import path
from custom_admin import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path("", views.index, name="index"),
    path("billing/", views.billing, name="billing"),
    path("tables/", views.tables, name="tables"),
    path("vr/", views.vr, name="vr"),
    path("rtl/", views.rtl, name="rtl"),
    path("profile/", views.profile, name="profile"),
    # Authentication
    path("accounts/logout/", views.logout_view, name="logout"),
]
