from selenium import webdriver

from .base import FunctionalTestCase


class AdminTestCase(FunctionalTestCase):
    """Test the functionality of the accounts feature to superusers
    and users with staff permissions
    """
    def setUp(self):
        self.browser = webdriver.Firefox(options=self.browser_options)

        self.admin_user = self.User.objects.create_superuser(
            username = 'Kelvin',
            email='kelvin@murage.com',
            password='kelvinpassword'
        )

        self.user1 = self.User.objects.create_user(
            username = 'AlvinMukuna',
            email = 'alvin@mukuna.com',
            phone_number = '+254 701 234 567',
            password = 'alvinpassword'
        )

        self.user2 = self.User.objects.create_user(
            username = 'BrianKimani',
            email = 'brian@kimani.com',
            phone_number = '+254 712 345 678',
            password = 'brianpassword'
        )

        self.user3 = self.User.objects.create_user(
            username = 'ChristineKyalo',
            email = 'christine@kyalo.com',
            phone_number = '+254 723 456 789',
            password = 'christinepassword'
        )

    def test_that_an_admin_can_manage_groups_and_user_permissions(self):
        """Tests that a superuser can manage group and user permissions
        """
        # Kelvin would like to give Christine permissions to login
        # to the admin site and add books for other viewers to read.
        # He visits the admin site
        self.browser.get(self.get_admin_url())

        # He can tell he's in the right place because of the title
        self.assertEqual(self.browser.title,
            'Log in | StAnds Church School IMS admin'
        )

        # He enters his email and password and submits the form to
        # log in
        login_form = self.browser.find_element_by_id(
            'login-form')
        login_form.find_element_by_name('username').\
            send_keys('Kelvin')
        login_form.find_element_by_name('password').\
            send_keys('kelvinpassword')
        login_form.find_element_by_css_selector(
            '.submit-row input').click()

        # He sees links to ACCOUNTS, Users, AUTHENTICATION
        # AND AUTHORIZATION and Groups
        self.assertEqual(
            self.browser.\
                find_element_by_link_text('ACCOUNTS').\
                    get_attribute('href'),
            self.get_admin_url() + 'accounts/'
        )

        self.assertEqual(
            self.browser.\
                find_element_by_link_text('Users').\
                    get_attribute('href'),
            self.get_admin_url() + 'accounts/customuser/'
        )

        self.assertEqual(
            self.browser.\
                find_element_by_link_text('AUTHENTICATION AND AUTHORIZATION').\
                    get_attribute('href'),
            self.get_admin_url() + 'auth/'
        )

        self.assertEqual(
            self.browser.\
                find_element_by_link_text('Groups').\
                    get_attribute('href'),
            self.get_admin_url() + 'auth/group/'
        )

        # He clicks on the Groups link
        self.browser.find_element_by_css_selector(
            '#site-name a').click()

        self.browser.find_element_by_link_text('Groups').click()

        # He creates a group with create, edit and view permissions
        # for the User model in the Accounts app
        self.browser.find_element_by_link_text('ADD GROUP').click()
        group_form = self.browser.find_element_by_id('group_form')
        group_form.find_element_by_name('name').send_keys('Editors')
        group_form.find_element_by_id('id_permissions_input').\
            send_keys('accounts')

        permissions_to_add = group_form.\
            find_element_by_name('permissions_old')
        options_to_choose = [1, -1]
        for choice in options_to_choose:
            permissions_to_add.\
                find_elements_by_tag_name('option')[choice].click()
            group_form.find_element_by_link_text('Choose').click()

        group_form.find_element_by_css_selector(
            '.submit-row input').click()

        self.assertEqual(
            self.browser.find_elements_by_css_selector(
                '#result_list tr')[1].text,
            'Editors'
        )

        # Going back to the home page of the admin, he clicks the
        # Users link and sees all users who have registered
        # to the site. They are ordered by first name
        self.browser.find_element_by_css_selector(
            '#site-name a').click()
        self.browser.find_element_by_link_text('Users').click()

        user_rows = self.browser.find_elements_by_css_selector(
            '#result_list tr')
        self.assertEqual(user_rows[1].text,
            'AlvinMukuna alvin@mukuna.com +254701234567')
        self.assertEqual(user_rows[2].text,
            'BrianKimani brian@kimani.com +254712345678')
        self.assertEqual(user_rows[3].text,
            'ChristineKyalo christine@kyalo.com +254723456789')
        self.assertEqual(user_rows[4].text,
            'Kelvin kelvin@murage.com')

        # He also sees links to change the users information
        self.assertIsNotNone(
            self.browser.find_element_by_link_text(
                'AlvinMukuna').get_attribute('href')
        )

        self.assertIsNotNone(
            self.browser.find_element_by_link_text(
                'BrianKimani').get_attribute('href')
        )

        self.assertIsNotNone(
            self.browser.find_element_by_link_text(
                'ChristineKyalo').get_attribute('href')
        )

        # At the moment, Christine can't login to the admin site
        christines_details = self.browser.\
            find_elements_by_css_selector('#result_list tr')[3]

        self.assertEqual(
            christines_details.find_element_by_css_selector(
                '.field-is_staff img').get_attribute('alt'),
            'False'
        )

        # He clicks on Christine's link to add her to the
        # editors group
        self.browser.find_element_by_link_text('ChristineKyalo').click()
        user_form = self.browser.find_element_by_id('customuser_form')
        user_form.find_element_by_name('is_staff').click()
        user_form.find_element_by_name('groups_old').\
            find_elements_by_tag_name('option')[0].click()
        user_form.find_element_by_link_text('Choose').click()
        user_form.find_element_by_css_selector(
            '.submit-row input').click()

        #  Christine is now able to login to the admin panel
        christines_details = self.browser.\
            find_elements_by_css_selector('#result_list tr')[3]

        self.assertEqual(
            christines_details.text,
            'ChristineKyalo christine@kyalo.com +254723456789'
        )

        self.assertEqual(
            christines_details.find_element_by_css_selector(
                '.field-is_staff img').get_attribute('alt'),
            'True'
        )
