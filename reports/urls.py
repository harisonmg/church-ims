from django import urls
from django.urls import path

from . import views

app_name = "reports"
urlpatterns = [
    path(
        "temperature/<int:year>/<str:month>/<int:day>/",
        views.BodyTemperatureDayArchiveView.as_view(),
        name="body_temperature_day_archive",
    ),
    path(
        "temperature/today/",
        views.BodyTemperatureTodayArchiveView.as_view(),
        name="body_temperature_today",
    ),
]
