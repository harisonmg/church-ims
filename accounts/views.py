from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm

# from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"


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


# class UserProfileInline(InlineFormSetFactory):
#     model = Person
#     form = UserProfileForm
#     extra = 0

#     def get_factory_kwargs(self):
#         kwargs = super(UserProfileInline,self).get_factory_kwargs()
#         kwargs.update({
#             "min_num": 1,
#             "fk_name": "created_by"
#         })
#         return kwargs


# class UserCreateView(CreateWithInlinesView):
#     model = CustomUser
#     inlines = [UserProfileInline,]
#     form_class = CustomUserCreationForm
#     success_url = "core:dashboard"
#     template_name = 'register_profile.html'


@login_required
def profile(request):
    if request.method == "POST":
        # pass the current user's info to the form
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)

        # save the data from both forms only when both inputs are valid
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Your profile has been updated")
            # avoid the redirect alert from browser when one reloads the page
            return redirect("accounts:profile")

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    context = {"user_form": user_form, "profile_form": profile_form}

    return render(request, "accounts/profile.html", context)
