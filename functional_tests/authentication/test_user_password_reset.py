import re

from django.core import mail

from accounts.factories import UserFactory
from functional_tests.base import FunctionalTestCase


class PasswordResetTestCase(FunctionalTestCase):

    def test_that_a_user_can_reset_their_password(self):
        # An existing user wants to log in to the site, but they
        # have forgotten their password. She visits the login page
        self.browser.get(self.live_server_url + "/accounts/login/")
        self.assertEqual(self.browser.find_element_by_tag_name("h1").text, "Log in")

        # She knows she's in the right place because she can see the name
        # of the site in the navigation bar
        self.assertEqual(
            self.browser.find_element_by_css_selector("header > a").text,
            self.get_site_name(),
        )

        # She sees the inputs of the login form, including labels and placeholders
        self.assertEqual(self.browser.find_element_by_css_selector("h1").text, "Log in")

        login_form = self.browser.find_element_by_id("login_form")
        login_form.find_element_by_css_selector("input#id_login")
        self.assertEqual(
            login_form.find_element_by_css_selector("label[for='id_login']").text,
            "E-mail*",
        )

        login_form.find_element_by_css_selector("input#id_password")
        self.assertEqual(
            login_form.find_element_by_css_selector("label[for='id_password']").text,
            "Password*",
        )

        login_button = login_form.find_element_by_css_selector("button[type='submit']")
        self.assertEqual(login_button.text, "Log in")

        # She also sees links for signing up and password reset
        login_form.find_element_by_link_text("Sign up")

        password_reset_link = login_form.find_element_by_link_text(
            "I don't remember my password"
        )

        self.assertEqual(
            password_reset_link.get_attribute("href"),
            self.live_server_url + "/accounts/password/reset/",
        )

        # She clicks on the password reset link and is redirected to the
        # password reset page, where she sees an email input and placeholder
        # on the password reset form
        password_reset_link.click()
        self.assertEqual(
            self.browser.current_url, self.live_server_url + "/accounts/password/reset/"
        )
        self.assertEqual(
            self.browser.find_element_by_tag_name("h1").text, "Password reset"
        )

        password_reset_form = self.browser.find_element_by_id("password_reset_form")
        email_input = password_reset_form.find_element_by_css_selector("input#id_email")
        self.assertEqual(
            password_reset_form.find_element_by_css_selector(
                "label[for='id_email']"
            ).text,
            "E-mail*",
        )

        password_reset_button = password_reset_form.find_element_by_css_selector(
            "button[type='submit']"
        )
        self.assertEqual(password_reset_button.text, "Reset my password")

        # She enters her email and clicks the password reset button
        user = UserFactory()
        email_input.send_keys(user.email)
        password_reset_button.click()

        # She is redirected to the password reset done page and receives an
        # email with instructions for resetting her password
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + "/accounts/password/reset/done/",
        )
        self.assertEqual(
            self.browser.find_element_by_tag_name("h1").text, "Password reset"
        )

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn(user.email, email.to)
        self.assertIn("Click the link below to reset your password", email.body)

        # The email has a password reset link
        url = re.search(r"(?P<url>https?://[^\s]+)", email.body).group("url")
        self.assertIn(self.live_server_url, url)

        # She clicks the link and is taken to the password reset page
        self.browser.get(url)
        self.assertEqual(
            self.browser.find_element_by_tag_name("h1").text, "Change password"
        )

        # She sees the inputs of the password change form,
        # including labels and placeholders
        password_change_form = self.browser.find_element_by_id("password_change_form")
        password_input = password_change_form.find_element_by_css_selector(
            "input#id_password1"
        )
        self.assertEqual(
            password_change_form.find_element_by_css_selector(
                "label[for='id_password1']"
            ).text,
            "New Password*",
        )

        password_confirmation_input = password_change_form.find_element_by_css_selector(
            "input#id_password2"
        )
        self.assertEqual(
            password_change_form.find_element_by_css_selector(
                "label[for='id_password2']"
            ).text,
            "New Password (again)*",
        )

        password_change_button = password_change_form.find_element_by_css_selector(
            "button[type='submit']"
        )
        self.assertEqual(password_change_button.text, "Change password")

        # She enters a new password and clicks password change button
        # to send the form
        password = self.fake.password()
        password_input.send_keys(password)
        password_confirmation_input.send_keys(password)
        password_change_button.click()

        # The password reset is successful
        self.assertEqual(
            self.browser.current_url,
            self.live_server_url + "/accounts/password/reset/key/done/",
        )
        self.assertEqual(
            self.browser.find_element_by_tag_name("h1").text, "Password reset complete"
        )
        self.browser.find_element_by_link_text("log in")

        alerts = self.browser.find_elements_by_class_name("alert")
        self.assertEqual(alerts[0].text, "Password successfully changed.")
