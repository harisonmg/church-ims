from django.test import RequestFactory, SimpleTestCase

from core import views


class IndexViewTestCase(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("dummy_path/")
        self.response = views.IndexView.as_view()(self.request)

    def test_response_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        with self.assertTemplateUsed("core/index.html"):
            self.response.render()
