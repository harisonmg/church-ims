from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from core import views
from people.factories import AdultFactory


class IndexViewTestCase(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("dummy_path/")
        self.view = views.IndexView

    def test_response_status_code(self):
        response = self.view.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.view.as_view()(self.request)
        with self.assertTemplateUsed("core/index.html"):
            response.render()


class LoginRedirectViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/login/redirect/"
        cls.fully_registered_user = UserFactory()
        cls.partially_registered_user = UserFactory()

        # personal details
        AdultFactory(user=cls.fully_registered_user)

    def test_anonymous_user_response(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_fully_registered_user_response(self):
        self.client.force_login(self.fully_registered_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("core:dashboard"))

    def test_partially_registered_user_response(self):
        self.client.force_login(self.partially_registered_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("people:adult_self_register"))


class DashboardViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/dashboard/"
        cls.fully_registered_user = UserFactory()
        cls.partially_registered_user = UserFactory()

        # personal details
        AdultFactory(user=cls.fully_registered_user)

    def test_anonymous_user_response(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_fully_registered_user_response(self):
        self.client.force_login(self.fully_registered_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_partially_registered_user_response(self):
        self.client.force_login(self.partially_registered_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
