from django.urls import path
from . import views

urlpatterns = [
  path("", views.index, name="index"),
  path("user/login", views.login_view, name="user_login"),
  path("user/register", views.register_view, name="register_view"),
  path("dashboard", views.dashboard, name="dashboard")
]