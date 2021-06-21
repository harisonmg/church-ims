from django.contrib.auth import get_user_model
from django.test import RequestFactory, SimpleTestCase, TestCase

from core import views


class IndexViewTestCase(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view(self):
        """
        Test that index view returns a 200 response and uses
        the correct template
        """
        request = self.factory.get("/")
        response = views.IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        with self.assertTemplateUsed("core/index.html"):
            response.render()


class DashboardViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.User = get_user_model()

        self.test_user = self.User.objects.create_user(
            username = 'testuser',
            password='testing4321'
        )

    def test_redirect_if_not_logged_in(self):
        """
        Test that the dashboard view redirects to the login page
        first when a user is not logged in
        """
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
            '/accounts/login/?next=/dashboard/')

    def test_dashboard_view_if_logged_in(self):
        """
        Test that the dashboard view returns a 200 response
        and uses the correct template when a user is logged in
        """
        self.client.login(
            username = 'testuser',
            password = 'testing4321'
        )
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('core/dashboard.html')
