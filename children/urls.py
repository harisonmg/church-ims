from django.urls import path

from . import views

app_name = "children"
urlpatterns = [
    # path("child_relationship/<uuid:pk>/update/", views.ChildRelationshipUpdateView.as_view(), name="child_relationship_update"),
    path("child_relationship/add/", views.ChildRelationshipCreateView.as_view(), name="child_relationship_create"),
    path(
        "relationships/add/",
        views.RelationshipCreateView.as_view(),
        name="relationship_create",
    ),
    path(
        "relationships/all/",
        views.RelationshipListView.as_view(),
        name="relationship_list",
    ),
    path(
        "relationships/<uuid:pk>/delete/",
        views.RelationshipDeleteView.as_view(),
        name="relationship_delete",
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
        "relationships/",
        views.RelationshipByUserListView.as_view(),
        name="relationship_by_user_list",
    ),
    path("add/", views.ChildCreateView.as_view(), name="create"),
    path("all/", views.ChildListView.as_view(), name="list"),
    path(
        "<slug:slug>/children/",
        views.ChildrenByUserListView.as_view(),
        name="by_user_list",
    ),
    path("<slug:slug>/update/", views.ChildUpdateView.as_view(), name="update"),
    path("<slug:slug>/", views.ChildDetailView.as_view(), name="detail"),
    path("all/", views.ChildListView.as_view(), name="list"),
    path("", views.ChildrenByUserListView.as_view(), name="by_user_list"),
]
