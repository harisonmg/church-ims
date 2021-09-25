from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView

from .models import Person


class PeopleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    context_object_name = "people"
    model = Person
    paginate_by = 10
    permission_required = "people.view_person"
    template_name = "people/people_list.html"
