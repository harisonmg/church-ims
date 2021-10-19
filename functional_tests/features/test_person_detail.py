from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests import pages
from functional_tests.base import FunctionalTestCase
from people.factories import AdultFactory, ChildFactory


class PersonDetailTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        change_person = Permission.objects.filter(name="Can change person")
        view_person = Permission.objects.filter(name="Can view person")
        permissions = change_person | view_person
        self.user = UserFactory(user_permissions=tuple(permissions))

        # people
        self.adult = AdultFactory()
        self.child = ChildFactory()

        # auth
        self.create_pre_authenticated_session(self.user)

    def test_adult_detail(self):
        # An authorized user visits an adult's detail page.
        person_detail_page = pages.PersonDetailPage(self, self.adult.username)
        person_detail_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(person_detail_page.title, self.SITE_NAME)
        self.assertEqual(person_detail_page.header.title, self.header_title)
        self.assertEqual(person_detail_page.heading, f"{self.adult.username}'s info")

        # He sees the person's details and an update link.
        self.assertEqual(
            person_detail_page.main_text[0], f"Name: {self.adult.full_name}"
        )
        self.assertEqual(
            person_detail_page.main_text[1],
            f"Gender: {self.adult.get_gender_display()}",
        )
        self.assertEqual(person_detail_page.main_text[2], f"Age: {self.adult.age}")
        self.assertEqual(
            person_detail_page.main_text[3], f"Phone number: {self.adult.phone_number}"
        )
        self.assertEqual(
            person_detail_page.update_link,
            {"Update": pages.PersonUpdatePage(self, self.adult.username).url},
        )

    def test_child_detail(self):
        # An authorized user visits a child's detail page.
        person_detail_page = pages.PersonDetailPage(self, self.child.username)
        person_detail_page.visit()

        # He knows he's in the right place because he can see the name
        # of the site in the title and header
        self.assertEqual(person_detail_page.title, self.SITE_NAME)
        self.assertEqual(person_detail_page.header.title, self.header_title)
        self.assertEqual(person_detail_page.heading, f"{self.child.username}'s info")

        # He sees the person's details and an update link.
        self.assertEqual(
            person_detail_page.main_text[0], f"Name: {self.child.full_name}"
        )
        self.assertEqual(
            person_detail_page.main_text[1],
            f"Gender: {self.child.get_gender_display()}",
        )
        self.assertEqual(person_detail_page.main_text[2], f"Age: {self.child.age}")
        self.assertEqual(
            person_detail_page.update_link,
            {"Update": pages.PersonUpdatePage(self, self.child.username).url},
        )
