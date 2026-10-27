from django.urls import path

from . import views

# Each line is one address the React site can call, e.g. /api/login/
urlpatterns = [
    path("csrf/", views.csrf, name="csrf"),
    path("me/", views.me, name="me"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
