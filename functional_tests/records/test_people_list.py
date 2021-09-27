from django.contrib.auth.models import Permission

from accounts.factories import UserFactory
from functional_tests.base import FunctionalTestCase
from functional_tests.pages import LoginPage
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
        login_page = LoginPage(self).visit()
        login_page.get_attributes().login(self.user.email, self.password)

    def get_parent_attribute(self, element, attribute="class"):
        return element.find_element_by_xpath("..").get_attribute(attribute)

    def get_page_attributes(self):
        self.assertEqual(self.browser.title, self.get_site_name())
        self.assertEqual(self.browser.find_element_by_tag_name("h1").text, "People")

        sidebar_navigation = self.browser.find_element_by_id("sidebarMenu")
        people_link = sidebar_navigation.find_element_by_link_text("People")
        self.assertIn("active", people_link.get_attribute("class"))

    def get_page_navigation_links(self):
        page_navigation = self.browser.find_element_by_css_selector("nav .pagination")
        page_navigation_links = page_navigation.find_elements_by_css_selector("li a")
        return page_navigation_links

    def get_people_list(self):
        people_table = self.browser.find_element_by_tag_name("table")
        self.assertEqual(
            people_table.find_element_by_tag_name("thead").text, "# Username Full name"
        )
        people_list = people_table.find_elements_by_css_selector("tbody tr")
        return people_list

    def get_search_form(self):
        search_form = self.browser.find_element_by_id("search_form")
        search_input = search_form.find_element_by_css_selector("input[type='search']")
        self.assertEqual(search_input.get_attribute("placeholder"), "Search")
        search_button = search_form.find_element_by_css_selector(
            "button[type='submit']"
        )
        self.assertEqual(search_button.text, "Search")
        return search_input, search_button

    def test_people_list(self):
        # An authorized user clicks on the people link on the sidebar
        self.login()
        self.browser.find_element_by_link_text("People").click()

        # He is redirected to the people list page
        self.assertEqual(self.browser.current_url, self.live_server_url + "/people/")
        self.get_page_attributes()

        # He sees a list of people and a page navigation
        people_list = self.get_people_list()
        person = self.people[0]
        self.assertEqual(people_list[0].text, f"1 {person.username} {person.full_name}")
        self.assertEqual(len(people_list), 10)

        page_navigation_links = self.get_page_navigation_links()
        self.assertEqual(len(page_navigation_links), 6)
        self.assertIn("disabled", self.get_parent_attribute(page_navigation_links[0]))

        # He clicks on the last link in the page navigation and is redirected
        # to that page. The page also contains a list of people and a page navigation
        page_navigation_links[-1].click()

        self.get_page_attributes()

        people_list = self.get_people_list()
        person = self.people[-2]
        self.assertEqual(
            people_list[-2].text, f"4 {person.username} {person.full_name}"
        )
        self.assertEqual(len(people_list), 5)

        page_navigation_links = self.get_page_navigation_links()
        self.assertEqual(len(page_navigation_links), 6)

        self.assertEqual(
            page_navigation_links[-2].get_attribute("href"), self.browser.current_url
        )
        self.assertIn("active", self.get_parent_attribute(page_navigation_links[-2]))
        self.assertIn("disabled", self.get_parent_attribute(page_navigation_links[-1]))

    def test_people_list_search(self):
        # An authorized user visits the people list page
        self.login()
        self.browser.get(self.live_server_url + "/people/")
        self.get_page_attributes()

        # He sees a list of people, a page navigation and a search form
        # with placeholders
        people_list = self.get_people_list()
        person = self.people[0]
        self.assertEqual(people_list[0].text, f"1 {person.username} {person.full_name}")
        self.assertEqual(len(people_list), 10)

        self.get_search_form()

        page_navigation_links = self.get_page_navigation_links()
        self.assertEqual(len(page_navigation_links), 6)
        self.assertIn("disabled", self.get_parent_attribute(page_navigation_links[0]))

        # He decides to search for a person that exists
        search_input, search_button = self.get_search_form()
        person = self.people[20]
        search_input.send_keys(person.full_name)
        search_button.click()

        people_list = self.get_people_list()
        self.assertEqual(len(people_list), 1)

        # He decides to search for a person that doesn't exist
        search_input, search_button = self.get_search_form()
        search_input.send_keys("Does not exist")
        search_button.click()

        self.assertEqual(
            self.browser.find_element_by_css_selector("p.lead").text,
            "Your search didn't yield any results",
        )
