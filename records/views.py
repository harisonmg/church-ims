from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import ChildTemperature

class ChildTemperatureListView(LoginRequiredMixin, ListView):
    model = ChildTemperature
    context_object_name = "children_temperature"
    template_name = "records/child_temperature_list.html"


class ChildTemperatureByUserListView(LoginRequiredMixin, ListView):
    model = ChildTemperature
    context_object_name = "children_temperature"    
    template_name = "records/child_temperature_list.html"

    def get_queryset(self):
        return ChildTemperature.objects.filter(created_by=self.request.user)


class ChildTemperatureDetailView(LoginRequiredMixin, DetailView):
    model = ChildTemperature
    context_object_name = "child_temperature"
    template_name = "records/child_temperature_detail.html"


class ChildTemperatureCreateView(LoginRequiredMixin, CreateView):
    model = ChildTemperature
    fields = ('child', 'temp',)    
    template_name = "records/child_temperature_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("records:child_temperature_list")


class ChildTemperatureUpdateView(LoginRequiredMixin, UpdateView):
    model = ChildTemperature
    fields = ('child', 'temp',)    
    template_name = "records/child_temperature_form.html"
    context_object_name = "child_temperature"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy("records:child_temperature_list")
