from django.test import RequestFactory, SimpleTestCase

from core import views


class IndexViewTestCase(SimpleTestCase):
    """
    Tests for the index view
    """
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view_basic(self):
        """
        Test that index view returns a 200 response and uses
        the correct template
        """
        request = self.factory.get("/")
        response = views.IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        with self.assertTemplateUsed("index.html"):
            response.render()
