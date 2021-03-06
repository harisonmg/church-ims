from unittest.mock import call, patch

from django.contrib.auth.models import AnonymousUser, Permission
from django.core.exceptions import ImproperlyConfigured
from django.http.response import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils.module_loading import import_string

from accounts.factories import UserFactory
from people import views
from people.factories import (
    AdultFactory,
    ChildFactory,
    InterpersonalRelationshipFactory,
    PersonFactory,
)
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


class PersonCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = UserFactory()
        cls.person = PersonFactory.build()
        cls.form_data = {
            "username": cls.person.username,
            "full_name": cls.person.full_name,
            "gender": cls.person.gender,
            "dob": cls.person.dob,
        }

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.post("dummy_path", data=self.form_data)
        self.view_class = views.PersonCreateView
        self.view_func = self.view_class.as_view()
        self.view = self.view_class()

    def create_duplicate(self):
        data = self.form_data.copy()
        data["username"] = PersonFactory.build().username
        data["created_by"] = self.user
        PersonFactory(**data)

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
        self.assertEqual(form_class, import_string("people.forms.PersonCreationForm"))

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
        self.view.object = self.person
        success_url = self.view.get_success_url()
        self.assertEqual(
            success_url,
            reverse(
                "people:person_detail", kwargs={"username": self.form_data["username"]}
            ),
        )

    def test_form_invalid(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = None
        form = self.view.get_form()
        response = self.view.form_invalid(form)
        self.assertEqual(response.status_code, 200)

    # SuccessMessageMixin
    def test_success_message(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = self.person
        success_message = self.view.get_success_message(self.form_data)
        self.assertEqual(
            success_message, f"{self.person}'s information has been added successfully."
        )

    @patch("django.contrib.messages.success")
    def test_form_valid_without_duplicate(self, mock_success):
        self.request.user = self.user
        self.view.setup(self.request)
        form = self.view.get_form()
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)
        self.assertTrue(mock_success.called)
        self.assertEqual(response.status_code, 302)
        person = Person.objects.get(username=self.form_data["username"])
        self.assertEqual(person.created_by, self.user)

    # ModelFormMixin
    def test_form_valid_with_duplicate(self):
        # setup
        self.create_duplicate()
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = None
        form = self.view.get_form()
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)

        # test
        self.assertEqual(response.status_code, 200)
        response.render()
        error_message = "This person already exists"
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
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            obj = self.view.get_object()
            self.assertIsNone(obj)

    def test_context_object_name(self):
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            queryset = self.view.get_queryset()
            context_object_name = self.view.get_context_object_name(queryset)
            self.assertIsNone(context_object_name)

    def test_context_data(self):
        self.view.setup(self.request)
        self.view.object = None
        context_data = self.view.get_context_data()
        self.assertEqual(list(context_data.keys()), ["form", "view", "action"])
        self.assertEqual(context_data.get("action"), "add")

    # SingleObjectTemplateResponseMixin
    def test_template_name(self):
        self.view.setup(self.request)
        template_names = self.view.get_template_names()
        self.assertIn("people/person_form.html", template_names)

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
        self.assertEqual(permission_required, ("people.add_person",))


class AdultCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = UserFactory()
        cls.person = AdultFactory.build()
        cls.form_data = {
            "username": cls.person.username,
            "full_name": cls.person.full_name,
            "gender": cls.person.gender,
            "dob": cls.person.dob,
            "phone_number": cls.person.phone_number,
        }

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.post("dummy_path", data=self.form_data)
        self.view_class = views.AdultCreateView
        self.view_func = self.view_class.as_view()
        self.view = self.view_class()

    def create_duplicate(self):
        data = self.form_data.copy()
        data["username"] = AdultFactory.build().username
        data["created_by"] = self.user
        AdultFactory(**data)

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
        self.assertEqual(form_class, import_string("people.forms.AdultCreationForm"))

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
        self.view.object = self.person
        success_url = self.view.get_success_url()
        self.assertEqual(
            success_url,
            reverse(
                "people:person_detail", kwargs={"username": self.form_data["username"]}
            ),
        )

    def test_form_invalid(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = None
        form = self.view.get_form()
        response = self.view.form_invalid(form)
        self.assertEqual(response.status_code, 200)

    # SuccessMessageMixin
    def test_success_message(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = self.person
        success_message = self.view.get_success_message(self.form_data)
        self.assertEqual(
            success_message, f"{self.person}'s information has been added successfully."
        )

    @patch("django.contrib.messages.success")
    def test_form_valid_without_duplicate(self, mock_success):
        self.request.user = self.user
        self.view.setup(self.request)
        form = self.view.get_form()
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)
        self.assertTrue(mock_success.called)
        self.assertEqual(response.status_code, 302)
        person = Person.objects.get(username=self.form_data["username"])
        self.assertEqual(person.created_by, self.user)

    # ModelFormMixin
    def test_form_valid_with_duplicate(self):
        # setup
        self.create_duplicate()
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = None
        form = self.view.get_form()
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)

        # test
        self.assertEqual(response.status_code, 200)
        response.render()
        error_message = "This person already exists"
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
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            obj = self.view.get_object()
            self.assertIsNone(obj)

    def test_context_object_name(self):
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            queryset = self.view.get_queryset()
            context_object_name = self.view.get_context_object_name(queryset)
            self.assertIsNone(context_object_name)

    def test_context_data(self):
        self.view.setup(self.request)
        self.view.object = None
        context_data = self.view.get_context_data()
        self.assertEqual(
            list(context_data.keys()), ["form", "view", "action", "age_category"]
        )
        self.assertEqual(context_data.get("action"), "add")
        self.assertEqual(context_data.get("age_category"), "an adult")

    # SingleObjectTemplateResponseMixin
    def test_template_name(self):
        self.view.setup(self.request)
        template_names = self.view.get_template_names()
        self.assertIn("people/person_form.html", template_names)

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
        self.assertEqual(permission_required, ("people.add_person",))


class AdultSelfRegisterViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = UserFactory()
        cls.person = AdultFactory.build()
        cls.form_data = {
            "username": cls.person.username,
            "full_name": cls.person.full_name,
            "gender": cls.person.gender,
            "dob": cls.person.dob,
            "phone_number": cls.person.phone_number,
        }

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.post("dummy_path", data=self.form_data)
        self.view_class = views.AdultSelfRegisterView
        self.view_func = self.view_class.as_view()
        self.view = self.view_class()

    def create_duplicate(self):
        data = self.form_data.copy()
        data["username"] = AdultFactory.build().username
        data["created_by"] = self.user
        AdultFactory(**data)

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
        self.assertEqual(form_class, import_string("people.forms.AdultCreationForm"))

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
        self.view.object = self.person
        success_url = self.view.get_success_url()
        self.assertEqual(success_url, reverse("core:dashboard"))

    def test_form_invalid(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = None
        form = self.view.get_form()
        response = self.view.form_invalid(form)
        self.assertEqual(response.status_code, 200)

    # SuccessMessageMixin
    def test_success_message(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = self.person
        success_message = self.view.get_success_message(self.form_data)
        self.assertEqual(
            success_message, f"{self.person}'s information has been added successfully."
        )

    @patch("django.contrib.messages.success")
    def test_form_valid_without_duplicate(self, mock_success):
        self.request.user = self.user
        self.view.setup(self.request)
        form = self.view.get_form()
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)
        self.assertTrue(mock_success.called)
        self.assertEqual(response.status_code, 302)
        person = Person.objects.get(username=self.form_data["username"])
        self.assertEqual(person.created_by, self.user)
        self.assertEqual(person.user, self.user)

    # ModelFormMixin
    def test_form_valid_with_duplicate(self):
        # setup
        self.create_duplicate()
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = None
        form = self.view.get_form()
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)

        # test
        self.assertEqual(response.status_code, 200)
        response.render()
        error_message = "This person already exists"
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
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            obj = self.view.get_object()
            self.assertIsNone(obj)

    def test_context_object_name(self):
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            queryset = self.view.get_queryset()
            context_object_name = self.view.get_context_object_name(queryset)
            self.assertIsNone(context_object_name)

    def test_context_data(self):
        self.view.setup(self.request)
        self.view.object = None
        context_data = self.view.get_context_data()
        self.assertEqual(
            list(context_data.keys()), ["form", "view", "action", "age_category"]
        )
        self.assertEqual(context_data.get("action"), "add")
        self.assertEqual(context_data.get("age_category"), "an adult")

    # SingleObjectTemplateResponseMixin
    def test_template_name(self):
        self.view.setup(self.request)
        template_names = self.view.get_template_names()
        self.assertIn("people/self_register_form.html", template_names)

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
        self.assertEqual(permission_required, ())


class ChildCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = UserFactory()
        cls.parent = AdultFactory(user=cls.user)
        cls.person = ChildFactory.build()
        cls.form_data = {
            "username": cls.person.username,
            "full_name": cls.person.full_name,
            "gender": cls.person.gender,
            "dob": cls.person.dob,
        }

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.build_post_request(self.form_data)
        self.view_class = views.ChildCreateView
        self.view_func = self.view_class.as_view()
        self.view = self.view_class()

    def build_post_request(self, data=None):
        return self.factory.post("dummy_path", data=data)

    def create_duplicate(self):
        data = self.form_data.copy()
        data["username"] = ChildFactory.build().username
        data["created_by"] = self.user
        ChildFactory(**data)

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
        self.assertEqual(form_class, import_string("people.forms.ChildCreationForm"))

    def test_form_kwargs(self):
        self.view.setup(self.request)
        form_kwargs = {
            "initial": self.view.get_initial(),
            "prefix": self.view.get_prefix(),
            "data": self.request.POST,
            "files": self.request.FILES,
        }
        self.assertEqual(self.view.get_form_kwargs(), form_kwargs)

    def test_success_url_when_creator_is_the_parent(self):
        self.view.setup(self.request)
        self.view.object = self.person
        success_url = self.view.get_success_url(is_parent=True)
        self.assertEqual(success_url, reverse("core:dashboard"))

    def test_success_url_when_creator_is_not_the_parent(self):
        self.view.setup(self.request)
        self.view.object = self.person
        success_url = self.view.get_success_url()
        self.assertEqual(
            success_url,
            reverse(
                "people:parent_child_relationship_create",
                kwargs={"username": self.person.username},
            ),
        )

    def test_form_invalid(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = None
        form = self.view.get_form()
        response = self.view.form_invalid(form)
        self.assertEqual(response.status_code, 200)

    # SuccessMessageMixin
    def test_success_message(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = self.person
        success_message = self.view.get_success_message(self.form_data)
        self.assertEqual(
            success_message, f"{self.person}'s information has been added successfully."
        )

    @patch("django.contrib.messages.success")
    def test_form_valid_when_creator_is_not_the_parent(self, mock_success):
        self.request.user = self.user
        self.view.setup(self.request)
        form = self.view.get_form()
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)
        self.assertTrue(mock_success.called)
        self.assertEqual(response.status_code, 302)
        person = Person.objects.get(username=self.form_data["username"])
        self.assertEqual(person.created_by, self.user)
        self.assertEqual(person.user, None)

    @patch("django.contrib.messages.info")
    def test_create_relationship(self, mock_info):
        # setup
        child = ChildFactory(**self.form_data)
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = child
        self.view.create_relationship()

        # test
        relationship = InterpersonalRelationship.objects.get(relative=child)
        self.assertEqual(relationship.relation, "PC")
        self.assertEqual(relationship.person, self.parent)
        self.assertEqual(relationship.created_by, self.user)
        self.assertTrue(mock_info.called)
        message = f"A parent-child relationship between {self.parent} and {child}"
        message += " has been added."
        self.assertEqual(mock_info.call_args, call(self.request, message))

    @patch("django.contrib.messages.success")
    @patch("django.contrib.messages.info")
    def test_form_valid_when_creator_is_the_parent(self, mock_success, mock_info):
        # setup
        data = self.form_data.copy()
        data["is_parent"] = True
        self.request = self.build_post_request(data)
        self.request.user = self.user
        self.view.setup(self.request)
        form = self.view.get_form()

        # test
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)
        self.assertTrue(mock_success.called)
        self.assertEqual(response.status_code, 302)
        person = Person.objects.get(username=self.form_data["username"])
        self.assertEqual(person.created_by, self.user)
        self.assertEqual(person.user, None)
        self.assertTrue(mock_info.called)

    # ModelFormMixin
    def test_form_valid_with_duplicate(self):
        # setup
        self.create_duplicate()
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = None
        form = self.view.get_form()
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)

        # test
        self.assertEqual(response.status_code, 200)
        response.render()
        error_message = "This person already exists"
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
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            obj = self.view.get_object()
            self.assertIsNone(obj)

    def test_context_object_name(self):
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            queryset = self.view.get_queryset()
            context_object_name = self.view.get_context_object_name(queryset)
            self.assertIsNone(context_object_name)

    def test_context_data(self):
        self.view.setup(self.request)
        self.view.object = None
        context_data = self.view.get_context_data()
        self.assertEqual(
            list(context_data.keys()), ["form", "view", "action", "age_category"]
        )
        self.assertEqual(context_data.get("action"), "add")
        self.assertEqual(context_data.get("age_category"), "a child")

    # SingleObjectTemplateResponseMixin
    def test_template_name(self):
        self.view.setup(self.request)
        template_names = self.view.get_template_names()
        self.assertIn("people/person_form.html", template_names)

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
        self.assertEqual(permission_required, ())

    # UserPassesTestMixin
    def test_test_func_false(self):
        self.request.user = UserFactory()
        self.view.setup(self.request)
        self.assertFalse(self.view.test_func())

    def test_test_func_true(self):
        user = UserFactory()
        AdultFactory(user=user)
        self.request.user = user
        self.view.setup(self.request)
        self.assertTrue(self.view.test_func())


class PersonUpdateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = UserFactory()
        cls.person = PersonFactory()
        cls.form_data = {
            "username": cls.person.username,
            "full_name": cls.person.full_name,
            "gender": cls.person.gender,
            "dob": cls.person.dob,
        }

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.post("dummy_path", data=self.form_data)
        self.view_class = views.PersonUpdateView
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
        self.assertEqual(form_class, import_string("people.forms.PersonUpdateForm"))

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
        self.view.object = self.person
        success_url = self.view.get_success_url()
        self.assertEqual(
            success_url,
            reverse(
                "people:person_detail", kwargs={"username": self.form_data["username"]}
            ),
        )

    def test_form_invalid(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = None
        form = self.view.get_form()
        response = self.view.form_invalid(form)
        self.assertEqual(response.status_code, 200)

    # SuccessMessageMixin
    def test_success_message(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = self.person
        success_message = self.view.get_success_message(self.form_data)
        self.assertEqual(
            success_message,
            f"{self.person}'s information has been updated successfully.",
        )

    @patch("django.contrib.messages.success")
    def test_form_valid(self, mock_success):
        self.request.user = self.user
        self.view.setup(self.request, username=self.person.username)
        self.view.object = self.view.get_object()
        form = self.view.get_form()
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)
        self.assertTrue(mock_success.called)
        self.assertEqual(response.status_code, 302)

    # SingleObjectMixin
    def test_queryset(self):
        self.view.setup(self.request)
        queryset = self.view.get_queryset()
        self.assertEqual(list(queryset), [self.person])

    def test_slug_field(self):
        self.view.setup(self.request)
        slug_field = self.view.get_slug_field()
        self.assertEqual(slug_field, "username")

    def test_object(self):
        self.view.setup(self.request, username=self.person.username)
        obj = self.view.get_object()
        self.assertEqual(obj, self.person)

    def test_context_object_name(self):
        self.view.setup(self.request, username=self.person.username)
        obj = self.view.get_object()
        context_object_name = self.view.get_context_object_name(obj)
        self.assertEqual(context_object_name, "person")

    def test_context_data(self):
        self.view.setup(self.request)
        self.view.object = None
        context_data = self.view.get_context_data()
        self.assertEqual(list(context_data.keys()), ["form", "view", "action"])
        self.assertEqual(context_data.get("action"), "update")

    # SingleObjectTemplateResponseMixin
    def test_template_name(self):
        self.view.setup(self.request)
        template_names = self.view.get_template_names()
        self.assertIn("people/person_form.html", template_names)

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
        self.assertEqual(permission_required, ("people.change_person",))


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


class InterpersonalRelationshipCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = UserFactory()
        cls.person = PersonFactory()
        cls.relative = PersonFactory()
        cls.relationship = InterpersonalRelationshipFactory.build(
            person=cls.person, relative=cls.relative
        )
        cls.form_data = {
            "person": cls.person.username,
            "relative": cls.relative.username,
            "relation": cls.relationship.relation,
        }

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.post("dummy_path", data=self.form_data)
        self.view_class = views.RelationshipCreateView
        self.view_func = self.view_class.as_view()
        self.view = self.view_class()

    def get_data(self):
        data = self.form_data.copy()
        data["person"] = self.person
        data["relative"] = self.relative
        return data

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
            form_class,
            import_string("people.forms.InterpersonalRelationshipCreationForm"),
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
        self.view.object = self.relationship
        success_url = self.view.get_success_url()
        self.assertEqual(success_url, reverse("people:relationships_list"))

    def test_form_invalid(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = None
        form = self.view.get_form()
        response = self.view.form_invalid(form)
        self.assertEqual(response.status_code, 200)

    # SuccessMessageMixin
    def test_success_message(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = self.relationship
        data = self.get_data()
        success_message = self.view.get_success_message(data)
        people = f"{self.person} and {self.relative}"
        self.assertEqual(
            success_message,
            f"The relationship between {people} has been added successfully.",
        )

    @patch("django.contrib.messages.success")
    def test_form_valid_without_duplicate(self, mock_success):
        self.request.user = self.user
        self.view.setup(self.request)
        form = self.view.get_form()
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)
        self.assertTrue(mock_success.called)
        self.assertEqual(response.status_code, 302)
        relationship = InterpersonalRelationship.objects.get(person=self.person)
        self.assertEqual(relationship.created_by, self.user)

    # ModelFormMixin
    def test_form_valid_with_duplicate(self):
        data = self.get_data()
        InterpersonalRelationshipFactory(**data)
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = None
        form = self.view.get_form()
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors, {"__all__": ["This interpersonal relationship already exists"]}
        )

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
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            obj = self.view.get_object()
            self.assertIsNone(obj)

    def test_context_object_name(self):
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            queryset = self.view.get_queryset()
            context_object_name = self.view.get_context_object_name(queryset)
            self.assertIsNone(context_object_name)

    def test_context_data(self):
        self.view.setup(self.request)
        self.view.object = None
        context_data = self.view.get_context_data()
        self.assertEqual(list(context_data.keys()), ["form", "view"])

    # SingleObjectTemplateResponseMixin
    def test_template_name(self):
        self.view.setup(self.request)
        template_names = self.view.get_template_names()
        self.assertIn("people/relationship_form.html", template_names)

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
        self.assertEqual(permission_required, ("people.add_interpersonalrelationship",))


class ParentChildRelationshipCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = UserFactory()
        cls.person = AdultFactory(user=cls.user)
        cls.parent = AdultFactory()
        cls.child = ChildFactory()
        cls.form_data = {"person": cls.parent.username}
        cls.relationship_data = {
            "person": cls.parent,
            "relative": cls.child,
            "relation": "PC",
        }
        cls.relationship = InterpersonalRelationshipFactory.build(
            **cls.relationship_data
        )

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.post("dummy_path", data=self.form_data)
        self.view_class = views.ParentChildRelationshipCreateView
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
            form_class,
            import_string("people.forms.ParentChildRelationshipCreationForm"),
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
        self.view.object = self.relationship
        success_url = self.view.get_success_url()
        self.assertEqual(success_url, reverse("core:dashboard"))

    def test_form_invalid(self):
        self.request.user = self.user
        self.view.setup(self.request, username=self.child.username)
        self.view.object = None
        form = self.view.get_form()
        response = self.view.form_invalid(form)
        self.assertEqual(response.status_code, 200)

    # SuccessMessageMixin
    def test_success_message(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.view.object = self.relationship
        data = self.form_data.copy()
        success_message = self.view.get_success_message(data)
        people = f"{self.parent} and {self.child}"
        self.assertEqual(
            success_message,
            f"A parent-child relationship between {people} has been added.",
        )

    @patch("django.contrib.messages.success")
    def test_form_valid_without_duplicate(self, mock_success):
        self.request.user = self.user
        self.view.setup(self.request, username=self.child.username)
        form = self.view.get_form()
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)
        self.assertTrue(mock_success.called)
        self.assertEqual(response.status_code, 302)
        relationship = InterpersonalRelationship.objects.get(person=self.parent)
        self.assertEqual(relationship.created_by, self.user)
        self.assertEqual(relationship.relation, "PC")

    # ModelFormMixin
    def test_form_valid_with_duplicate(self):
        # setup
        InterpersonalRelationshipFactory(**self.relationship_data)
        self.request.user = self.user
        self.view.setup(self.request, username=self.child.username)
        self.view.object = None
        form = self.view.get_form()
        self.assertTrue(form.is_valid())
        response = self.view.form_valid(form)

        # test
        self.assertEqual(response.status_code, 200)
        response.render()
        error_message = "This interpersonal relationship already exists"
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
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            obj = self.view.get_object()
            self.assertIsNone(obj)

    def test_child_with_existing_person(self):
        self.view.setup(self.request, username=self.child.username)
        obj = self.view.get_child()
        self.assertEqual(obj, self.child)

    def test_child_with_non_existent_person(self):
        self.view.setup(self.request, username="non-existent-person")
        with self.assertRaises(Http404):
            self.view.get_child()

    def test_context_object_name(self):
        self.view.setup(self.request)
        with self.assertRaises(ImproperlyConfigured):
            queryset = self.view.get_queryset()
            context_object_name = self.view.get_context_object_name(queryset)
            self.assertIsNone(context_object_name)

    def test_context_data(self):
        self.view.setup(self.request, username=self.child.username)
        self.view.object = None
        context_data = self.view.get_context_data()
        self.assertEqual(list(context_data.keys()), ["form", "view", "child"])
        self.assertEqual(context_data.get("child"), self.child)

    # SingleObjectTemplateResponseMixin
    def test_template_name(self):
        self.view.setup(self.request)
        template_names = self.view.get_template_names()
        self.assertIn("people/relationship_form.html", template_names)

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
        self.assertEqual(permission_required, ())

    # UserPassesTestMixin
    def test_test_func_false(self):
        self.request.user = UserFactory()
        self.view.setup(self.request)
        self.assertFalse(self.view.test_func())

    def test_test_func_true(self):
        self.request.user = self.user
        self.view.setup(self.request)
        self.assertTrue(self.view.test_func())
