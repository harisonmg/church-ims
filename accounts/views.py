from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from extra_views import InlineFormSetFactory, UpdateWithInlinesView

from accounts.models import CustomUser

from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm
from .models import Profile


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse(
            "accounts:user_update", kwargs={"username": self.request.user.username}
        )


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


class UserProfileInline(InlineFormSetFactory):
    model = Profile
    form = UserProfileForm
    extra = 0

    def get_factory_kwargs(self):
        kwargs = super(UserProfileInline, self).get_factory_kwargs()
        kwargs.update(
            {
                "min_num": 1,
            }
        )
        return kwargs


class ProfileUpdateView(UpdateWithInlinesView):
    model = CustomUser
    inlines = [
        UserProfileInline,
    ]
    form_class = UserUpdateForm
    slug_field = "username"
    template_name = "accounts/user_update.html"

    def get_success_url(self):
        return self.object.get_absolute_url()


class UserDetailView(generic.DetailView):
    slug_field = "username"
    template_name = "accounts/user_detail.html"
    context_object_name = "user_information"
    queryset = get_user_model().objects.all()

    def get_object(self):
        current_username = self.kwargs.get("username")
        return get_object_or_404(get_user_model(), username=current_username)


@login_required
def profile_update(request, username):
    if request.method == "POST":
        # pass the current user's info to the form
        user = get_user_model().objects.get(username=username)
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user.profile)
        

        # save the data from both forms only when both inputs are valid
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Your profile has been updated")
            # avoid the redirect alert from browser when one reloads the page
            return redirect(
                "accounts:user_detail",
                username=user_form.cleaned_data.get('username')
            )

    else:
        user = get_user_model().objects.get(username=username)
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=user.profile)

    context = {"user_form": user_form, "profile_form": profile_form}

    return render(request, "accounts/profile.html", context)
