from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, SimpleTestCase, TestCase

from accounts.factories import UserFactory
from core import views


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


class DashboardViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/dashboard/"
        cls.view = views.DashboardView

    def test_template_used(self):
        factory = RequestFactory()
        request = factory.get("dummy_path/")
        request.user = AnonymousUser

        response = self.view.as_view()(request)
        with self.assertTemplateUsed("core/dashboard.html"):
            response.render()

    def test_view_requires_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_logged_in_response_status_code(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
