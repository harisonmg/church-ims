from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "core/index.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"
