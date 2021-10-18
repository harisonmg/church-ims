from selenium.webdriver.common.by import By

from . import components
from .base import BasePage


class HomePage(BasePage):
    PATH = "/"
    SIGN_UP_LINK = (By.ID, "signup")
    LOGIN_LINK = (By.ID, "login")

    @property
    def signup_link(self):
        element = self.browser.find_element(*self.SIGN_UP_LINK)
        return {element.text: element.get_attribute("href")}

    @property
    def login_link(self):
        element = self.browser.find_element(*self.LOGIN_LINK)
        return {element.text: element.get_attribute("href")}


class Dashboard(BasePage):
    PATH = "/dashboard/"


class PeopleListPage(BasePage):
    PATH = "/people/"

    @property
    def form(self):
        return components.SearchForm(self.browser)

    @property
    def table(self):
        return components.PeopleTable(self.browser)

    def search(self, search_term):
        self.form.search(search_term=search_term)
        return self


class TemperatureRecordsListPage(BasePage):
    PATH = "/records/temperature/"

    @property
    def form(self):
        return components.SearchForm(self.browser)

    @property
    def table(self):
        return components.Table(self.browser)

    def search(self, search_term):
        self.form.search(search_term=search_term)
        return self


class TemperatureRecordCreationPage(BasePage):
    def __init__(self, test, person_username):
        super().__init__(test)
        self.person_username = person_username

    @property
    def PATH(self):
        return f"/records/temperature/{self.person_username}/add/"

    @property
    def form(self):
        return components.TemperatureRecordCreationForm(self.browser)

    def add_temperature(self, temperature):
        self.form.send_keys(temperature=temperature)
        return self


class PersonCreationPage(BasePage):
    PATH = "/people/add/"

    @property
    def form(self):
        return components.PersonForm(self.browser)

    def add_person(self, username, full_name, gender, dob):
        self.form.send_keys(
            username=username, full_name=full_name, gender=gender, dob=dob
        )
        return self


class AdultCreationPage(PersonCreationPage):
    PATH = "/people/add/adult/"


class PersonDetailPage(BasePage):
    UPDATE_LINK = (By.ID, "update")

    def __init__(self, test, person_username):
        super().__init__(test)
        self.person_username = person_username

    @property
    def PATH(self):
        return f"/people/{self.person_username}/"

    @property
    def _update_link_element(self):
        return self.browser.find_element(*self.UPDATE_LINK)

    @property
    def update_link(self):
        element = self._update_link_element
        return {element.text: element.get_attribute("href")}

    def update_person(self):
        self._update_link_element.click()


class PersonUpdatePage(BasePage):
    def __init__(self, test, person_username):
        super().__init__(test)
        self.person_username = person_username

    @property
    def PATH(self):
        return f"/people/{self.person_username}/update/"

    @property
    def form(self):
        return components.PersonForm(self.browser)

    def update_person(self, username=None, full_name=None, gender=None, dob=None):
        self.form.send_keys(
            username=username, full_name=full_name, gender=gender, dob=dob
        )
        return self


class InterpersonalRelationshipsListPage(BasePage):
    PATH = "/people/relationships/"

    @property
    def form(self):
        return components.SearchForm(self.browser)

    @property
    def table(self):
        return components.Table(self.browser)

    def search(self, search_term):
        self.form.search(search_term=search_term)
        return self


class InterpersonalRelationshipCreationPage(BasePage):
    PATH = "/people/relationships/add/"

    @property
    def form(self):
        return components.InterpersonalRelationshipCreationForm(self.browser)

    def add_relationship(self, person_username, relative_username, relationship_type):
        self.form.send_keys(
            person_username=person_username,
            relative_username=relative_username,
            relationship_type=relationship_type,
        )
        return self
