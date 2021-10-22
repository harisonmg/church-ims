from django.urls import path

from . import views

app_name = "people"
urlpatterns = [
    path(
        "relationships/parent-child/add/",
        views.ParentChildRelationshipCreateView.as_view(),
        name="parent_child_relationship_create",
    ),
    path(
        "relationships/add/",
        views.RelationshipCreateView.as_view(),
        name="relationship_create",
    ),
    path(
        "relationships/",
        views.RelationshipsListView.as_view(),
        name="relationships_list",
    ),
    path(
        "register/self/",
        views.AdultSelfRegisterView.as_view(),
        name="adult_self_register",
    ),
    path("add/adult/", views.AdultCreateView.as_view(), name="adult_create"),
    path("add/child/", views.ChildCreateView.as_view(), name="child_create"),
    path("add/", views.PersonCreateView.as_view(), name="person_create"),
    path(
        "<str:username>/update/", views.PersonUpdateView.as_view(), name="person_update"
    ),
    path("<str:username>/", views.PersonDetailView.as_view(), name="person_detail"),
    path("", views.PeopleListView.as_view(), name="people_list"),
]
