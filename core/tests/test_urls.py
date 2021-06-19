from django.test import SimpleTestCase
from django.urls import resolve


class CoreURLsTestCase(SimpleTestCase):
    """
    Test URL configuration of core
    """

    def test_root_url_uses_index_view(self):
        """
        Test that the root of the site resolves to the
        correct view function
        """
        root = resolve("/")
        self.assertEqual(root.func.__name__, "IndexView")
