from django.urls import path
from django.contrib.auth.views import LoginView
from .views import register_view, profile_view, update_profile, logout_view
from .forms import LoginForm

urlpatterns = [
    path("accounts/register/", register_view, name="register"),
    path(
        "accounts/login/",
        LoginView.as_view(authentication_form=LoginForm),
        name="login",
    ),
    path("accounts/logout/", logout_view, name="logout"),
    path("user/profile/", profile_view, name="profile"),
    path("user/profile/edit/", update_profile, name="update_profile"),
]
