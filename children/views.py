from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls.base import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

# from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory

from .models import Child, ParentChildRelationship


# class ParentChildRelationshipsInline(InlineFormSetFactory):
#     model = ParentChildRelationship
#     fields = ("parent", "child", "relationship_type")
#     extra = 1


# class ChildRelationshipCreateView(CreateWithInlinesView):
#     model = Child
#     inlines = [ParentChildRelationshipsInline,]
#     fields = ("slug", "full_name", "dob", "gender")
#     template_name = 'children_form.html'

#     def get_success_url(self):
#         return reverse("children:relationship_by_user_list")


# class ChildRelationshipUpdateView(UpdateWithInlinesView):
#     model = Child
#     inlines = [ParentChildRelationshipsInline,]
#     fields = ("slug", "full_name", "dob", "gender")
#     template_name = 'children_form.html'

#     def get_success_url(self):
#         return reverse("children:relationship_by_user_list")


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
        return reverse("children:by_user_list")


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
        return ParentChildRelationship.objects.filter(
            parent=self.request.user
        )


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
        context['form'].fields['child'].queryset = Child.objects.filter(
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
        return ParentChildRelationship.objects.filter(
            parent=self.request.user
        )

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
