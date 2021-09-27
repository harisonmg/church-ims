from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests.base import FunctionalTestCase
from functional_tests.pages import LoginPage, PeopleListPage
from people.factories import PersonFactory


class PeopleListTestCase(FunctionalTestCase):
    def setUp(self):
        super().setUp()

        # user
        self.password = self.fake.password()
        permission = Permission.objects.filter(name="Can view person")
        self.user = UserFactory(
            password=self.password, user_permissions=tuple(permission)
        )

        # people
        people = PersonFactory.create_batch(45)
        self.people = sorted(people, key=lambda p: p.username)

    def login(self):
        self.browser.get(self.live_server_url + "/accounts/login/")
        LoginPage(self).get_attributes().login(self.user.email, self.password)

    def get_pagination_links(self):
        page_navigation = self.browser.find_element_by_css_selector("nav .pagination")
        return page_navigation.find_elements_by_css_selector("li")

    def get_active_pagination_link(self):
        return self.browser.find_element_by_css_selector(".pagination li.active a")

    def test_people_list(self):
        # An authorized user clicks on the people link on the sidebar
        self.login()
        sidebar_navigation = self.browser.find_element_by_id("sidebarMenu")
        sidebar_navigation.find_element_by_link_text("People").click()

        # He is redirected to the people list page where he sees a list
        # of people, a search form and a page navigation
        self.assertEqual(self.browser.current_url, self.live_server_url + "/people/")
        people_list_page = PeopleListPage(self).get_attributes()
        person = self.people[0]
        self.assertEqual(
            people_list_page.people_list[0].text,
            f"1 {person.username} {person.full_name}",
        )
        self.assertEqual(len(people_list_page.people_list), 10)

        pagination_links = self.get_pagination_links()
        self.assertEqual(len(pagination_links), 6)
        self.assertIn("disabled", pagination_links[0].get_attribute("class"))

        # He clicks on the last link in the page navigation and is redirected
        # to that page. The page also contains a list of people, a search form
        # and a page navigation
        pagination_links[-1].click()

        people_list_page = PeopleListPage(self).get_attributes()
        person = self.people[-2]
        self.assertEqual(
            people_list_page.people_list[-2].text,
            f"4 {person.username} {person.full_name}",
        )
        self.assertEqual(len(people_list_page.people_list), 5)

        pagination_links = self.get_pagination_links()
        self.assertEqual(len(pagination_links), 6)

        active_link = self.get_active_pagination_link()
        self.assertEqual(active_link.get_attribute("href"), self.browser.current_url)
        self.assertIn("disabled", pagination_links[-1].get_attribute("class"))

    def test_people_list_search(self):
        # An authorized user visits the people list page. He sees a list of people,
        # a page navigation and a search form with placeholders
        self.login()
        self.browser.get(self.live_server_url + "/people/")
        people_list_page = PeopleListPage(self).get_attributes()

        person = self.people[0]
        self.assertEqual(
            people_list_page.people_list[0].text,
            f"1 {person.username} {person.full_name}",
        )
        self.assertEqual(len(people_list_page.people_list), 10)

        pagination_links = self.get_pagination_links()
        self.assertEqual(len(pagination_links), 6)
        self.assertIn("disabled", pagination_links[0].get_attribute("class"))

        # He decides to search for a person that exists
        person = self.people[20]
        people_list_page = people_list_page.search(person.full_name)
        self.assertEqual(len(people_list_page.people_list), 1)

        # He decides to search for a person that doesn't exist
        people_list_page.search("Does not exist")

        self.assertEqual(
            self.browser.find_element_by_css_selector("p.lead").text,
            "Your search didn't yield any results",
        )
