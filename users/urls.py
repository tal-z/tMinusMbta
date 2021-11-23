# users/urls.py
from django.urls import path
from django.conf.urls import include, url
from users.views import index, dashboard, edit_dashboard, register, profile, delete_timer, move_up, move_down, edit_profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r"^dashboard/edit/", edit_dashboard, name="edit_dashboard"),
    path(r"dashboard/delete_timer/<str:timer_id>/", delete_timer, name="delete_timer"),
    path(r"dashboard/move_up/<str:timer_id>/", move_up, name="move_up"),
    path(r"dashboard/move_down/<str:timer_id>/", move_down, name="move_down"),
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^profile/edit/", edit_profile, name="edit_profile"),
    url(r"^profile/", profile, name="profile"),
    url(r"^register/", register, name="register"),
    url(r"^oauth/", include("social_django.urls", namespace="social")),
]