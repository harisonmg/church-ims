from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView

from accounts.models import CustomUser
from people.models import Person

from .forms import ProfileForm


class LoginSuccessRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        user_profile = get_object_or_404(Person, user=self.request.user)
        if not user_profile.full_name:
            return reverse(
                "accounts:profile_self_update",
                kwargs={"username": user_profile.username},
            )
        return reverse("core:dashboard")


class ProfileSelfUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ProfileForm
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


class ProfileSuperuserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = ProfileForm
    slug_field = "username"
    template_name = "accounts/profile_update.html"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

    def get_object(self):
        return get_object_or_404(Person, username=self.kwargs.get("username"))

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Person
    slug_field = "username"
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile"

    def test_func(self):
        current_user = self.request.user
        person = self.get_object()
        if current_user.is_superuser or (current_user.person == person):
            return True
        return False

    def get_object(self):
        current_username = self.kwargs.get("username")
        return get_object_or_404(Person, username=current_username)


class SettingsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    fields = ("username", "phone_number")
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


class SettingsDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
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
