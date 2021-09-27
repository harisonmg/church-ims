import re

from django.core import mail
from django.test import override_settings

from functional_tests.base import FunctionalTestCase


@override_settings(ACCOUNT_EMAIL_VERIFICATION="mandatory")
class SignUpTestCase(FunctionalTestCase):
    def test_that_a_user_can_signup(self):
        # A user visits the home page
        self.browser.get(self.live_server_url)
        self.assertEqual(self.browser.title, self.get_site_name())
        self.assertEqual(
            self.browser.find_element_by_tag_name("h1").text, self.get_site_name()
        )

        # She knows she's in the right place because she can see the name
        # of the site in the navigation bar
        self.assertEqual(
            self.browser.find_element_by_css_selector("header > a").text,
            self.get_site_name(),
        )

        # She sees two call-to-action buttons, which are links for
        # the sign up and login pages.
        cta_buttons = self.browser.find_elements_by_css_selector("main .btn")
        self.assertEqual(len(cta_buttons), 2)

        signup_link, login_link = cta_buttons

        self.assertEqual("Sign up", signup_link.text)
        self.assertEqual("Log in", login_link.text)
        self.assertEqual(
            signup_link.get_attribute("href"),
            self.live_server_url + "/accounts/signup/",
        )
        self.assertEqual(
            login_link.get_attribute("href"), self.live_server_url + "/accounts/login/"
        )

        # She doesn't have an account and therefore decides to register. She clicks
        # on the sign up link and is redirected to the sign up page, where she sees
        # the inputs of the sign up form, including labels and placeholders.
        signup_link.click()

        self.assertEqual(self.browser.title, self.get_site_name())
        self.assertEqual(
            self.browser.find_element_by_css_selector("h1").text, "Sign up"
        )

        signup_form = self.browser.find_element_by_id("signup_form")
        email_input = signup_form.find_element_by_css_selector("input#id_email")
        self.assertEqual(
            signup_form.find_element_by_css_selector("label[for='id_email']").text,
            "E-mail*",
        )

        password_input = signup_form.find_element_by_css_selector("input#id_password1")
        self.assertEqual(
            signup_form.find_element_by_css_selector("label[for='id_password1']").text,
            "Password*",
        )

        password_confirmation_input = signup_form.find_element_by_css_selector(
            "input#id_password2"
        )
        self.assertEqual(
            signup_form.find_element_by_css_selector("label[for='id_password2']").text,
            "Password (again)*",
        )

        signup_button = signup_form.find_element_by_css_selector(
            "button[type='submit']"
        )
        self.assertEqual(signup_button.text, "Sign up")

        # She also sees a login link
        signup_form.find_element_by_link_text("Log in")

        # She keys in his first name, last name, email, phone number
        # and password and clicks the sign up button to send the form.
        user_email = self.fake.email()
        email_input.send_keys(user_email)
        user_password = self.fake.password()
        password_input.send_keys(user_password)
        password_confirmation_input.send_keys(user_password)
        signup_button.click()

        # The sign up was successful and she is redirected to the email
        # verification page
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + "/accounts/confirm-email/",
        )
        self.assertEqual(self.browser.title, self.get_site_name())
        self.assertEqual(
            self.browser.find_element_by_tag_name("h1").text,
            "Verify your email address",
        )

        alerts = self.browser.find_elements_by_class_name("alert")
        self.assertEqual(alerts[0].text, f"Confirmation e-mail sent to {user_email}.")

        # She receives an email with a link for verifying her email address
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn(user_email, email.to)
        self.assertIn("To confirm this is correct, go to", email.body)

        url = re.search(r"(?P<url>https?://[^\s]+)", email.body).group("url")
        self.assertIn(self.live_server_url, url)

        # She clicks the link and is taken to the email confirmation page
        self.browser.get(url)
        self.assertEqual(self.browser.title, self.get_site_name())
        self.assertEqual(
            self.browser.find_element_by_tag_name("h1").text, "Confirm email address"
        )
        self.browser.find_element_by_link_text(user_email)

        email_confirmation_form = self.browser.find_element_by_id(
            "email_confirmation_form"
        )
        email_confirmation_button = (
            email_confirmation_form.find_element_by_css_selector(
                "button[type='submit']"
            )
        )
        self.assertEqual(email_confirmation_button.text, "Confirm")

        # She clicks on the confirm button to verify her email
        # and is redirected to the login page
        email_confirmation_button.click()

        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + "/accounts/login/",
        )
        self.assertEqual(self.browser.title, self.get_site_name())
        self.assertEqual(self.browser.find_element_by_tag_name("h1").text, "Log in")

        alerts = self.browser.find_elements_by_class_name("alert")
        self.assertEqual(alerts[0].text, f"You have confirmed {user_email}.")

    def test_invalid_email_confirmation_link(self):
        # A user who recently signed up opens the email that was sent
        # to verify their email. They click on the link provided
        url = self.live_server_url + "/accounts/confirm-email/expired-token/"
        self.browser.get(url)
        self.assertEqual(self.browser.title, self.get_site_name())
        self.assertEqual(
            self.browser.find_element_by_tag_name("h1").text, "Confirm email address"
        )
        self.browser.find_element_by_link_text(
            "issue a new e-mail confirmation request"
        )
