from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from accounts import views


class AccountsBaseTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testing4321"
        )


class LoginViewTestCase(AccountsBaseTestCase):
    def test_login_view(self):
        """Test that the login view returns a 200 response and uses
        the correct template
        """
        request = self.factory.get("/accounts/login/")
        response = views.LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed("accounts/login.html"):
            response.render()


class LogoutViewTestCase(AccountsBaseTestCase):
    def test_redirect_if_not_logged_in(self):
        """
        Test that the logout view redirects to the home page
        when a user is not logged in
        """
        response = self.client.get("/accounts/logout/")
        self.assertRedirects(response, "/")

    def test_logout_redirect_url(self):
        """
        Test that the logout view redirects to the home page
        when a user is logged in
        """
        self.client.login(username="testuser", password="testing4321")
        response = self.client.get("/accounts/logout/")
        self.assertRedirects(response, "/")


class PasswordChangeViewTestCase(AccountsBaseTestCase):
    def test_password_change_view(self):
        """Test that the password change view returns a 200 response
        and uses the correct template
        """
        self.client.login(username="testuser", password="testing4321")
        response = self.client.get("/accounts/password_change/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/password_change.html")


class PasswordChangeDoneViewTestCase(AccountsBaseTestCase):
    def test_password_change_done_view(self):
        """Test that the password change done view returns
        a 200 response and uses the correct template
        """
        self.client.login(username="testuser", password="testing4321")
        response = self.client.get("/accounts/password_change/done/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/password_change_done.html")


class PasswordResetViewTestCase(AccountsBaseTestCase):
    def test_password_reset_view(self):
        """Test that the password reset view returns a 200 response
        and uses the correct template
        """
        request = self.factory.get("/accounts/password_reset/")
        response = views.PasswordResetView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed("accounts/password_reset.html"):
            response.render()


class PasswordResetDoneViewTestCase(AccountsBaseTestCase):
    def test_password_reset_done_view(self):
        """Test that the password reset done view returns
        a 200 response and uses the correct template
        """
        request = self.factory.get("/accounts/password_reset/done/")
        response = views.PasswordResetDoneView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed("accounts/password_reset_done.html"):
            response.render()


class PasswordResetCompleteViewTestCase(AccountsBaseTestCase):
    def test_password_reset_complete_view(self):
        """Test that the password reset complete view returns
        a 200 response and uses the correct template
        """
        request = self.factory.get("/accounts/reset/done/")
        response = views.PasswordResetCompleteView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed("accounts/password_reset_complete.html"):
            response.render()


class RegisterViewTestCase(AccountsBaseTestCase):
    def test_register_view(self):
        """Test that the register view returns a 200 response
        and uses the correct template
        """
        request = self.factory.get("/accounts/register/")
        response = views.RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed("accounts/register.html"):
            response.render()
