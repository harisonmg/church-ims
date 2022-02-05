from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from people.factories import AdultFactory


class AdultCreationTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        create_person = Permission.objects.filter(name="Can add person")
        view_person = Permission.objects.filter(name="Can view person")
        permissions = create_person | view_person
        self.user = UserFactory(user_permissions=tuple(permissions))

        # person
        self.person = AdultFactory.build()

        # auth
        self.create_pre_authenticated_session(self.user)

    def test_adult_creation(self):
        # An authorized user visits the adult creation page.
        adult_creation_page = pages.AdultCreationPage(self)
        adult_creation_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(adult_creation_page.title, self.SITE_NAME)
        self.assertEqual(adult_creation_page.header.title, self.header_title)
        self.assertEqual(adult_creation_page.heading, "Add an adult's information")

        # He can also see a sidebar navigation, with the current page link highlighted
        self.assertEqual(
            adult_creation_page.sidebar.active_links,
            {"Add an adult": self.browser.current_url},
        )

        # He sees the inputs of the adult form, including labels and placeholders.
        self.assertEqual(adult_creation_page.form.username_label, "Username*")
        self.assertEqual(adult_creation_page.form.full_name_label, "Full name*")
        self.assertEqual(adult_creation_page.form.gender_label, "Gender*")
        self.assertEqual(adult_creation_page.form.date_of_birth_label, "Date of birth*")
        self.assertEqual(adult_creation_page.form.phone_number_label, "Phone number*")
        self.assertEqual(adult_creation_page.form.submit_button_label, "Add")

        # He enters the person's details and submits the form
        adult_creation_page.form.enter_username(self.person.username)
        adult_creation_page.form.enter_full_name(self.person.full_name)
        adult_creation_page.form.select_gender(self.person.get_gender_display())
        adult_creation_page.form.enter_dob(str(self.person.dob))
        adult_creation_page.form.enter_phone_number(str(self.person.phone_number))
        adult_creation_page.form.submit()

        # The person's information was added successfully and he is redirected
        # to the person's detail page
        person_detail_page = pages.PersonDetailPage(self, self.person.username)
        self.assertEqual(self.browser.current_url, person_detail_page.url)
        self.assertEqual(
            person_detail_page.messages[0],
            f"{self.person.username}'s information has been added successfully.",
        )
