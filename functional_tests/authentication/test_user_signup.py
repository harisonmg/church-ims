from functional_tests.base import FunctionalTestCase


class SignUpTestCase(FunctionalTestCase):
    def test_that_a_user_can_signup(self):
        # A user visits the home page
        self.browser.get(self.live_server_url)

        # He knows he's in the right place because he can see the name
        # of the site in the navigation bar
        self.assertEqual(
            self.browser.find_element_by_css_selector("header > a").text,
            self.get_site_name(),
        )

        # He sees two call-to-action buttons, which are links for
        # the sign up and login pages.
        cta_buttons = self.browser.find_elements_by_css_selector("main .btn")
        self.assertEqual(len(cta_buttons), 2)

        login_link, signup_link = cta_buttons

        self.assertEqual("Sign up", signup_link.text)
        self.assertEqual("Log in", login_link.text)
        self.assertEqual(
            signup_link.get_attribute("href"),
            self.live_server_url + "/accounts/signup/",
        )
        self.assertEqual(
            login_link.get_attribute("href"), self.live_server_url + "/accounts/login/"
        )

        # He doesn't have an account and therefore decides to register. He clicks
        # on the sign up link and is redirected to the sign up page, where he sees
        # the inputs of the sign up form, including labels and placeholders.
        signup_link.click()

        self.assertEqual(
            self.browser.find_element_by_css_selector("h1").text, "Sign up"
        )

        signup_form = self.browser.find_element_by_id("signup_form")
        email_input = signup_form.find_element_by_css_selector("input#id_email")
        self.assertEqual(
            signup_form.find_element_by_css_selector('label[for="id_email"]').text,
            "Email address",
        )

        password_input = signup_form.find_element_by_css_selector("input#id_password1")
        self.assertEqual(
            signup_form.find_element_by_css_selector('label[for="id_password1"]').text,
            "Password",
        )

        password_confirmation_input = signup_form.find_element_by_css_selector(
            "input#id_password2"
        )
        self.assertEqual(
            signup_form.find_element_by_css_selector('label[for="id_password2"]').text,
            "Confirm password",
        )

        signup_button = signup_form.find_element_by_css_selector(
            'button[type="submit"]'
        )
        self.assertEqual(signup_button.text, "Sign up")

        # He also sees a login link
        signup_form.find_element_by_link_text("Log in")

        # He keys in his first name, last name, email, phone number
        # and password and clicks sign up button to send the form.
        email_input.send_keys(self.fake.email())
        password = self.fake.password()
        password_input.send_keys(password)
        password_confirmation_input.send_keys(password)
        signup_form.find_element_by_css_selector('button[type="submit"]').click()

        # The sign up was successful and he is redirected to the login page
        self.assertEqual(
            self.browser.current_url, self.live_server_url + "/accounts/login/"
        )
