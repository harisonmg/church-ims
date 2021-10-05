from django.contrib.auth.models import AnonymousUser, Permission
from django.test import RequestFactory, TestCase

from faker import Faker

from accounts.factories import UserFactory
from records import views
from records.factories import TemperatureRecordFactory
from records.models import TemperatureRecord


class TemperatureRecordsListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/records/temperature/"
        cls.table_head = """
        <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Username</th>
              <th scope="col">Temperature</th>
              <th scope="col">Time</th>
            </tr>
        </thead>
        """
        # users
        permission = Permission.objects.filter(name="Can view temperature record")
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
        self.assertTemplateUsed(response, "records/temperature_records_list.html")

    def test_context_data_contains_temperature_records(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertIn("temperature_records", response.context)

    def test_is_paginated(self):
        TemperatureRecordFactory.create_batch(11)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        self.assertTrue(response.context.get("is_paginated"))
        self.assertEqual(len(response.context.get("temperature_records")), 10)

    def test_pagination_lists_all_items(self):
        TemperatureRecordFactory.create_batch(12)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url + "?page=2")
        expected_records = list(TemperatureRecord.objects.all())[-2:]
        temp_records = list(response.context.get("temperature_records"))
        self.assertEqual(temp_records, expected_records)

    def test_response_with_no_temperature_records(self):
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        with self.assertRaises(AssertionError):
            self.assertInHTML(self.table_head, response.content.decode())
        self.assertInHTML(
            "There are no temperature records yet!", response.content.decode()
        )

    def test_response_with_temperature_records(self):
        TemperatureRecordFactory.create_batch(3)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url)
        with self.assertRaises(AssertionError):
            self.assertInHTML(
                "There are no temperature records yet!", response.content.decode()
            )
        self.assertInHTML(self.table_head, response.content.decode())

    def test_search_by_full_name(self):
        # setup
        temp_records = TemperatureRecordFactory.create_batch(10)
        search_term = temp_records[0].person.full_name
        self.client.force_login(self.authorized_user)

        # test
        response = self.client.get(f"{self.url}?q={search_term}")
        response_temp_records = response.context.get("temperature_records")
        filtered_temp_records = TemperatureRecord.objects.filter(
            person__full_name__icontains=search_term
        )
        self.assertAlmostEqual(list(response_temp_records), list(filtered_temp_records))

    def test_search_by_name(self):
        # setup
        temp_records = TemperatureRecordFactory.create_batch(10)
        search_term = temp_records[0].person.full_name.split()[0]
        self.client.force_login(self.authorized_user)

        # test
        response = self.client.get(f"{self.url}?q={search_term}")
        response_temp_records = response.context.get("temperature_records")
        filtered_temp_records = TemperatureRecord.objects.filter(
            person__full_name__icontains=search_term
        )
        self.assertAlmostEqual(list(response_temp_records), list(filtered_temp_records))

    def test_search_by_username(self):
        # setup
        temp_records = TemperatureRecordFactory.create_batch(10)
        search_term = temp_records[0].person.username
        self.client.force_login(self.authorized_user)

        # test
        response = self.client.get(f"{self.url}?q={search_term}")
        response_temp_records = response.context.get("temperature_records")
        filtered_temp_records = TemperatureRecord.objects.filter(
            person__username__icontains=search_term
        )
        self.assertAlmostEqual(list(response_temp_records), list(filtered_temp_records))

    def test_response_with_no_search_results(self):
        TemperatureRecordFactory.create_batch(10)
        self.client.force_login(self.authorized_user)
        response = self.client.get(self.url + "?q=Does not exist")
        self.assertEqual(list(response.context.get("temperature_records")), [])
        with self.assertRaises(AssertionError):
            self.assertInHTML(self.table_head, response.content.decode())
        self.assertInHTML(
            "Your search didn't yield any results", response.content.decode()
        )


class TemperatureRecordCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "/records/temperature/username/add/"
        cls.view = views.TemperatureRecordCreateView

    def test_template_used(self):
        factory = RequestFactory()
        request = factory.get("dummy_path/")
        request.user = AnonymousUser

        response = self.view.as_view()(request)
        with self.assertTemplateUsed("records/temperature_record_form.html"):
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
