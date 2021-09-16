from django.urls import path

from . import views

app_name = "accounts"

allauth_urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="account_signup"),
    path("login/", views.LoginView.as_view(), name="account_login"),
]

urlpatterns = []
