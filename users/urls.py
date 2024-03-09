from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    AboutMeView,
    ChangeMeView,
    ChangeUserView,
    CreateUserView,
    ListUsersView,
    LoginView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("aboutme/", AboutMeView.as_view(), name="aboutme"),
    path("changeme/", ChangeMeView.as_view(), name="change_me"),
    path("", ListUsersView.as_view(), name="users"),
    path("<int:pk>", ChangeUserView.as_view(), name="user-edit"),
    path("new/", CreateUserView.as_view(), name="user-new"),
]
