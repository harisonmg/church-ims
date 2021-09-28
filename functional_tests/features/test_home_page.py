from functional_tests.base import FunctionalTestCase
from functional_tests.utils import pages


class HomePageTestCase(FunctionalTestCase):
    def test_that_a_user_can_access_the_home_page(self):
        # A user visits the home page
        home_page = pages.HomePage(self)
        home_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the site title, heading and header
        site_name = self.get_site_name()
        self.assertEqual(home_page.title, site_name)
        self.assertEqual(home_page.header.title, site_name)
        self.assertEqual(home_page.heading, site_name)

        # He sees links for the sign up and login pages
        self.assertEqual(home_page.primary_cta_link, pages.SignupPage(self).url)
        self.assertEqual(home_page.sencondary_cta_link, pages.LoginPage(self).url)
