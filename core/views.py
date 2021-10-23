from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView


class IndexView(TemplateView):
    template_name = "core/index.html"


class LoginRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.personal_details is None:
            url = reverse("people:adult_self_register")
        else:
            url = reverse("core:dashboard")
        return url


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"
