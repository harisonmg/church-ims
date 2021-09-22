class LoginPage:
    def __init__(self, test):
        self.test = test
        self.path = "/accounts/login/"

    def get_attributes(self):
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

    def visit(self):
        url = self.test.live_server_url + self.path
        self.test.browser.get(url)
        return self
