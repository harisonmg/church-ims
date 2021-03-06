from selenium.webdriver.common.by import By

from .base import BasePage
from .components.forms.features import (
    AdultForm,
    ChildForm,
    InterpersonalRelationshipCreationForm,
    ParentChildRelationshipCreationForm,
    PersonForm,
    TemperatureRecordCreationForm,
)
from .components.forms.generic import SearchForm
from .components.tables import PeopleTable, Table


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
        return SearchForm(self.browser)

    @property
    def table(self):
        return PeopleTable(self.browser)


class TemperatureRecordsListPage(BasePage):
    PATH = "/records/temperature/"

    @property
    def form(self):
        return SearchForm(self.browser)

    @property
    def table(self):
        return Table(self.browser)


class TemperatureRecordCreationPage(BasePage):
    def __init__(self, test, person_username):
        super().__init__(test)
        self.person_username = person_username

    @property
    def PATH(self):
        return f"/records/temperature/{self.person_username}/add/"

    @property
    def form(self):
        return TemperatureRecordCreationForm(self.browser)


class PersonCreationPage(BasePage):
    PATH = "/people/add/"

    @property
    def form(self):
        return PersonForm(self.browser)


class AdultCreationPage(PersonCreationPage):
    PATH = "/people/add/adult/"

    @property
    def form(self):
        return AdultForm(self.browser)


class AdultSelfRegistrationPage(AdultCreationPage):
    PATH = "/people/register/self/"


class ChildCreationPage(PersonCreationPage):
    PATH = "/people/add/child/"

    @property
    def form(self):
        return ChildForm(self.browser)


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

    def update_personal_info(self):
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
        return PersonForm(self.browser)


class InterpersonalRelationshipsListPage(BasePage):
    PATH = "/people/relationships/"

    @property
    def form(self):
        return SearchForm(self.browser)

    @property
    def table(self):
        return Table(self.browser)


class InterpersonalRelationshipCreationPage(BasePage):
    PATH = "/people/relationships/add/"

    @property
    def form(self):
        return InterpersonalRelationshipCreationForm(self.browser)


class ParentChildRelationshipCreationPage(BasePage):
    def __init__(self, test, child_username):
        super().__init__(test)
        self.child_username = child_username

    @property
    def PATH(self):
        return f"/people/relationships/add/{self.child_username}/parent/"

    @property
    def form(self):
        return ParentChildRelationshipCreationForm(self.browser)
