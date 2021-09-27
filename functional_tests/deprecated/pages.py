from selenium.common.exceptions import NoSuchElementException


class LoginPage:
    def __init__(self, test):
        self.test = test

    def get_attributes(self):
        self.title = self.test.browser.title
        self.test.assertEqual(self.title, self.test.get_site_name())

        self.h1 = self.test.browser.find_element_by_css_selector("h1").text
        self.test.assertEqual(self.h1, "Log in")

        # login form
        self.login_form = self.test.browser.find_element_by_id("login_form")
        self.email_input = self.login_form.find_element_by_css_selector(
            "input#id_login"
        )
        self.test.assertEqual(
            self.login_form.find_element_by_css_selector("label[for='id_login']").text,
            "E-mail*",
        )

        self.password_input = self.login_form.find_element_by_css_selector(
            "input#id_password"
        )
        self.test.assertEqual(
            self.login_form.find_element_by_css_selector(
                "label[for='id_password']"
            ).text,
            "Password*",
        )

        self.login_button = self.login_form.find_element_by_css_selector(
            "button[type='submit']"
        )
        self.test.assertEqual(self.login_button.text, "Log in")

        # alternative action links
        self.signup_link = self.login_form.find_element_by_link_text("Sign up")
        self.password_reset_link = self.login_form.find_element_by_link_text(
            "I don't remember my password"
        )
        self.test.assertEqual(
            self.password_reset_link.get_attribute("href"),
            self.test.live_server_url + "/accounts/password/reset/",
        )
        return self

    def login(self, email, password):
        self.email_input.send_keys(email)
        self.password_input.send_keys(password)
        self.login_button.click()


class PeopleListPage:
    def __init__(self, test):
        self.test = test

    def get_attributes(self):
        self.title = self.test.browser.title
        self.test.assertEqual(self.title, self.test.get_site_name())

        self.h1 = self.test.browser.find_element_by_tag_name("h1").text
        self.test.assertEqual(self.h1, "People")

        # sidebar
        self.sidebar_navigation = self.test.browser.find_element_by_id("sidebarMenu")
        people_link = self.sidebar_navigation.find_element_by_link_text("People")
        self.test.assertIn("active", people_link.get_attribute("class"))

        # people list
        self._get_people_list()

        # search form
        self._get_search_form()

        # pagination
        return self

    def _get_people_list(self):
        try:
            self.people_table = self.test.browser.find_element_by_tag_name("table")
            self.test.assertEqual(
                self.people_table.find_element_by_tag_name("thead").text,
                "# Username Full name",
            )
            self.people_list = self.people_table.find_elements_by_css_selector(
                "tbody tr"
            )
        except NoSuchElementException:
            pass

    def _get_search_form(self):
        try:
            self.search_form = self.test.browser.find_element_by_id("search_form")
            self.search_input = self.search_form.find_element_by_css_selector(
                "input[type='search']"
            )
            self.test.assertEqual(
                self.search_input.get_attribute("placeholder"), "Search"
            )
            self.search_button = self.search_form.find_element_by_css_selector(
                "button[type='submit']"
            )
            self.test.assertEqual(self.search_button.text, "Search")
        except NoSuchElementException:
            pass

    def search(self, search_term):
        self.search_input.send_keys(search_term)
        self.search_button.click()
        return self.get_attributes()
