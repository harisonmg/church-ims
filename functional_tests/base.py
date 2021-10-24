import logging
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from django.test import tag

import decouple
from faker import Faker
from selenium import webdriver

from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.utils.search import find_url


@tag("functional")
class FunctionalTestCase(StaticLiveServerTestCase):
    """Sets up data to be shared across all functional tests

    Args:
        StaticLiveServerTestCase (object): A subclass of
        django.test.LiveServerTestCase
    """

    SCREENSHOT = decouple.config("SCREENSHOT", cast=bool, default=False)
    SCREENSHOTS_DIR = Path(__file__).resolve().parent / "screenshots"
    SITE_NAME = settings.SITE_NAME

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # set up a faker object
        cls.fake = Faker()

        # set browser options based on settings
        cls.browser_options = webdriver.firefox.options.Options()
        cls.browser_options.headless = decouple.config("CI", cast=bool, default=False)

        # logging
        logging.basicConfig(filename="functional_tests.log", level=logging.INFO)

    def setUp(self):
        self.browser = webdriver.Firefox(options=self.browser_options)

    def tearDown(self):
        self.take_screenshot()
        self.browser.quit()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    @property
    def mail(self):
        return mail

    @staticmethod
    def find_url(text):
        return find_url(text=text)

    @property
    def account_dropdown_links(self):
        links = {"Log out": pages.LogoutPage(self).url}
        return links

    @property
    def header_title(self):
        return {self.SITE_NAME: pages.HomePage(self).url}

    def create_pre_authenticated_session(self, user=None):
        # create a user
        if user is None:
            user = UserFactory()

        # create a session
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()

        # to set a cookie, we need to first visit the domain.
        # 404 pages load the quickest!
        pages.BasePage(self).visit()
        cookie_dict = dict(
            name=settings.SESSION_COOKIE_NAME, value=session.session_key, path="/"
        )
        self.browser.add_cookie(cookie_dict=cookie_dict)

    def take_screenshot(self):
        if self.SCREENSHOT:
            filename = self._get_screenshot_filename()
            logging.info(f"screenshotting to {filename}")
            self.browser.get_screenshot_as_file(filename)

    def _get_screenshot_filename(self):
        if not self.SCREENSHOTS_DIR.exists():
            self.SCREENSHOTS_DIR.mkdir(parents=True)

        classname = self.__class__.__name__
        method = self._testMethodName
        timestamp = datetime.now().isoformat().replace(":", ".")
        file_name = f"{self.SCREENSHOTS_DIR}/{classname}.{method}-{timestamp}.png"
        return file_name
