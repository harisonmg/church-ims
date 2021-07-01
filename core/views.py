from django.views.generic import TemplateView

from children.views import ChildrenByUserListView


class IndexView(TemplateView):
    template_name = "core/index.html"


class DashboardView(ChildrenByUserListView):
    template_name = "core/dashboard.html"
