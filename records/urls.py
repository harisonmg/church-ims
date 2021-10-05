from django.urls import path

from . import views

app_name = "records"
urlpatterns = [
    path(
        "temperature/username/add/",
        views.TemperatureRecordCreateView.as_view(),
        name="temperature_record_create",
    ),
    path(
        "temperature/",
        views.TemperatureRecordsListView.as_view(),
        name="temperature_records_list",
    ),
]
