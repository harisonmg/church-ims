from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

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


class PersonCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Person
    fields = ["username", "full_name"]
    permission_required = "people.add_person"
    success_message = "%(username)s's information has been added successfully."
    template_name = "people/person_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "add"
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(username=cleaned_data["username"])


class PersonDetailView(LoginRequiredMixin, TemplateView):
    template_name = "people/person_detail.html"


class PersonUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Person
    fields = ["username", "full_name"]
    permission_required = "people.change_person"
    slug_field = "username"
    slug_url_kwarg = "username"
    success_message = "%(username)s's information has been updated successfully."
    template_name = "people/person_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "update"
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(username=cleaned_data["username"])
