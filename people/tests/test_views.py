from django.contrib.auth.models import AnonymousUser, Permission
from django.test import RequestFactory, TestCase

from faker import Faker

from accounts.factories import UserFactory
from people import views
from people.factories import PersonFactory
from people.models import Person


class PeopleListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/people/"
        cls.table_head = """
        <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Username</th>
              <th scope="col">Full name</th>
              <th scope="col">Actions</th>
            </tr>
        </thead>
        """
        # users
        permission = Permission.objects.filter(name="Can view person")
        cls.user = UserFactory()
        cls.authorized_user = UserFactory(user_permissions=tuple(permission))
        cls.staff_user = UserFactory(is_staff=True)

    def test_anonymous_user_response(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_authenticated_user_response(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_authorized_user_response(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_staff_user_response(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_template_used(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "people/people_list.html")

    def test_context_data_contains_people(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertIn("people", response.context)

    def test_is_paginated(self):
        PersonFactory.create_batch(11)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertTrue(response.context.get("is_paginated"))
        self.assertEqual(len(response.context.get("people")), 10)

    def test_pagination_lists_all_items(self):
        PersonFactory.create_batch(12)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url + "?page=2")
        expected_people = list(Person.objects.all())[-2:]
        people = list(response.context.get("people"))
        self.assertEqual(people, expected_people)

    def test_response_with_no_people(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        with self.assertRaises(AssertionError):
            self.assertInHTML(self.table_head, response.content.decode())
        self.assertInHTML("There are no people yet!", response.content.decode())

    def test_response_with_people(self):
        PersonFactory.create_batch(3)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        with self.assertRaises(AssertionError):
            self.assertInHTML("There are no people yet!", response.content.decode())
        self.assertInHTML(self.table_head, response.content.decode())

    def test_search_by_full_name(self):
        # setup
        people = PersonFactory.create_batch(10)
        search_term = people[0].full_name
        self.client.force_login(self.authorized_user)

        # test
        response = self.client.get(f"{self.url}?q={search_term}")
        response_people = response.context.get("people")
        filtered_people = Person.objects.filter(full_name__icontains=search_term)
        self.assertQuerysetEqual(response_people, filtered_people)

    def test_search_by_name(self):
        # setup
        people = PersonFactory.create_batch(10)
        search_term = people[0].full_name.split()[0]
        self.client.force_login(self.authorized_user)

        # test
        response = self.client.get(f"{self.url}?q={search_term}")
        response_people = response.context.get("people")
        filtered_people = Person.objects.filter(full_name__icontains=search_term)
        self.assertQuerysetEqual(response_people, filtered_people)

    def test_search_by_username(self):
        # setup
        people = PersonFactory.create_batch(10)
        search_term = people[0].username
        self.client.force_login(self.authorized_user)

        # test
        response = self.client.get(f"{self.url}?q={search_term}")
        response_people = response.context.get("people")
        filtered_people = Person.objects.filter(username__icontains=search_term)
        self.assertQuerysetEqual(response_people, filtered_people)

    def test_response_with_no_search_results(self):
        PersonFactory.create_batch(10)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url + "?q=Does not exist")
        self.assertEqual(list(response.context.get("people")), [])
        with self.assertRaises(AssertionError):
            self.assertInHTML(self.table_head, response.content.decode())
        self.assertInHTML(
            "Your search didn't yield any results", response.content.decode()
        )


class PersonCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/people/add/"
        cls.view = views.PersonCreateView

    def test_template_used(self):
        factory = RequestFactory()
        request = factory.get("dummy_path/")
        request.user = AnonymousUser

        response = self.view.as_view()(request)
        with self.assertTemplateUsed("people/person_form.html"):
            response.render()

    def test_view_requires_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_logged_in_response_status_code(self):
        fake = Faker()
        user_password = fake.password()
        user = UserFactory(password=user_password)

        self.client.login(email=user.email, password=user_password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
