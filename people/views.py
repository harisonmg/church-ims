from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from extra_views import SearchableListMixin

from .forms import (
    AdultCreationForm,
    ChildCreationForm,
    InterpersonalRelationshipCreationForm,
    PersonCreationForm,
    PersonUpdateForm,
)
from .models import InterpersonalRelationship, Person


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
    form_class = PersonCreationForm
    permission_required = "people.add_person"
    success_message = "%(username)s's information has been added successfully."
    template_name = "people/person_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "add"
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(username=cleaned_data["username"])


class AdultCreateView(PersonCreateView):
    form_class = AdultCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["age_category"] = "an adult"
        return context


class AdultSelfRegisterView(AdultCreateView):
    permission_required = ()
    success_url = reverse_lazy("core:dashboard")
    template_name = "people/self_register_form.html"

    def form_valid(self, form):
        form.instance.user_account = self.request.user
        return super().form_valid(form)


class ChildCreateView(PersonCreateView):
    form_class = ChildCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["age_category"] = "a child"
        return context


class PersonDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Person
    permission_required = "people.view_person"
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "people/person_detail.html"


class PersonUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    form_class = PersonUpdateForm
    model = Person
    permission_required = "people.change_person"
    slug_field = "username"
    slug_url_kwarg = "username"
    success_message = "%(username)s's information has been updated successfully."
    template_name = "people/person_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "update"
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(username=cleaned_data["username"])


class RelationshipsListView(
    LoginRequiredMixin, PermissionRequiredMixin, SearchableListMixin, ListView
):
    context_object_name = "relationships"
    model = InterpersonalRelationship
    paginate_by = 10
    permission_required = "people.view_interpersonalrelationship"
    search_fields = ["person__username", "relative__username"]
    template_name = "people/relationships_list.html"


class RelationshipCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    form_class = InterpersonalRelationshipCreationForm
    permission_required = "people.add_interpersonalrelationship"
    success_message = "The relationship between %(people)s has been added successfully."
    success_url = reverse_lazy("people:relationships_list")
    template_name = "people/relationship_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        person = cleaned_data["person"]
        relative = cleaned_data["relative"]
        people = f"{person.username} and {relative.username}"
        return self.success_message % dict(people=people)
