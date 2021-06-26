import time

from selenium import webdriver

from children.models import Child, ParentChildRelationship, RelationshipType

from .base import FunctionalTestCase

class AdminTestCase(FunctionalTestCase):
    """Test the functionality of the children feature to superusers
    and users with staff permissions
    """

    def setUp(self):
        self.browser = webdriver.Firefox(options=self.browser_options)

        self.admin_user = self.User.objects.create_superuser(
            username="Kelvin",
            email="kelvin@murage.com",
            password="kelvinpassword"
        )

        self.alvin = self.User.objects.create(
            username="AlvinMukuna",
            email="alvin@mukuna.com",
            phone_number="+254 701 234 567",
            password="alvinpassword"
        )

        self.christine = self.User.objects.create(
            username="ChristineKyalo",
            email="christine@kyalo.com",
            phone_number="+254 723 456 789",
            password="christinepassword"
        )

        self.abigael = Child.objects.create(
            slug="AbigaelAuma",
            full_name="Abigael Auma",
            dob="2015-05-14",
            gender="F",
            created_by=self.alvin,
        )

        self.brian = Child.objects.create(
            slug="BrianKimani",
            full_name="Brian Kimani",
            dob="2018-09-23",
            gender="M",
            created_by=self.christine,
        )

        self.mother = RelationshipType.objects.create(name='mother')
        self.father = RelationshipType.objects.create(name='daughter')

        self.abigael_father = ParentChildRelationship(
            parent=self.alvin,
            child=self.abigael,
            relationship_type=self.father,
            created_by=self.alvin
        )
        self.abigael_father.save()

        self.brian_mother = ParentChildRelationship(
            parent=self.christine,
            child=self.brian,
            relationship_type=self.mother,
            created_by=self.christine
        )
        self.brian_mother.save()


    def test_that_a_staff_can_manage_children(self):
        # Kelvin would like to check existing members records and add
        # details for users that are not willing to register by
        # themselves. He visits the admin site
        self.browser.get(self.get_admin_url())

        # He can tell he's in the right place because of the title
        self.assertEqual(self.browser.title, "Log in | StAnds IMS admin")

        # He enters his email and password and submits the form to
        # log in
        login_form = self.browser.find_element_by_id("login-form")
        login_form.find_element_by_name("username").send_keys("Kelvin")
        login_form.find_element_by_name("password").send_keys("kelvinpassword")
        login_form.find_element_by_css_selector(".submit-row input").click()

        # He sees links to CHILDREN, Child, Relationship types
        # and Parent child relationships
        self.assertEqual(
            self.browser.find_element_by_link_text('CHILDREN').get_attribute('href'),
            self.get_admin_url() + 'children/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text('Children').get_attribute('href'),
            self.get_admin_url() + 'children/child/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text('Relationship types').get_attribute('href'),
            self.get_admin_url() + 'children/relationshiptype/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text('Parent child relationships').get_attribute('href'),
            self.get_admin_url() + 'children/parentchildrelationship/'
        )

        # Kelvin wants to add and update children's details and those
        # their children to StAnds IMS. He goes back to the homepage
        # of the admin site
        self.browser.find_element_by_css_selector('#site-name a').click()
        self.browser.find_element_by_link_text('Children').click()

        # He's sees the children's details listed alphabetically by username
        children_rows = self.browser.find_elements_by_css_selector('#result_list tr')

        self.assertEqual(
            children_rows[1].text,
            'AbigaelAuma Abigael Auma 6 Female'
        )
        self.assertEqual(
            children_rows[2].text,
            'BrianKimani Brian Kimani 2 Male'
        )

        # He adds a child's records to a parent that already exists
        self.browser.find_element_by_css_selector('#site-name a').click()
        self.browser.find_element_by_link_text('Parent child relationships').click()        
        self.browser.find_element_by_link_text('ADD PARENT CHILD RELATIONSHIP').click()

        relationships_form = self.browser.find_element_by_id('parentchildrelationship_form')
        relationships_form.find_element_by_name('parent').find_elements_by_tag_name('option')[1].click()
        relationships_form.find_element_by_id('add_id_child').click()
        self.browser.switch_to.window(self.browser.window_handles[1])

        import time; time.sleep(0.5)
        child_form = self.browser.find_element_by_id('child_form')
        child_form.find_element_by_name('slug').send_keys('DavidKamau')
        child_form.find_element_by_name('full_name').send_keys('David Kamau')
        child_form.find_element_by_name('dob').send_keys('25/06/2012')
        child_form.find_element_by_name('gender').find_elements_by_tag_name('option')[1].click()
        child_form.find_element_by_name('created_by').find_elements_by_tag_name('option')[1].click()
        self.browser.find_element_by_css_selector('.submit-row input').click()
        self.browser.switch_to.window(self.browser.window_handles[0])

        relationships_form = self.browser.find_element_by_id('parentchildrelationship_form')
        relationships_form.find_element_by_name('relationship_type').find_elements_by_tag_name('option')[1].click()
        relationships_form.find_element_by_name('created_by').find_elements_by_tag_name('option')[1].click()
        self.browser.find_elements_by_css_selector('.submit-row input')[0].click()
