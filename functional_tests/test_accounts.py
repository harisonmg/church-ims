import time

from selenium import webdriver

from .base import FunctionalTestCase


class AdminTestCase(FunctionalTestCase):
    """Test the functionality of the accounts feature to superusers
    and users with staff permissions
    """

    def setUp(self):
        self.browser = webdriver.Firefox(options=self.browser_options)

        self.admin_user = self.User.objects.create_superuser(
            username="Kelvin", email="kelvin@murage.com", password="kelvinpassword"
        )

        self.user1 = self.User.objects.create_user(
            username="AlvinMukuna",
            email="alvin@mukuna.com",
            phone_number="+254 701 234 567",
            password="alvinpassword",
        )

        self.user2 = self.User.objects.create_user(
            username="BrianKimani",
            email="brian@kimani.com",
            phone_number="+254 712 345 678",
            password="brianpassword",
        )

        self.user3 = self.User.objects.create_user(
            username="ChristineKyalo",
            email="christine@kyalo.com",
            phone_number="+254 723 456 789",
            password="christinepassword",
        )

    def test_that_an_admin_can_manage_groups_and_user_permissions(self):
        """Tests that a superuser can manage group and user permissions"""
        # Kelvin would like to give Christine permissions to login
        # to the admin site and add books for other viewers to read.
        # He visits the admin site
        self.browser.get(self.get_admin_url())

        # He can tell he's in the right place because of the title
        self.assertEqual(self.browser.title, "Log in | StAnds IMS admin")

        # He enters his email and password and submits the form to
        # log in
        login_form = self.browser.find_element_by_id("login-form")
        login_form.find_element_by_name("username").send_keys("Kelvin")
        login_form.find_element_by_name("password").send_keys("kelvinpassword")
        login_form.find_element_by_css_selector(".submit-row input").click()

        # He sees links to ACCOUNTS, Users, AUTHENTICATION
        # AND AUTHORIZATION and Groups
        self.assertEqual(
            self.browser.find_element_by_link_text("ACCOUNTS").get_attribute("href"),
            self.get_admin_url() + "accounts/",
        )

        self.assertEqual(
            self.browser.find_element_by_link_text("Users").get_attribute("href"),
            self.get_admin_url() + "accounts/customuser/",
        )

        self.assertEqual(
            self.browser.find_element_by_link_text(
                "AUTHENTICATION AND AUTHORIZATION"
            ).get_attribute("href"),
            self.get_admin_url() + "auth/",
        )

        self.assertEqual(
            self.browser.find_element_by_link_text("Groups").get_attribute("href"),
            self.get_admin_url() + "auth/group/",
        )

        # He clicks on the Groups link
        self.browser.find_element_by_css_selector("#site-name a").click()

        self.browser.find_element_by_link_text("Groups").click()

        # He creates a group with create, edit and view permissions
        # for the User model in the Accounts app
        self.browser.find_element_by_link_text("ADD GROUP").click()
        group_form = self.browser.find_element_by_id("group_form")
        group_form.find_element_by_name("name").send_keys("Editors")
        group_form.find_element_by_id("id_permissions_input").send_keys("accounts")

        permissions_to_add = group_form.find_element_by_name("permissions_old")
        options_to_choose = [1, -1]
        for choice in options_to_choose:
            permissions_to_add.find_elements_by_tag_name("option")[choice].click()
            group_form.find_element_by_link_text("Choose").click()

        group_form.find_element_by_css_selector(".submit-row input").click()

        self.assertEqual(
            self.browser.find_elements_by_css_selector("#result_list tr")[1].text,
            "Editors",
        )

        # Going back to the home page of the admin, he clicks the
        # Users link and sees all users who have registered
        # to the site. They are ordered by first name
        self.browser.find_element_by_css_selector("#site-name a").click()
        self.browser.find_element_by_link_text("Users").click()

        user_rows = self.browser.find_elements_by_css_selector("#result_list tr")
        self.assertEqual(
            user_rows[1].text, "AlvinMukuna alvin@mukuna.com +254701234567"
        )
        self.assertEqual(
            user_rows[2].text, "BrianKimani brian@kimani.com +254712345678"
        )
        self.assertEqual(
            user_rows[3].text, "ChristineKyalo christine@kyalo.com +254723456789"
        )
        self.assertEqual(user_rows[4].text, "Kelvin kelvin@murage.com")

        # He also sees links to change the users information
        self.assertIsNotNone(
            self.browser.find_element_by_link_text("AlvinMukuna").get_attribute("href")
        )

        self.assertIsNotNone(
            self.browser.find_element_by_link_text("BrianKimani").get_attribute("href")
        )

        self.assertIsNotNone(
            self.browser.find_element_by_link_text("ChristineKyalo").get_attribute(
                "href"
            )
        )

        # At the moment, Christine can't login to the admin site
        christines_details = self.browser.find_elements_by_css_selector(
            "#result_list tr"
        )[3]

        self.assertEqual(
            christines_details.find_element_by_css_selector(
                ".field-is_staff img"
            ).get_attribute("alt"),
            "False",
        )

        # He clicks on Christine's link to add her to the
        # editors group
        self.browser.find_element_by_link_text("ChristineKyalo").click()

        time.sleep(1)
        user_form = self.browser.find_element_by_id("customuser_form")
        user_form.find_element_by_name("is_staff").click()
        user_form.find_element_by_name("groups_old").find_elements_by_tag_name(
            "option"
        )[0].click()
        user_form.find_element_by_link_text("Choose").click()
        user_form.find_element_by_css_selector(".submit-row input").click()

        #  Christine is now able to login to the admin panel
        christines_details = self.browser.find_elements_by_css_selector(
            "#result_list tr"
        )[3]

        self.assertEqual(
            christines_details.text, "ChristineKyalo christine@kyalo.com +254723456789"
        )

        self.assertEqual(
            christines_details.find_element_by_css_selector(
                ".field-is_staff img"
            ).get_attribute("alt"),
            "True",
        )


