from django.urls import path

from . import views

app_name = "records"
urlpatterns = [
    path("temperature/children/add/", views.ChildTemperatureCreateView.as_view(), name="child_temperature_create"),
    path("temperature/children/all/", views.ChildTemperatureListView.as_view(), name="child_temperature_list"),
    path("temperature/children/<uuid:pk>/update/", views.ChildTemperatureUpdateView.as_view(), name="child_temperature_update"),
    path("temperature/children/<uuid:pk>/", views.ChildTemperatureDetailView.as_view(), name="child_temperature_detail"),
    path("temperature/children/", views.ChildTemperatureByUserListView.as_view(), name="child_temperature_by_user_list"),
]
