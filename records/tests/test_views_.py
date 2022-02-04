from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser, Permission
from django.core.exceptions import ImproperlyConfigured
from django.http.response import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils.module_loading import import_string

from accounts.factories import UserFactory
from people.factories import PersonFactory
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
        self.assertEqual(context_object_name, "temperature_records")

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
        self.assertIn("records/temperature_records_list.html", template_names)

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
        self.assertEqual(permission_required, ("records.view_temperaturerecord",))

    # template logic
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


class TemperatureRecordCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.person = PersonFactory()
        cls.user = UserFactory()
        cls.temp_record = TemperatureRecordFactory.build(person=cls.person)
        cls.form_data = {
            "person": cls.person,
            "body_temperature": cls.temp_record.body_temperature,
        }

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.post("dummy_path", data=self.form_data)
        self.view_class = views.TemperatureRecordCreateView
        self.view_func = self.view_class.as_view()
        self.view = self.view_class()

    # FormMixin
    def test_initial(self):
        self.view.setup(self.request)
        initial = self.view.get_initial()
        self.assertEqual(initial, {})

    def test_prefix(self):
        self.view.setup(self.request)
        prefix = self.view.get_prefix()
        self.assertIsNone(prefix)

    def test_form_class(self):
        self.view.setup(self.request)
        form_class = self.view.get_form_class()
        self.assertEqual(
            form_class, import_string("records.forms.TemperatureRecordCreationForm")
        )

    def test_form_kwargs(self):
        self.view.setup(self.request)
        form_kwargs = {
            "initial": self.view.get_initial(),
            "prefix": self.view.get_prefix(),
            "data": self.request.POST,
            "files": self.request.FILES,
        }
        self.assertEqual(self.view.get_form_kwargs(), form_kwargs)

    def test_success_url(self):
        self.view.setup(self.request)
        self.view.object = self.temp_record
        success_url = self.view.get_success_url()
        self.assertEqual(success_url, reverse("people:people_list"))

    def test_form_invalid(self):
        self.request.user = self.user
        self.view.setup(self.request, username=self.person.username)
        self.view.object = None
        form = self.view.get_form()
        response = self.view.form_invalid(form)
        self.assertEqual(response.status_code, 200)

    # SuccessMessageMixin
    def test_success_message(self):
        self.request.user = self.user
        self.view.setup(self.request, username=self.person.username)
        self.view.object = self.temp_record
        success_message = self.view.get_success_message(self.form_data)
        self.assertEqual(
            success_message,
            f"A temperature record for {self.person} has been added successfully.",
        )

    @patch("django.contrib.messages.success")
    def test_form_valid_without_duplicate(self, mock_success):
        self.request.user = self.user
        self.view.setup(self.request, username=self.person.username)
        form = self.view.get_form()
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)
        self.assertTrue(mock_success.called)
        self.assertEqual(response.status_code, 302)
        temp_record = TemperatureRecord.objects.get(person=self.person)
        self.assertEqual(temp_record.created_by, self.user)

    # ModelFormMixin
    def test_form_valid_with_duplicate(self):
        TemperatureRecordFactory(**self.form_data)
        self.request.user = self.user
        self.view.setup(self.request, username=self.person.username)
        self.view.object = None
        form = self.view.get_form()
        response = self.view.form_valid(form)
        self.assertEqual(response.status_code, 200)
        response.render()
        error_message = f"{self.person}'s temperature record already exists"
        self.assertInHTML(error_message, str(response.content))

    # SingleObjectMixin
    def test_queryset(self):
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            queryset = self.view.get_queryset()
            self.assertEqual(list(queryset), [])

    def test_slug_field(self):
        self.view.setup(self.request)
        slug_field = self.view.get_slug_field()
        self.assertEqual(slug_field, "slug")

    def test_object(self):
        self.view.setup(self.request, username=self.person.username)
        with self.assertRaises(ImproperlyConfigured):
            obj = self.view.get_object()
            self.assertIsNone(obj)

    def test_person_with_existing_person(self):
        self.view.setup(self.request, username=self.person.username)
        obj = self.view.get_person()
        self.assertEqual(obj, self.person)

    def test_person_with_non_existent_person(self):
        self.view.setup(self.request, username="non-existent-person")
        with self.assertRaises(Http404):
            self.view.get_person()

    def test_context_object_name(self):
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            queryset = self.view.get_queryset()
            context_object_name = self.view.get_context_object_name(queryset)
            self.assertIsNone(context_object_name)

    def test_context_data(self):
        self.view.setup(self.request, username=self.person.username)
        self.view.object = None
        context_data = self.view.get_context_data()
        self.assertEqual(list(context_data.keys()), ["form", "view", "person"])

    # SingleObjectTemplateResponseMixin
    def test_template_name(self):
        self.view.setup(self.request)
        template_names = self.view.get_template_names()
        self.assertIn("records/temperature_record_form.html", template_names)

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
        self.assertEqual(permission_required, ("records.add_temperaturerecord",))
