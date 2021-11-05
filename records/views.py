from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from extra_views import SearchableListMixin

from people.models import Person

from .forms import TemperatureRecordCreationForm
from .models import TemperatureRecord
from .utils import is_duplicate_temp_record


class TemperatureRecordsListView(
    LoginRequiredMixin, PermissionRequiredMixin, SearchableListMixin, ListView
):
    context_object_name = "temperature_records"
    model = TemperatureRecord
    paginate_by = 10
    permission_required = "records.view_temperaturerecord"
    search_fields = ["person__username", "person__full_name"]
    template_name = "records/temperature_records_list.html"


class TemperatureRecordCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    form_class = TemperatureRecordCreationForm
    permission_required = "records.add_temperaturerecord"
    success_url = reverse_lazy("people:people_list")
    success_message = "A temperature record for %(person)s has been added successfully."
    template_name = "records/temperature_record_form.html"

    def get_person(self):
        return get_object_or_404(Person, username=self.kwargs["username"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["person"] = self.get_person()
        return context

    def form_valid(self, form):
        form.instance.person = self.get_person()
        form.instance.created_by = self.request.user
        if is_duplicate_temp_record(form.instance):
            error_message = "%(person)s's temperature record already exists"
            form.add_error(
                field=None, error=error_message % dict(person=form.instance.person)
            )
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(person=self.object.person)
