from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from core import views
from people.factories import AdultFactory


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("dummy_path/")
        self.view_class = views.IndexView
        self.view_func = self.view_class.as_view()
        self.view = self.view_class()

    # TemplateResponseMixin
    def test_template_name(self):
        self.view.setup(self.request)
        template_names = self.view.get_template_names()
        self.assertIn("core/index.html", template_names)

    # View
    def test_response(self):
        response = self.view_func(self.request)
        self.assertEqual(response.status_code, 200)


class LoginRedirectViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("dummy_path/")
        self.view_class = views.LoginRedirectView
        self.view_func = self.view_class.as_view()
        self.view = self.view_class()

    # LoginRequiredMixin
    def test_login_required(self):
        self.request.user = AnonymousUser()
        response = self.view_func(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account_login"), response.url)

    # RedirectView
    def test_redirect_url_for_user_with_person(self):
        # setup
        user = UserFactory()
        AdultFactory(user=user)
        self.request.user = user
        self.view.setup(self.request)

        # test
        url = self.view.get_redirect_url()
        self.assertEqual(url, reverse("core:dashboard"))

    def test_redirect_url_for_user_without_person(self):
        self.request.user = UserFactory()
        self.view.setup(self.request)
        url = self.view.get_redirect_url()
        self.assertEqual(url, reverse("people:adult_self_register"))


class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("dummy_path/")
        self.view_class = views.DashboardView
        self.view_func = self.view_class.as_view()
        self.view = self.view_class()

    # TemplateResponseMixin
    def test_template_name(self):
        self.view.setup(self.request)
        template_names = self.view.get_template_names()
        self.assertIn("core/dashboard.html", template_names)

    # LoginRequiredMixin
    def test_login_required(self):
        self.request.user = AnonymousUser()
        response = self.view_func(self.request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account_login"), response.url)

    # View
    def test_response_for_user_with_person(self):
        # setup
        user = UserFactory()
        AdultFactory(user=user)
        self.request.user = user

        # test
        response = self.view_func(self.request)
        self.assertEqual(response.status_code, 200)

    def test_response_for_user_without_person(self):
        self.request.user = UserFactory()
        with self.assertRaises(PermissionDenied):
            self.view_func(self.request)
