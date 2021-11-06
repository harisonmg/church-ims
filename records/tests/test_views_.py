from django.contrib.auth.models import AnonymousUser, Permission
from django.test import RequestFactory, TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from records import views
from records.factories import TemperatureRecordFactory
from records.models import TemperatureRecord

from .helpers import search_temperature_records


class TemperatureRecordsListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.authorized_user = cls.get_authorized_user()

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.build_get_request()
        self.view_class = views.TemperatureRecordsListView
        self.view_func = self.view_class.as_view()
        self.view = self.view_class()

    def build_get_request(self, data=None):
        return self.factory.get("dummy_path", data=data)

    @staticmethod
    def get_authorized_user():
        view_temp = Permission.objects.filter(name="Can view temperature record")
        return UserFactory(user_permissions=tuple(view_temp))

    @property
    def table_head(self):
        thead = """
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Username</th>
                <th scope="col">Temperature</th>
                <th scope="col">Time</th>
            </tr>
        </thead>
        """
        return thead

    def test_allow_empty(self):
        self.view.setup(self.request)
        allow_empty = self.view.get_allow_empty()
        self.assertTrue(allow_empty)

    def test_ordering(self):
        self.view.setup(self.request)
        ordering = self.view.get_ordering()
        self.assertIsNone(ordering)

    def test_search_fields(self):
        self.view.setup(self.request)
        search_fields = self.view.get_search_fields_with_filters()
        expected_search_fields = [
            ("person__username", "icontains"),
            ("person__full_name", "icontains"),
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
        self.assertQuerysetEqual(queryset, TemperatureRecord.objects.all())

    def test_queryset_with_search_query(self):
        temp_records = TemperatureRecordFactory.create_batch(10)
        search_term = temp_records[0].person.full_name.split()[0]
        self.request = self.build_get_request({"q": search_term})
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        self.assertQuerysetEqual(queryset, search_temperature_records(search_term))

    def test_paginate_by(self):
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        paginate_by = self.view.get_paginate_by(queryset)
        self.assertEqual(paginate_by, 10)

    def test_context_object_name(self):
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        context_object_name = self.view.get_context_object_name(queryset)
        self.assertEqual(context_object_name, "temperature_records")

    def test_template_name(self):
        self.view.setup(self.request)
        self.view.object_list = self.view.get_queryset()
        template_names = self.view.get_template_names()
        self.assertIn("records/temperature_records_list.html", template_names)

    def test_login_required(self):
        self.request.user = AnonymousUser()
        self.view.setup(self.request)
        response = self.view.dispatch(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account_login"), response.url)

    def test_permission_required(self):
        self.request.user = UserFactory()
        self.view.setup(self.request)
        permission_required = self.view.get_permission_required()
        self.assertEqual(permission_required, ("records.view_temperaturerecord",))

    def test_response_with_no_temperature_records(self):
        # setup
        self.request.user = self.authorized_user
        response = self.view_func(self.request)
        response.render()

        # test
        with self.assertRaises(AssertionError):
            self.assertInHTML(self.table_head, response.content.decode())
        self.assertInHTML(
            "There are no temperature records yet!", response.content.decode()
        )

    def test_response_with_temperature_records(self):
        # setup
        TemperatureRecordFactory()
        self.request.user = self.authorized_user
        response = self.view_func(self.request)
        response.render()

        # test
        with self.assertRaises(AssertionError):
            self.assertInHTML(
                "There are no temperature records yet!", response.content.decode()
            )
        self.assertInHTML(self.table_head, response.content.decode())

    def test_response_with_no_search_results(self):
        # setup
        TemperatureRecordFactory.create_batch(10)
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
