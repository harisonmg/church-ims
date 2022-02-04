from django.test import SimpleTestCase
from django.urls import resolve
from django.utils.module_loading import import_string


class IndexURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class, import_string("core.views.IndexView")
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "core:index")


class LoginRedirectURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/login/redirect/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class, import_string("core.views.LoginRedirectView")
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "core:login_redirect")


class DashboardURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/dashboard/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class, import_string("core.views.DashboardView")
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "core:dashboard")
