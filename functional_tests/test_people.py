import time

from selenium import webdriver

from people.models import Person, RelationshipType, FamilyRelationship

from .base import FunctionalTestCase

class AdminTestCase(FunctionalTestCase):
    """Test the functionality of the people feature to superusers
    and users with staff permissions
    """

    def setUp(self):
        self.browser = webdriver.Firefox(options=self.browser_options)

        self.admin_user = self.User.objects.create_superuser(
            username="Kelvin",
            email="kelvin@murage.com",
            password="kelvinpassword"
        )

        self.alvin_user = self.User.objects.create_user(
            username="AlvinMukuna",
            email="alvin@mukuna.com",
            phone_number="+254 701 234 567",
            password="alvinpassword"
        )

        self.christine_user = self.User.objects.create_user(
            username="ChristineKyalo",
            email="christine@kyalo.com",
            phone_number="+254 723 456 789",
            password="christinepassword"
        )

        self.kelvin_person = Person.objects.create(
            slug="Kelvin",
            full_name="Kelvin Murage",
            dob="1995-06-05",
            gender="M",
            created_by=self.admin_user,
        )

        self.alvin_person = Person.objects.create(
            slug="AlvinMukuna",
            full_name="Alvin Mukuna",
            dob="1984-12-12",
            gender="M",
            created_by=self.alvin_user,
        )

        self.abigael_person = Person.objects.create(
            slug="AbigaelAuma",
            full_name="Abigael Auma",
            dob="2015-05-14",
            gender="F",
            created_by=self.alvin_user,
        )

        self.christine_person = Person.objects.create(
            slug="ChristineKyalo",
            full_name="Christine Kyalo",
            dob="1992-03-21",
            gender="F",
            created_by=self.christine_user,
        )

        self.brian_person = Person.objects.create(
            slug="BrianKimani",
            full_name="Brian Kimani",
            dob="2018-09-23",
            gender="M",
            created_by=self.christine_user,
        )

        self.son = RelationshipType.objects.create(name='son')
        self.daughter = RelationshipType.objects.create(name='daughter')

        self.alvin_daughter = FamilyRelationship(
            person=self.alvin_person,
            relative=self.abigael_person,
            relationship_type=self.daughter,
            created_by=self.alvin_user
        )
        self.alvin_daughter.save()

        self.christine_son = FamilyRelationship(
            person=self.christine_person,
            relative=self.brian_person,
            relationship_type=self.son,
            created_by=self.christine_user
        )
        self.christine_son.save()

    def find_relationships_inline(self):
        return self.browser.find_element_by_id('relationships-group')

    def add_family_relationship(self):
        self.browser.find_element_by_link_text(
            'Add another Family relationship'
        ).click()

    def test_that_a_staff_can_manage_people(self):
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

        # He sees links to PEOPLE, People, Relationship types
        # and Family member relationships
        self.assertEqual(
            self.browser.find_element_by_link_text('PEOPLE').get_attribute('href'),
            self.get_admin_url() + 'people/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text('People').get_attribute('href'),
            self.get_admin_url() + 'people/person/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text('Relationship types').get_attribute('href'),
            self.get_admin_url() + 'people/relationshiptype/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text('Family relationships').get_attribute('href'),
            self.get_admin_url() + 'people/familyrelationship/'
        )

        # Kelvin wants to add and update people's details and those
        # their children to StAnds IMS. He goes back to the homepage
        # of the admin site
        self.browser.find_element_by_css_selector(
            '#site-name a').click()

        self.browser.find_element_by_link_text('People').click()

        # He's sees the people's details listed alphabetically by username
        people_rows = self.browser.find_elements_by_css_selector('#result_list tr')

        self.assertEqual(
            people_rows[1].text,
            'AbigaelAuma Abigael Auma 6'
        )
        self.assertEqual(
            people_rows[2].text,
            'AlvinMukuna Alvin Mukuna 36'
        )
        self.assertEqual(
            people_rows[3].text,
            'BrianKimani Brian Kimani 2'
        )
        self.assertEqual(
            people_rows[4].text,
            'ChristineKyalo Christine Kyalo 29'
        )
        self.assertEqual(
            people_rows[5].text,
            'Kelvin Kelvin Murage 26'
        )

        # He adds a child's records to a parent that already exists
        self.browser.find_element_by_link_text('AlvinMukuna').click()
        relationships_inline = self.find_relationships_inline()
        relatives = relationships_inline.find_elements_by_css_selector('.field-relative')
        relatives[-2].find_element_by_css_selector('.add-related').click()
        self.browser.switch_to.window(self.browser.window_handles[1])

        import time; time.sleep(0.5)
        person_form = self.browser.find_element_by_id('person_form')
        person_form.find_element_by_name('slug').send_keys('DavidKamau')
        person_form.find_element_by_name('full_name').send_keys('David Kamau')
        person_form.find_element_by_name('dob').send_keys('25/06/2012')
        person_form.find_element_by_name('gender').find_elements_by_tag_name('option')[1].click()
        person_form.find_element_by_name('created_by').find_elements_by_tag_name('option')[1].click()
        self.browser.find_element_by_css_selector('.submit-row input').click()
        self.browser.switch_to.window(self.browser.window_handles[0])

        relationships_inline = self.find_relationships_inline()
        relationship_types = relationships_inline.find_elements_by_css_selector('.field-relationship_type')
        relationship_types[-2].find_elements_by_tag_name('option')[1].click()
        
        created_by_fields = relationships_inline.find_elements_by_css_selector('.field-created_by')
        created_by_fields[-2].find_elements_by_tag_name('option')[1].click()
        self.browser.find_elements_by_css_selector('.submit-row input')[0].click()

        # He then adds children's records to a parent that doesn't exist
        self.browser.find_element_by_link_text('ADD PERSON').click()

        person_form = self.browser.find_element_by_id('person_form')
        person_form.find_element_by_name('slug').send_keys('SheilaMwakitawa')
        person_form.find_element_by_name('full_name').send_keys('Sheila Mwakitawa')
        person_form.find_element_by_name('dob').send_keys('29/11/1987')
        person_form.find_element_by_name('gender').find_elements_by_tag_name('option')[2].click()
        person_form.find_element_by_name('created_by').find_elements_by_tag_name('option')[-1].click()

        relationships_inline = self.find_relationships_inline()
        relatives = relationships_inline.find_elements_by_css_selector('.field-relative')
        relatives[-2].find_element_by_css_selector('.add-related').click()
        self.browser.switch_to.window(self.browser.window_handles[1])

        import time; time.sleep(0.5)
        person_form = self.browser.find_element_by_id('person_form')
        person_form.find_element_by_name('slug').send_keys('FauziaAmani')
        person_form.find_element_by_name('full_name').send_keys('Fauzia Amani')
        person_form.find_element_by_name('dob').send_keys('25/06/2012')
        person_form.find_element_by_name('gender').find_elements_by_tag_name('option')[2].click()
        person_form.find_element_by_name('created_by').find_elements_by_tag_name('option')[-1].click()
        self.browser.find_element_by_css_selector('.submit-row input').click()
        self.browser.switch_to.window(self.browser.window_handles[0])

        relationships_inline = self.find_relationships_inline()
        relationship_types = relationships_inline.find_elements_by_css_selector('.field-relationship_type')
        relationship_types[-2].find_elements_by_tag_name('option')[2].click()

        created_by_fields = relationships_inline.find_elements_by_css_selector('.field-created_by')
        created_by_fields[-2].find_elements_by_tag_name('option')[-1].click()

        self.add_family_relationship()
        relationships_inline = self.find_relationships_inline()
        relatives = relationships_inline.find_elements_by_css_selector('.field-relative')
        relatives[-2].find_element_by_css_selector('.add-related').click()
        self.browser.switch_to.window(self.browser.window_handles[1])

        import time; time.sleep(0.5)
        person_form = self.browser.find_element_by_id('person_form')
        person_form.find_element_by_name('slug').send_keys('SwalehHassan')
        person_form.find_element_by_name('full_name').send_keys('Swaleh Hassan')
        person_form.find_element_by_name('dob').send_keys('02/01/2019')
        person_form.find_element_by_name('gender').find_elements_by_tag_name('option')[1].click()
        person_form.find_element_by_name('created_by').find_elements_by_tag_name('option')[-1].click()
        self.browser.find_element_by_css_selector('.submit-row input').click()
        self.browser.switch_to.window(self.browser.window_handles[0])

        relationships_inline = self.find_relationships_inline()
        relationship_types = relationships_inline.find_elements_by_css_selector('.field-relationship_type')
        relationship_types[-2].find_elements_by_tag_name('option')[1].click()

        created_by_fields = relationships_inline.find_elements_by_css_selector('.field-created_by')
        created_by_fields[-2].find_elements_by_tag_name('option')[-1].click()
        self.browser.find_elements_by_css_selector('.submit-row input')[0].click()

        # He creates a new family relationship
        # .field-relationship-type .add-related
