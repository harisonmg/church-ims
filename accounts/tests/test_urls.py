from django.test import SimpleTestCase
from django.urls import resolve, reverse


class AccountsURLsTestCase(SimpleTestCase):
    def test_login_url(self):
        login = resolve(reverse("accounts:login"))
        self.assertEqual(login.func.__name__, "LoginView")

    def test_logout_url(self):
        login = resolve(reverse("accounts:logout"))
        self.assertEqual(login.func.__name__, "LogoutView")

    def test_password_change_url(self):
        password_reset = resolve(reverse("accounts:password_change"))
        self.assertEqual(password_reset.func.__name__, "PasswordChangeView")

    def test_password_change_done_url(self):
        password_reset_done = resolve(reverse("accounts:password_change_done"))
        self.assertEqual(password_reset_done.func.__name__, "PasswordChangeDoneView")

    def test_password_reset_url(self):
        password_reset = resolve(reverse("accounts:password_reset"))
        self.assertEqual(password_reset.func.__name__, "PasswordResetView")

    def test_password_reset_done_url(self):
        password_reset_done = resolve(reverse("accounts:password_reset_done"))
        self.assertEqual(password_reset_done.func.__name__, "PasswordResetDoneView")

    def test_password_reset_complete_url(self):
        password_reset_complete = resolve(reverse("accounts:password_reset_complete"))
        self.assertEqual(
            password_reset_complete.func.__name__, "PasswordResetCompleteView"
        )

    def test_register_url(self):
        register = resolve(reverse("accounts:register"))
        self.assertEqual(register.func.__name__, "RegisterView")
