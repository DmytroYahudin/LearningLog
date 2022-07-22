from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path(
        "logout/",
        LogoutView.as_view(template_name="my_notes/index.html"),
        name="logout",
    ),
    path(
        "register/",
        views.SignUpView.as_view(template_name="users/register.html"),
        name="register",
    ),
]
