from django.contrib.auth.models import AnonymousUser, Permission
from django.http.response import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from people import views
from people.factories import InterpersonalRelationshipFactory, PersonFactory
from people.models import InterpersonalRelationship, Person

from .helpers import search_interpersonal_relationships, search_people


class PeopleListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.authorized_user = cls.get_authorized_user()

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.build_get_request()
        self.view_class = views.PeopleListView
        self.view_func = self.view_class.as_view()
        self.view = self.view_class()

    def build_get_request(self, data=None):
        return self.factory.get("dummy_path", data=data)

    @staticmethod
    def get_authorized_user():
        view_person = Permission.objects.filter(name="Can view person")
        return UserFactory(user_permissions=tuple(view_person))

    @property
    def table_head(self):
        thead = """
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Username</th>
                <th scope="col">Full name</th>
                <th scope="col">Age category</th>
                <th scope="col">Actions</th>
            </tr>
        </thead>
        """
        return thead

    # MultipleObjectMixin
    def test_allow_empty(self):
        self.view.setup(self.request)
        allow_empty = self.view.get_allow_empty()
        self.assertTrue(allow_empty)

    def test_ordering(self):
        self.view.setup(self.request)
        ordering = self.view.get_ordering()
        self.assertIsNone(ordering)

    # SearchableListMixin
    def test_search_fields(self):
        self.view.setup(self.request)
        search_fields = self.view.get_search_fields_with_filters()
        expected_search_fields = [("username", "icontains"), ("full_name", "icontains")]
        self.assertEqual(search_fields, expected_search_fields)

    def test_search_query(self):
        search_term = "search query"
        self.request = self.build_get_request({"q": search_term})
        self.view.setup(self.request)
        search_query = self.view.get_search_query()
        self.assertEqual(search_query, search_term)

    def test_queryset_without_search_query(self):
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        self.assertQuerysetEqual(queryset, Person.objects.all())

    def test_queryset_with_search_query(self):
        people = PersonFactory.create_batch(10)
        search_term = people[0].full_name.split()[0]
        self.request = self.build_get_request({"q": search_term})
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        self.assertQuerysetEqual(queryset, search_people(search_term))

    # MultipleObjectMixin
    def test_paginate_by(self):
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        paginate_by = self.view.get_paginate_by(queryset)
        self.assertEqual(paginate_by, 10)

    def test_context_object_name(self):
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        context_object_name = self.view.get_context_object_name(queryset)
        self.assertEqual(context_object_name, "people")

    def test_context_data(self):
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        self.view.object_list = queryset
        context_object_name = self.view.get_context_object_name(queryset)
        context_data = self.view.get_context_data()
        expected_context_data_keys = [
            "paginator",
            "page_obj",
            "is_paginated",
            "object_list",
            context_object_name,
            "view",
        ]
        self.assertEqual(list(context_data.keys()), expected_context_data_keys)

    # MultipleObjectTemplateResponseMixin
    def test_template_name(self):
        self.view.setup(self.request)
        self.view.object_list = self.view.get_queryset()
        template_names = self.view.get_template_names()
        self.assertIn("people/people_list.html", template_names)

    # LoginRequiredMixin
    def test_login_required(self):
        self.request.user = AnonymousUser()
        self.view.setup(self.request)
        response = self.view.dispatch(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account_login"), response.url)

    # PermissionRequiredMixin
    def test_permission_required(self):
        self.request.user = UserFactory()
        self.view.setup(self.request)
        permission_required = self.view.get_permission_required()
        self.assertEqual(permission_required, ("people.view_person",))

    # template logic
    def test_response_with_no_people(self):
        # setup
        self.request.user = self.authorized_user
        response = self.view_func(self.request)
        response.render()

        # test
        with self.assertRaises(AssertionError):
            self.assertInHTML(self.table_head, response.content.decode())
        self.assertInHTML("There are no people yet!", response.content.decode())

    def test_response_with_people(self):
        # setup
        PersonFactory()
        self.request.user = self.authorized_user
        response = self.view_func(self.request)
        response.render()

        # test
        with self.assertRaises(AssertionError):
            self.assertInHTML("There are no people yet!", response.content.decode())
        self.assertInHTML(self.table_head, response.content.decode())

    def test_response_with_no_search_results(self):
        # setup
        PersonFactory.create_batch(10)
        search_term = "does not exist"
        self.request = self.build_get_request({"q": search_term})
        self.request.user = self.authorized_user
        response = self.view_func(self.request)
        response.render()

        # test
        with self.assertRaises(AssertionError):
            self.assertInHTML(self.table_head, response.content.decode())
        self.assertInHTML(
            "Your search didn't yield any results", response.content.decode()
        )


class PersonDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.person = PersonFactory()

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("dummy_path")
        self.view_class = views.PersonDetailView
        self.view_func = self.view_class.as_view()
        self.view = self.view_class()

    # SingleObjectMixin
    def test_queryset(self):
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        self.assertEqual(list(queryset), [self.person])

    def test_slug_field(self):
        self.view.setup(self.request)
        slug_field = self.view.get_slug_field()
        self.assertEqual(slug_field, "username")

    def test_object_with_existing_person(self):
        self.view.setup(self.request, username=self.person.username)
        obj = self.view.get_object()
        self.assertEqual(obj, self.person)

    def test_object_with_non_existent_person(self):
        self.view.setup(self.request, username="non-existent-person")
        with self.assertRaises(Http404):
            self.view.get_object()

    def test_context_object_name(self):
        self.view.setup(self.request, username=self.person.username)
        obj = self.view.get_object()
        context_object_name = self.view.get_context_object_name(obj)
        self.assertEqual(context_object_name, "person")

    def test_context_data(self):
        self.view.setup(self.request, username=self.person.username)
        obj = self.view.get_object()
        self.view.object = obj
        context_object_name = self.view.get_context_object_name(obj)
        context_data = self.view.get_context_data()
        expected_context_data_keys = ["object", context_object_name, "view"]
        self.assertEqual(list(context_data.keys()), expected_context_data_keys)

    # SingleObjectTemplateResponseMixin
    def test_template_name(self):
        self.view.setup(self.request)
        template_names = self.view.get_template_names()
        self.assertIn("people/person_detail.html", template_names)

    # LoginRequiredMixin
    def test_login_required(self):
        self.request.user = AnonymousUser()
        self.view.setup(self.request)
        response = self.view.dispatch(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account_login"), response.url)

    # PermissionRequiredMixin
    def test_permission_required(self):
        self.request.user = UserFactory()
        self.view.setup(self.request)
        permission_required = self.view.get_permission_required()
        self.assertEqual(permission_required, ("people.view_person",))


class InterpersonalRelationshipsListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.authorized_user = cls.get_authorized_user()

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.build_get_request()
        self.view_class = views.RelationshipsListView
        self.view_func = self.view_class.as_view()
        self.view = self.view_class()

    def build_get_request(self, data=None):
        return self.factory.get("dummy_path", data=data)

    @staticmethod
    def get_authorized_user():
        view_relationship = Permission.objects.filter(
            name="Can view interpersonal relationship"
        )
        return UserFactory(user_permissions=tuple(view_relationship))

    @property
    def table_head(self):
        thead = """
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Person</th>
                <th scope="col">Relative</th>
                <th scope="col">Relationship type</th>
            </tr>
        </thead>
        """
        return thead

    # MultipleObjectMixin
    def test_allow_empty(self):
        self.view.setup(self.request)
        allow_empty = self.view.get_allow_empty()
        self.assertTrue(allow_empty)

    def test_ordering(self):
        self.view.setup(self.request)
        ordering = self.view.get_ordering()
        self.assertIsNone(ordering)

    # SearchableListMixin
    def test_search_fields(self):
        self.view.setup(self.request)
        search_fields = self.view.get_search_fields_with_filters()
        expected_search_fields = [
            ("person__username", "icontains"),
            ("relative__username", "icontains"),
        ]
        self.assertEqual(search_fields, expected_search_fields)

    def test_search_query(self):
        search_term = "search query"
        self.request = self.build_get_request({"q": search_term})
        self.view.setup(self.request)
        search_query = self.view.get_search_query()
        self.assertEqual(search_query, search_term)

    def test_queryset_without_search_query(self):
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        self.assertQuerysetEqual(queryset, InterpersonalRelationship.objects.all())

    def test_queryset_with_search_query(self):
        relationships = InterpersonalRelationshipFactory.create_batch(10)
        search_term = relationships[0].person.full_name.split()[0]
        self.request = self.build_get_request({"q": search_term})
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        self.assertQuerysetEqual(
            queryset, search_interpersonal_relationships(search_term)
        )

    # MultipleObjectMixin
    def test_paginate_by(self):
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        paginate_by = self.view.get_paginate_by(queryset)
        self.assertEqual(paginate_by, 10)

    def test_context_object_name(self):
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        context_object_name = self.view.get_context_object_name(queryset)
        self.assertEqual(context_object_name, "relationships")

    def test_context_data(self):
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        self.view.object_list = queryset
        context_object_name = self.view.get_context_object_name(queryset)
        context_data = self.view.get_context_data()
        expected_context_data_keys = [
            "paginator",
            "page_obj",
            "is_paginated",
            "object_list",
            context_object_name,
            "view",
        ]
        self.assertEqual(list(context_data.keys()), expected_context_data_keys)

    # MultipleObjectTemplateResponseMixin
    def test_template_name(self):
        self.view.setup(self.request)
        self.view.object_list = self.view.get_queryset()
        template_names = self.view.get_template_names()
        self.assertIn("people/relationships_list.html", template_names)

    # LoginRequiredMixin
    def test_login_required(self):
        self.request.user = AnonymousUser()
        self.view.setup(self.request)
        response = self.view.dispatch(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account_login"), response.url)

    # PermissionRequiredMixin
    def test_permission_required(self):
        self.request.user = UserFactory()
        self.view.setup(self.request)
        permission_required = self.view.get_permission_required()
        self.assertEqual(
            permission_required, ("people.view_interpersonalrelationship",)
        )

    # template logic
    def test_response_with_no_relationships(self):
        # setup
        self.request.user = self.authorized_user
        response = self.view_func(self.request)
        response.render()

        # test
        with self.assertRaises(AssertionError):
            self.assertInHTML(self.table_head, response.content.decode())
        self.assertInHTML(
            "There are no interpersonal relationships yet!", response.content.decode()
        )

    def test_response_with_relationships(self):
        # setup
        InterpersonalRelationshipFactory()
        self.request.user = self.authorized_user
        response = self.view_func(self.request)
        response.render()

        # test
        with self.assertRaises(AssertionError):
            self.assertInHTML(
                "There are no interpersonal relationships yet!",
                response.content.decode(),
            )
        self.assertInHTML(self.table_head, response.content.decode())

    def test_response_with_no_search_results(self):
        # setup
        InterpersonalRelationshipFactory.create_batch(10)
        search_term = "does not exist"
        self.request = self.build_get_request({"q": search_term})
        self.request.user = self.authorized_user
        response = self.view_func(self.request)
        response.render()

        # test
        with self.assertRaises(AssertionError):
            self.assertInHTML(self.table_head, response.content.decode())
        self.assertInHTML(
            "Your search didn't yield any results", response.content.decode()
        )
