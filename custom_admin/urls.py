from django.urls import path
from custom_admin import views

app_name = 'custom_admin'

urlpatterns = [
    path("", views.index, name="index"),
    path("logout/", views.logout_view, name="logout"),
]