from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

name = "accounts"
urlpatterns = [
    path("profile/", views.ProfileView, name="profile"),
    path("members/", views.MembersView, name="members"),
    # Authentication URLs
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
