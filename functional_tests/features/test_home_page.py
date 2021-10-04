from functional_tests.base import FunctionalTestCase
from functional_tests.utils import pages


class HomePageTestCase(FunctionalTestCase):
    def test_anonymous_user_can_access_the_home_page(self):
        # A user visits the home page
        home_page = pages.HomePage(self)
        home_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title, header and heading
        site_name = self.get_site_name()
        self.assertEqual(home_page.title, site_name)
        self.assertEqual(home_page.header.title, self.header_title)
        self.assertEqual(home_page.heading, site_name)

        # He sees links for the sign up and login pages
        self.assertEqual(home_page.primary_cta_link, pages.SignupPage(self).url)
        self.assertEqual(home_page.secondary_cta_link, pages.LoginPage(self).url)

        # There is also some site information in the footer
        self.assertEqual(home_page.footer.text, "Made with 💙 by Harison Gachuru")
        self.assertEqual(
            home_page.footer.links,
            {"Harison Gachuru": "https://harisonmg.netlify.app/"},
        )
