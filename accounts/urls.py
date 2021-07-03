from django.urls import path, re_path

from . import views

app_name = "accounts"
contrib_auth = [
    # provided by Django
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

custom = [
    # custom
    path("register/", views.RegisterView.as_view(), name="register"),
]

urlpatterns = [    
    path("login_success/", views.LoginSuccessRedirectView.as_view(), name="login_success"),    
    path(
        "settings/update/", views.SettingsUpdateView.as_view(), name="settings_update"
    ),
    path("settings/", views.SettingsDetailView.as_view(), name="settings_detail"),
    path(
        "profile/<slug:username>/update/",
        views.ProfileUpdateView.as_view(),
        name="profile_update",
    ),
    path("profile/<slug:username>/", views.ProfileDetailView.as_view(), name="profile_detail"),
    path(
        "profile/<slug:username>/update/",
        views.ProfileUpdateView.as_view(),
        name="profile_update",
    ),
    path("profile/<slug:username>/", views.ProfileDetailView.as_view(), name="profile_detail"),
]
