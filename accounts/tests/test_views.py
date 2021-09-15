from django.test import RequestFactory, SimpleTestCase

from accounts import views


class SignupViewTestCase(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("dummy_path/")
        self.view = views.SignupView

    def test_response_status_code(self):
        response = self.view.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.view.as_view()(self.request)
        with self.assertTemplateUsed("accounts/signup.html"):
            response.render()


class LoginViewTestCase(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("dummy_path/")
        self.view = views.LoginView

    def test_response_status_code(self):
        response = self.view.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.view.as_view()(self.request)
        with self.assertTemplateUsed("accounts/login.html"):
            response.render()
