from django.views.generic import TemplateView


class SignupView(TemplateView):
    template_name = "accounts/signup.html"


class LoginView(TemplateView):
    template_name = "accounts/login.html"
