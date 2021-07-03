from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from extra_views import SearchableListMixin

from .helpers import get_user_profile
from .models import FamilyRelationship, Person


class PersonListView(
    LoginRequiredMixin, UserPassesTestMixin, SearchableListMixin, ListView
):
    model = Person
    context_object_name = "people"
    paginate_by = 10
    search_fields = ("username", "full_name")

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def get_queryset(self):
        queryset = super().get_queryset()
        current_user = get_object_or_404(get_user_model(), pk=self.request.user.pk)
        return queryset.exclude(user=current_user)


class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Person
    fields = ("username", "full_name", "dob", "gender")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("people:relationship_create")


class PersonDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Person
    context_object_name = "person"
    slug_field = "username"

    def test_func(self):
        current_user = self.request.user
        person = self.get_object()
        if current_user.is_staff or (person.created_by == current_user):
            return True
        return False

    def get_object(self):
        return get_object_or_404(Person, username=self.kwargs.get("username"))


class PersonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Person
    context_object_name = "person"
    fields = ("username", "full_name", "dob", "gender")
    slug_field = "username"

    def test_func(self):
        current_user = self.request.user
        person = self.get_object()
        if current_user.is_staff or (person.created_by == current_user):
            return True
        return False

    def get_object(self):
        return get_object_or_404(Person, username=self.kwargs.get("username"))

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PersonByUserListView(
    LoginRequiredMixin, UserPassesTestMixin, SearchableListMixin, ListView
):
    model = Person
    context_object_name = "people"
    paginate_by = 10
    search_fields = ("username", "full_name")

    def test_func(self):
        current_user = self.request.user
        person = get_object_or_404(Person, username=self.kwargs.get("username"))
        if current_user.is_staff or (current_user == person.user):
            return True
        return False

    def get_queryset(self):
        queryset = super().get_queryset()
        person = get_object_or_404(Person, username=self.kwargs.get("username"))
        user = get_object_or_404(get_user_model(), person=person)
        return queryset.filter(created_by=user)


class RelationshipByUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = FamilyRelationship
    context_object_name = "relationships"
    template_name = "people/relationship_list.html"

    def test_func(self):
        current_user = get_object_or_404(get_user_model(), pk=self.request.user.pk)
        person = get_object_or_404(Person, username=self.kwargs.get("username"))
        if current_user.is_staff or (current_user == person.created_by):
            return True
        return False

    def get_queryset(self):
        queryset = super().get_queryset()
        person = get_object_or_404(Person, username=self.kwargs.get("username"))
        return queryset.filter(person=person)


class RelationshipListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = FamilyRelationship
    context_object_name = "relationships"
    template_name = "people/relationship_list.html"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class RelationshipCreateView(LoginRequiredMixin, CreateView):
    model = FamilyRelationship
    fields = ("relative", "relationship_type")
    template_name = "people/relationship_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        people = Person.objects.filter(created_by=current_user)
        context["form"].fields["relative"].queryset = people.exclude(
            pk=current_user.person.pk
        )
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.person = get_object_or_404(
            Person, pk=get_user_profile(self.request).pk
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "people:relationship_by_user_list",
            kwargs={"username": get_user_profile(self.request).username},
        )


class RelationshipDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = FamilyRelationship
    context_object_name = "relationship"
    template_name = "people/relationship_detail.html"

    def test_func(self):
        current_user = self.request.user
        relationship = self.get_object()
        if current_user.is_staff or (current_user.pk == relationship.person.pk):
            return True
        return False

    def get_object(self):
        return get_object_or_404(FamilyRelationship, pk=self.kwargs.get("pk"))


class RelationshipUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FamilyRelationship
    context_object_name = "relationship"
    fields = ("relative", "relationship_type")
    template_name = "people/relationship_form.html"

    def test_func(self):
        current_user = self.request.user
        relationship = self.get_object()
        if current_user.is_staff or (current_user.pk == relationship.person.pk):
            return True
        return False

    def get_object(self):
        return get_object_or_404(FamilyRelationship, pk=self.kwargs.get("pk"))

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "people:relationship_by_user_list",
            kwargs={"username": get_user_profile(self.request).username},
        )


class RelationshipDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FamilyRelationship
    context_object_name = "relationship"
    fields = ("relative", "relationship_type")
    template_name = "people/relationship_confirm_delete.html"

    def test_func(self):
        current_user = self.request.user
        relationship = self.get_object()
        if current_user.is_staff or (current_user.pk == relationship.person.pk):
            return True
        return False

    def get_object(self):
        return get_object_or_404(FamilyRelationship, pk=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse_lazy("people:relationship_by_user_list")
