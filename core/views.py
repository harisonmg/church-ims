from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from children.views import ChildrenByUserListView


class IndexView(TemplateView):
    template_name = "core/index.html"


class DashboardView(ChildrenByUserListView):
    template_name = "core/dashboard.html"
