from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse, reverse_lazy
from django.urls.base import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from extra_views import (CreateWithInlinesView, InlineFormSetFactory,
                         UpdateWithInlinesView)

from .models import Child, ParentChildRelationship


class ParentChildRelationshipInline(InlineFormSetFactory):
    model = ParentChildRelationship
    fields = ("child", "relationship_type")
    fk_name = "child"
    factory_kwargs = {"extra": 1}

    # def get_queryset(self):
    #     return ParentChildRelationship.objects.filter(parent=self.request.user)


class ChildRelationshipCreateView(CreateWithInlinesView):
    model = Child
    inlines = [
        ParentChildRelationshipInline,
    ]
    fields = ("slug", "full_name", "dob", "gender")
    template_name = "children/child_relationship_form.html"

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     form.instance.parent = self.request.user
    #     form.instance.updated_by = self.request.user
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse("children:relationship_by_user_list")


class ChildRelationshipUpdateView(UpdateWithInlinesView):
    model = Child
    inlines = [
        ParentChildRelationshipInline,
    ]
    fields = ("slug", "full_name", "dob", "gender")
    template_name = "children/child_relationship_form.html"

    def get_success_url(self):
        return reverse("children:relationship_by_user_list")


class ChildListView(LoginRequiredMixin, ListView):
    model = Child
    context_object_name = "children"


class ChildrenByUserListView(LoginRequiredMixin, ListView):
    model = Child
    context_object_name = "children"

    def get_queryset(self):
        return Child.objects.filter(created_by=self.request.user)


class ChildDetailView(LoginRequiredMixin, DetailView):
    model = Child


class ChildCreateView(LoginRequiredMixin, CreateView):
    model = Child
    fields = ("slug", "full_name", "dob", "gender")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("children:relationship_create")


class ChildUpdateView(LoginRequiredMixin, UpdateView):
    model = Child
    fields = ("slug", "full_name", "dob", "gender")

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class RelationshipListView(LoginRequiredMixin, ListView):
    model = ParentChildRelationship
    context_object_name = "relationships"
    template_name = "children/relationship_list.html"


class RelationshipByUserListView(LoginRequiredMixin, ListView):
    model = ParentChildRelationship
    context_object_name = "relationships"
    template_name = "children/relationship_list.html"

    def get_queryset(self):
        return ParentChildRelationship.objects.filter(parent=self.request.user)


class RelationshipDetailView(LoginRequiredMixin, DetailView):
    model = ParentChildRelationship
    context_object_name = "relationship"
    template_name = "children/relationship_detail.html"


class RelationshipCreateView(LoginRequiredMixin, CreateView):
    model = ParentChildRelationship
    fields = ("child", "relationship_type")
    template_name = "children/relationship_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"].fields["child"].queryset = Child.objects.filter(
            created_by=self.request.user
        )
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.parent = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("children:relationship_by_user_list")


class RelationshipUpdateView(LoginRequiredMixin, UpdateView):
    model = ParentChildRelationship
    fields = ("child", "relationship_type")
    context_object_name = "relationship"
    template_name = "children/relationship_form.html"

    def get_queryset(self):
        return ParentChildRelationship.objects.filter(parent=self.request.user)

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("children:relationship_by_user_list")


class RelationshipDeleteView(LoginRequiredMixin, DeleteView):
    model = ParentChildRelationship
    fields = ("child", "relationship_type")
    context_object_name = "relationship"
    template_name = "children/relationship_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("children:relationship_by_user_list")
