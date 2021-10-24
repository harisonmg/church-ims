from django.test import SimpleTestCase
from django.urls import resolve


class IndexURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/")

    def test_view_func(self):
        self.assertEqual(self.match.func.__name__, "IndexView")

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "core:index")


class LoginRedirectURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/login/redirect/")

    def test_view_func(self):
        self.assertEqual(self.match.func.__name__, "LoginRedirectView")

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "core:login_redirect")


class DashboardURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/dashboard/")

    def test_view_func(self):
        self.assertEqual(self.match.func.__name__, "DashboardView")

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "core:dashboard")
