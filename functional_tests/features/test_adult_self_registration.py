from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from people.factories import AdultFactory


class AdultRegistrationTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        self.user = UserFactory()

        # person
        self.person = AdultFactory.build()

        # auth
        self.create_pre_authenticated_session(self.user)

    def test_adult_registration(self):
        # An user visits the adult self registration page.
        adult_registration_page = pages.AdultSelfRegistrationPage(self)
        adult_registration_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(adult_registration_page.title, self.SITE_NAME)
        self.assertEqual(adult_registration_page.header.title, self.header_title)
        self.assertEqual(
            adult_registration_page.heading, "Add your personal information"
        )

        # He sees the inputs of the adult form, including labels and placeholders.
        self.assertEqual(adult_registration_page.form.username_label, "Username*")
        self.assertEqual(adult_registration_page.form.full_name_label, "Full name*")
        self.assertEqual(adult_registration_page.form.gender_label, "Gender*")
        self.assertEqual(
            adult_registration_page.form.date_of_birth_label, "Date of birth*"
        )
        self.assertEqual(
            adult_registration_page.form.phone_number_label, "Phone number*"
        )
        self.assertEqual(adult_registration_page.form.submit_button_label, "Add")

        # He enters his details and submits the form
        adult_registration_page.form.enter_username(self.person.username)
        adult_registration_page.form.enter_full_name(self.person.full_name)
        adult_registration_page.form.select_gender(self.person.get_gender_display())
        adult_registration_page.form.enter_dob(str(self.person.dob))
        adult_registration_page.form.enter_phone_number(str(self.person.phone_number))
        adult_registration_page.form.submit()

        # His information was added successfully and is redirected
        # to his dashboard
        dashboard = pages.Dashboard(self)
        self.assertEqual(self.browser.current_url, dashboard.url)
        self.assertEqual(
            dashboard.messages[0],
            f"{self.person.username}'s information has been added successfully.",
        )
