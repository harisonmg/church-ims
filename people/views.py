from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from extra_views import SearchableListMixin

from .forms import (
    DUPLICATE_RELATIONSHIPS_ERROR,
    AdultCreationForm,
    ChildCreationForm,
    InterpersonalRelationshipCreationForm,
    ParentChildRelationshipCreationForm,
    PersonCreationForm,
    PersonUpdateForm,
)
from .models import InterpersonalRelationship, Person
from .utils import is_duplicate_interpersonal_relationship, is_duplicate_person


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
        if is_duplicate_person(form.instance):
            form.add_error(field=None, error="This person already exists")
            return self.form_invalid(form)
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
        form.instance.user = self.request.user
        return super().form_valid(form)


class ChildCreateView(PersonCreateView, UserPassesTestMixin):
    form_class = ChildCreationForm
    permission_required = ()
    success_url = reverse_lazy("core:dashboard")

    def test_func(self):
        return self.request.user.personal_details is not None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["age_category"] = "a child"
        return context

    def get_success_url(self, is_parent=False):
        if not is_parent:
            url = reverse_lazy(
                "people:parent_child_relationship_create",
                kwargs={"username": self.object.username},
            )
        else:
            url = super().get_success_url()
        return url

    def create_relationship(self):
        relationship = InterpersonalRelationship.objects.create(
            person=self.request.user.personal_details,
            relative=self.object,
            relation="PC",
            created_by=self.request.user,
        )
        people = f"{relationship.person} and {relationship.relative}"
        message = f"A parent-child relationship between {people} has been added."
        messages.info(self.request, message)

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.is_valid():
            is_parent = form.cleaned_data["is_parent"]
            if is_parent:
                self.create_relationship()
            return HttpResponseRedirect(self.get_success_url(is_parent))
        return response


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


class ParentChildRelationshipCreateView(RelationshipCreateView, UserPassesTestMixin):
    form_class = ParentChildRelationshipCreationForm
    permission_required = ()
    success_url = reverse_lazy("core:dashboard")
    success_message = "A parent-child relationship between %(people)s has been added."

    def test_func(self):
        return self.request.user.personal_details is not None

    def get_child(self):
        return get_object_or_404(Person, username=self.kwargs["username"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["child"] = self.get_child()
        return context

    def form_valid(self, form):
        form.instance.relative = self.get_child()
        form.instance.relation = "PC"
        if is_duplicate_interpersonal_relationship(form.instance):
            form.add_error(field=None, error=DUPLICATE_RELATIONSHIPS_ERROR)
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        people = f"{self.object.person} and {self.object.relative}"
        return self.success_message % dict(people=people)
