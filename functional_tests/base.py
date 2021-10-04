import re

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from django.test import tag

import decouple
from faker import Faker
from selenium import webdriver

from functional_tests.utils import pages


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

        # set up a faker object
        cls.fake = Faker()

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

    # TODO: make a property
    @staticmethod
    def get_site_name():
        return settings.SITE_NAME

    @property
    def mail(self):
        return mail

    def find_url(self, text):
        return re.search(r"(?P<url>https?://[^\s]+)", text).group("url")

    @property
    def account_dropdown_links(self):
        links = {"Log out": pages.LogoutPage(self).url}
        return links

    @property
    def header_title(self):
        return {self.get_site_name(): pages.HomePage(self).url}
