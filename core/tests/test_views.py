from django.test import RequestFactory, SimpleTestCase

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
