from django.test import SimpleTestCase
from django.urls import resolve


class SignupURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/accounts/signup/")

    def test_view_func(self):
        self.assertEqual(self.match.func.__name__, "SignupView")

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "account_signup")


class LoginURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/accounts/login/")

    def test_view_func(self):
        self.assertEqual(self.match.func.__name__, "LoginView")

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "account_login")
