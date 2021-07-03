from allauth.account import views as allauth_views
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from accounts.models import CustomUser
from people.models import Person

from .forms import CustomUserCreationForm, CustomUserUpdateForm


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"


class LoginSuccessRedirectView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        user_profile = get_object_or_404(Person, user=self.request.user)
        if not user_profile.full_name:
            return reverse(
                "accounts:profile_update", kwargs={"username": user_profile.username}
            )
        return reverse("core:dashboard")


class LogoutView(auth_views.LogoutView):
    template_name = "accounts/logout.html"


class PasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy("accounts:password_change_done")
    template_name = "accounts/password_change.html"


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"


class PasswordResetView(auth_views.PasswordResetView):
    success_url = reverse_lazy("accounts:password_reset_done")
    email_template_name = "accounts/password_reset_email.html"
    template_name = "accounts/password_reset.html"


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")
    template_name = "accounts/password_reset_confirm.html"


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/register.html"


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Person
    fields = ("username", "full_name", "dob", "gender")
    slug_field = "username"
    template_name = "accounts/profile_update.html"

    def test_func(self):
        person = self.get_object()
        if self.request.user.person == person:
            return True
        return False

    def get_object(self):
        current_username = self.kwargs.get("username")
        return get_object_or_404(Person, username=current_username)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.user = self.request.user
        current_username = form.cleaned_data["username"]
        self.success_url = reverse(
            "accounts:profile_detail", kwargs={"username": current_username}
        )
        return super().form_valid(form)


class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Person
    slug_field = "username"
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile"

    def test_func(self):
        person = self.get_object()
        if self.request.user.person == person:
            return True
        return False

    def get_object(self):
        current_username = self.kwargs.get("username")
        return get_object_or_404(Person, username=current_username)


class SettingsUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    slug_field = "username"
    template_name = "accounts/settings_update.html"

    def test_func(self):
        current_user = self.get_object()
        if self.request.user == current_user:
            return True
        return False

    def get_object(self):
        return get_object_or_404(CustomUser, pk=self.request.user.pk)

    def get_success_url(self):
        return reverse("accounts:settings_detail")


class SettingsDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    slug_field = "username"
    template_name = "accounts/settings_detail.html"
    context_object_name = "settings"
    queryset = get_user_model().objects.all()

    def test_func(self):
        current_user = self.get_object()
        if self.request.user == current_user:
            return True
        return False

    def get_object(self):
        return get_object_or_404(CustomUser, pk=self.request.user.pk)
