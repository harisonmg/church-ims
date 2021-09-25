from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Person


class PeopleListView(LoginRequiredMixin, ListView):
    context_object_name = "people"
    model = Person
    paginate_by = 10
    template_name = "people/people_list.html"
