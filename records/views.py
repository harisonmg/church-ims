from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from people.models import Person

from .models import BodyTemperature


class BodyTemperatureCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = BodyTemperature
    fields = ("temp",)
    template_name = "records/body_temperature_form.html"

    def test_func(self):
        current_user = self.request.user
        person = get_object_or_404(Person, username=self.kwargs.get("username"))
        if current_user.is_staff and (current_user.pk != person.pk):
            return True
        return False

    def get_object(self):
        person = get_object_or_404(Person, username=self.kwargs.get("username"))
        return person

    def form_valid(self, form):
        form.instance.person = self.get_object()
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("people:person_list")


class BodyTemperatureByPersonListView(
    LoginRequiredMixin, UserPassesTestMixin, ListView
):
    model = BodyTemperature
    context_object_name = "body_temperature"
    template_name = "records/body_temperature_list.html"
    paginate_by = 10

    def test_func(self):
        current_user = get_object_or_404(get_user_model(), pk=self.request.user.pk)
        person = get_object_or_404(Person, username=self.kwargs.get("username"))
        if current_user.is_staff or (current_user.person == person):
            return True
        return False

    def get_queryset(self):
        queryset = super().get_queryset()
        person = get_object_or_404(Person, username=self.kwargs.get("username"))
        return queryset.filter(person=person)
