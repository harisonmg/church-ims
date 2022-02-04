from django.test import SimpleTestCase
from django.urls import resolve
from django.utils.module_loading import import_string


class SignupURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/accounts/signup/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class,
            import_string("allauth.account.views.SignupView"),
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "account_signup")


class LoginURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/accounts/login/")

    def test_view_func(self):
        self.assertEqual(
            self.match.func.view_class, import_string("allauth.account.views.LoginView")
        )

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "account_login")
