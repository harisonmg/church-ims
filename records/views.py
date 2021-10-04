from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class TemperatureRecordsListView(LoginRequiredMixin, TemplateView):
    template_name = "records/temperature_records_list.html"
