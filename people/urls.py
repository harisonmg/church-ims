from django.urls import path

from . import views

app_name = "people"
urlpatterns = [
    # relationships
    path(
        "relationships/<uuid:pk>/delete/",
        views.RelationshipDeleteView.as_view(),
        name="relationship_confirm_delete",
    ),
    path(
        "relationships/<uuid:pk>/update/",
        views.RelationshipUpdateView.as_view(),
        name="relationship_update",
    ),
    path(
        "relationships/<uuid:pk>/",
        views.RelationshipDetailView.as_view(),
        name="relationship_detail",
    ),
    path(
        "relationships/add/",
        views.RelationshipCreateView.as_view(),
        name="relationship_create",
    ),
    path(
        "relationships/", views.RelationshipListView.as_view(), name="relationship_list"
    ),
    # person
    path("add_child/", views.ChildCreateView.as_view(), name="child_create"),
    path(
        "<slug:username>/relatives/relationships/",
        views.RelationshipByUserListView.as_view(),
        name="relationship_by_user_list",
    ),
    path(
        "<slug:username>/relatives/",
        views.PersonByUserListView.as_view(),
        name="person_by_user_list",
    ),
    path(
        "<slug:username>/update/",
        views.ChildUpdateView.as_view(),
        name="child_update",
    ),
    path("<slug:username>/", views.PersonDetailView.as_view(), name="person_detail"),
    path("", views.PersonListView.as_view(), name="person_list"),
]
