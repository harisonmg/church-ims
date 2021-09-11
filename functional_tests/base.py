from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag

import decouple
from selenium import webdriver


@tag("functional")
class FunctionalTestCase(StaticLiveServerTestCase):
    """Sets up data to be shared across all functional tests

    Args:
        StaticLiveServerTestCase (object): A subclass of
        django.test.LiveServerTestCase
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # set browser options based on settings
        cls.browser_options = webdriver.firefox.options.Options()
        cls.browser_options.headless = decouple.config("CI", cast=bool, default=False)

    def setUp(self):
        self.browser = webdriver.Firefox(options=self.browser_options)

    def tearDown(self):
        self.browser.quit()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def get_admin_url(self):
        """Returns the admin URL from the `ADMIN_URL` setting

        Returns:
            string: The link to the homepage of the admin site
        """
        return f"{self.live_server_url}/{settings.ADMIN_URL}/"
