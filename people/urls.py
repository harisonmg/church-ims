from django.urls import path

from . import views

app_name = "people"
urlpatterns = [
    path("", views.PeopleListView.as_view(), name="people_list"),
]
