from accounts.factories import AdminUserFactory
from functional_tests.base import FunctionalTestCase


class AdminLoginTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        self.admin_password = self.fake.password()
        self.admin_user = AdminUserFactory(password=self.admin_password)

    def test_that_a_staff_can_log_in_to_the_admin_site(self):
        # An admin user visits the admin site
        self.browser.get(self.get_admin_url())

        # He can tell he's in the right place because of the title
        admin_site_title = f"Log in | {self.get_admin_site_title()}"
        self.assertEqual(self.browser.title, admin_site_title)

        # He enters his email and password and submits the form to
        # log in
        login_form = self.browser.find_element_by_id("login-form")
        login_form.find_element_by_name("username").send_keys(self.admin_user.username)
        login_form.find_element_by_name("password").send_keys(self.admin_password)
        login_form.find_element_by_css_selector(".submit-row input").click()

        # He sees the admin dashboard
        self.assertEqual(
            self.browser.find_element_by_link_text(
                "AUTHENTICATION AND AUTHORIZATION"
            ).get_attribute("href"),
            self.get_admin_url() + "auth/",
        )

        self.assertEqual(
            self.browser.find_element_by_link_text("Groups").get_attribute("href"),
            self.get_admin_url() + "auth/group/",
        )
