from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path(
        "login_success/", views.LoginSuccessRedirectView.as_view(), name="login_success"
    ),
    path(
        "settings/update/", views.SettingsUpdateView.as_view(), name="settings_update"
    ),
    path("settings/", views.SettingsDetailView.as_view(), name="settings_detail"),
    path(
        "profile/<slug:username>/superuser_update/",
        views.ProfileSuperuserUpdateView.as_view(),
        name="profile_superuser_update",
    ),
    path(
        "profile/<slug:username>/update/",
        views.ProfileSelfUpdateView.as_view(),
        name="profile_self_update",
    ),
    path(
        "profile/<slug:username>/",
        views.ProfileDetailView.as_view(),
        name="profile_detail",
    ),
]
