from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class PeopleListView(LoginRequiredMixin, TemplateView):
    template_name = "people/people_list.html"
