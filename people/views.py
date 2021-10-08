from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, TemplateView

from extra_views import SearchableListMixin

from .models import Person


class PeopleListView(
    LoginRequiredMixin, PermissionRequiredMixin, SearchableListMixin, ListView
):
    context_object_name = "people"
    model = Person
    paginate_by = 10
    permission_required = "people.view_person"
    search_fields = ["username", "full_name"]
    template_name = "people/people_list.html"


class PersonCreateView(LoginRequiredMixin, TemplateView):
    template_name = "people/person_form.html"
