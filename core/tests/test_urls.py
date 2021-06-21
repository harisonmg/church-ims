from django.test import SimpleTestCase
from django.urls import resolve


class CoreURLsTestCase(SimpleTestCase):

    def test_index_url(self):
        root = resolve("/")
        self.assertEqual(root.func.__name__, "IndexView")

    def test_dashboard_url(self):
        dashboard = resolve("/dashboard/")
        self.assertEqual(dashboard.func.__name__, "DashboardView")
