from django.conf import settings
from django.test import RequestFactory, TestCase

from core import context_processors


class ContextProcessorTestCase(TestCase):
    """Sets up data to be shared across context processor tests"""

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("dummy_path/")


class GoogleAnalyticsTestCase(ContextProcessorTestCase):
    """Tests for the `google_analytics` context processor"""

    def test_returns_google_analytics_id(self):
        response = context_processors.google_analytics(self.request)
        expected_response = {"GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID}
        self.assertEqual(response.keys(), expected_response.keys())
        self.assertEqual(list(response.values()), list(expected_response.values()))


class SiteInfoTestCase(ContextProcessorTestCase):
    """Tests for the `site_info` context processor"""

    def test_returns_site_info(self):
        response = context_processors.site_info(self.request)
        expected_response = {
            "SITE_NAME": settings.SITE_NAME,
            "SITE_DESCRIPTION": settings.SITE_DESCRIPTION,
        }
        self.assertEqual(response.keys(), expected_response.keys())
        self.assertEqual(list(response.values()), list(expected_response.values()))
