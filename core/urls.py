from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("login/redirect/", views.LoginRedirectView.as_view(), name="login_redirect"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("", views.IndexView.as_view(), name="index"),
]
