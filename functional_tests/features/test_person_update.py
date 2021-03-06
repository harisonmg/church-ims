from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from people.factories import PersonFactory


class PersonUpdateTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        update_person = Permission.objects.filter(name="Can change person")
        view_person = Permission.objects.filter(name="Can view person")
        permissions = update_person | view_person
        self.user = UserFactory(user_permissions=tuple(permissions))

        # person
        self.person = PersonFactory()
        self.username = PersonFactory.build().username

        # auth
        self.create_pre_authenticated_session(self.user)

    def test_person_update(self):
        # An authorized user visits a person's update page.
        person_update_page = pages.PersonUpdatePage(self, self.person.username)
        person_update_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(person_update_page.title, self.SITE_NAME)
        self.assertEqual(person_update_page.header.title, self.header_title)
        self.assertEqual(
            person_update_page.heading, f"Update {self.person.username}'s information"
        )

        # He sees the inputs and labels of the person update form
        self.assertEqual(person_update_page.form.username_label, "Username*")
        self.assertEqual(person_update_page.form.full_name_label, "Full name*")
        self.assertEqual(person_update_page.form.submit_button_label, "Update")

        # He updates the person's username and submits the form
        person_update_page.form.clear_username_input()
        person_update_page.form.enter_username(self.username)
        person_update_page.form.submit()

        # The person's information was added successfully and he is redirected
        # to the person's detail page
        person_detail_page = pages.PersonDetailPage(self, self.username)
        self.assertEqual(self.browser.current_url, person_detail_page.url)
        self.assertEqual(
            person_detail_page.messages[0],
            f"{self.username}'s information has been updated successfully.",
        )
