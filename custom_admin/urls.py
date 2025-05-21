from django.urls import path
from custom_admin import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from users import views as users_views

app_name = 'custom_admin'

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path('update-fixed-location/', views.update_fixed_location, name='update_fixed_location'),
    path('search/', views.search, name='search'),
]
