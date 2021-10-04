from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView

from .models import TemperatureRecord


class TemperatureRecordsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    context_object_name = "temperature_records"
    model = TemperatureRecord
    paginate_by = 10
    permission_required = "records.view_temperaturerecord"
    template_name = "records/temperature_records_list.html"
