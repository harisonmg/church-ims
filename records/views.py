from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView

from extra_views import SearchableListMixin

from .models import TemperatureRecord


class TemperatureRecordsListView(
    LoginRequiredMixin, PermissionRequiredMixin, SearchableListMixin, ListView
):
    context_object_name = "temperature_records"
    model = TemperatureRecord
    paginate_by = 10
    permission_required = "records.view_temperaturerecord"
    search_fields = ["person__username", "person__full_name"]
    template_name = "records/temperature_records_list.html"