class MemberTestCase(FunctionalTestCase):
    """Tests the functionality of the accounts feature to members
    and unregistered users
    """

    def setUp(self):
        self.browser = webdriver.Firefox(options=self.browser_options)

    def test_that_a_user_can_register_and_login(self):
        # Alex would like to attend a service at StAnds.
        # He visits the home page of StAnds IMS
        self.browser.get(self.live_server_url + "/")

        # He knows he's in the right place because he can see the
        # name of the site in the navbar, as well as calls-to-action
        # in the heading and adjacent paragraph.
        self.assertEqual(
            self.browser.find_element_by_css_selector("#mainNavigation h3").text,
            "StAnds IMS",
        )

        # He sees two call-to-action buttons, which are links for
        # the register and login pages.
        cta_buttons = self.browser.find_elements_by_css_selector("p.lead .btn")
        self.assertEqual(len(cta_buttons), 2)

        register_link, login_link = cta_buttons

        self.assertEqual("Register", register_link.text)
        self.assertEqual("Log in", login_link.text)
        self.assertEqual(
            register_link.get_attribute("href"),
            self.live_server_url + "/accounts/register/",
        )
        self.assertEqual(
            login_link.get_attribute("href"), self.live_server_url + "/accounts/login/"
        )

        # He doesn't have an account and therefore decides to
        # register. He clinks on the register link and is redirected
        # to the register page, where he sees the inputs of the
        # register form, including labels and placeholders.
        register_link.click()

        register_form = self.browser.find_element_by_id("register_form")
        self.assertEqual(
            register_form.find_element_by_css_selector("h1").text, "Register"
        )

        username_input = register_form.find_element_by_css_selector("input#id_username")
        self.assertEqual(
            register_form.find_element_by_css_selector('label[for="id_username"]').text,
            "Username*",
        )

        email_input = register_form.find_element_by_css_selector("input#id_email")
        self.assertEqual(
            register_form.find_element_by_css_selector('label[for="id_email"]').text,
            "Email address*",
        )

        phone_number_input = register_form.find_element_by_css_selector(
            "input#id_phone_number"
        )
        self.assertEqual(
            register_form.find_element_by_css_selector(
                'label[for="id_phone_number"]'
            ).text,
            "Phone number*",
        )
        self.assertEqual(
            register_form.find_element_by_css_selector(
                "small#hint_id_phone_number"
            ).text,
            "Enter a valid phone number",
        )

        password_input = register_form.find_element_by_css_selector(
            "input#id_password1"
        )
        self.assertEqual(
            register_form.find_element_by_css_selector(
                'label[for="id_password1"]'
            ).text,
            "Password*",
        )
        password_input_help_text_list = register_form.find_elements_by_css_selector(
            "small#hint_id_password1 li"
        )
        self.assertEqual(len(password_input_help_text_list), 4)

        password_confirmation_input = register_form.find_element_by_css_selector(
            "input#id_password2"
        )
        self.assertEqual(
            register_form.find_element_by_css_selector(
                'label[for="id_password2"]'
            ).text,
            "Password confirmation*",
        )

        register_button = register_form.find_element_by_css_selector(
            'button[type="submit"]'
        )
        self.assertEqual(register_button.text, "Register")

        # He keys in his first name, last name, email, phone number
        # and password and clicks register button to send the form.
        username_input.send_keys("AlexanderGithinji")
        email_input.send_keys("alex@githinji.com")
        phone_number_input.send_keys("+254 745 678 901")
        password_input.send_keys("alexpassword")
        password_confirmation_input.send_keys("alexpassword")
        register_form.find_element_by_css_selector('button[type="submit"]').click()

        # He is redirected to the login page, where he sees the inputs
        # of the login form, including labels and placeholders
        login_form = self.browser.find_element_by_id("login_form")
        self.assertEqual(login_form.find_element_by_css_selector("h1").text, "Login")

        username_input = login_form.find_element_by_css_selector("input#id_username")
        self.assertEqual(
            login_form.find_element_by_css_selector('label[for="id_username"]').text,
            "Username*",
        )

        password_input = login_form.find_element_by_css_selector("input#id_password")
        self.assertEqual(
            login_form.find_element_by_css_selector('label[for="id_password"]').text,
            "Password*",
        )

        # He enters his email and password and clicks the login button
        # to log in to the resource center.
        username_input.send_keys("AlexanderGithinji")
        password_input.send_keys("alexpassword")
        login_form.find_element_by_css_selector('button[type="submit"]').click()

        # The login was successful and he is redirected to his dashboard,
        # where he can add his personal details and family members
        # self.assertEqual(
        #     self.browser.current_url,
        #     self.live_server_url + "/accounts/AlexanderGithinji/update/",
        # )
