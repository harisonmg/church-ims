import datetime

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        UserPassesTestMixin)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from children.models import Child

from .models import ChildTemperature


class ChildTemperatureListView(LoginRequiredMixin, ListView):
    model = ChildTemperature
    context_object_name = "children_temperature"
    template_name = "records/child_temperature_list.html"
    paginate_by = 10


class ChildTemperatureByUserListView(LoginRequiredMixin, ListView):
    model = ChildTemperature
    context_object_name = "children_temperature"
    template_name = "records/child_temperature_list.html"
    paginate_by = 10

    def get_queryset(self):
        return ChildTemperature.objects.filter(created_by=self.request.user)


class ChildTemperatureDetailView(LoginRequiredMixin, DetailView):
    model = ChildTemperature
    context_object_name = "child_temperature"
    template_name = "records/child_temperature_detail.html"


class ChildTemperatureCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ChildTemperature
    fields = ("temp",)
    template_name = "records/child_temperature_form.html"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['child'] = get_object_or_404(Child, slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        form.instance.child = get_object_or_404(Child, slug=self.kwargs['slug'])
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("records:child_temperature_list")


class ChildTemperatureUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ChildTemperature
    fields = (
        "child",
        "temp",
    )
    template_name = "records/child_temperature_form.html"
    context_object_name = "child_temperature"

    def test_func(self):
        temp_record = self.get_object()
        if self.request.user == temp_record.created_by:
            return True
        return False

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("records:child_temperature_list")
