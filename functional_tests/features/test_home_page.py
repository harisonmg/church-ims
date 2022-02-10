from functional_tests import pages
from functional_tests.base import FunctionalTestCase


class HomePageTestCase(FunctionalTestCase):
    def test_anonymous_user_can_access_the_home_page(self):
        # A user visits the home page
        home_page = pages.HomePage(self)
        home_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title, header and heading
        self.assertEqual(home_page.title, self.SITE_NAME)
        self.assertEqual(home_page.header.title, self.header_title)
        self.assertEqual(home_page.heading, self.SITE_NAME)

        # He sees links for the sign up and login pages
        self.assertEqual(home_page.signup_link, {"Sign up": pages.SignupPage(self).url})
        self.assertEqual(home_page.login_link, {"Log in": pages.LoginPage(self).url})

        # There is also some site information in the footer
        self.assertEqual(home_page.footer.text, "Made with 💙 by contributors")
        contributors_link = (
            "https://github.com/harisonmg/church-ims/graphs/contributors"
        )
        self.assertEqual(home_page.footer.links, {"contributors": contributors_link})
