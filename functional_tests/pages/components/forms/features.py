from selenium.webdriver.common.by import By

from .generic import SubmitFormComponent


# people
class PersonForm(SubmitFormComponent):
    USERNAME_INPUT = (By.CSS_SELECTOR, "input#id_username")
    USERNAME_LABEL = (By.CSS_SELECTOR, "label[for='id_username']")
    FULL_NAME_INPUT = (By.CSS_SELECTOR, "input#id_full_name")
    FULL_NAME_LABEL = (By.CSS_SELECTOR, "label[for='id_full_name']")
    GENDER_OPTION = (By.CSS_SELECTOR, "select#id_gender option")
    GENDER_LABEL = (By.CSS_SELECTOR, "label[for='id_gender']")
    DATE_OF_BIRTH_INPUT = (By.CSS_SELECTOR, "input#id_dob")
    DATE_OF_BIRTH_LABEL = (By.CSS_SELECTOR, "label[for='id_dob']")

    @property
    def _username_input(self):
        return self.browser.find_element(*self.USERNAME_INPUT)

    @property
    def username_label(self):
        return self.browser.find_element(*self.USERNAME_LABEL).text

    @property
    def _full_name_input(self):
        return self.browser.find_element(*self.FULL_NAME_INPUT)

    @property
    def full_name_label(self):
        return self.browser.find_element(*self.FULL_NAME_LABEL).text

    @property
    def gender_label(self):
        return self.browser.find_element(*self.GENDER_LABEL).text

    @property
    def _gender_options(self):
        elements = self.browser.find_elements(*self.GENDER_OPTION)
        options = map(lambda el: el.text, elements)
        return dict(zip(options, elements))

    @property
    def gender_options(self):
        return list(self._gender_options.keys())

    @property
    def _date_of_birth_input(self):
        return self.browser.find_element(*self.DATE_OF_BIRTH_INPUT)

    @property
    def date_of_birth_label(self):
        return self.browser.find_element(*self.DATE_OF_BIRTH_LABEL).text

    def clear_username_input(self):
        self._username_input.clear()

    def enter_username(self, username):
        self._username_input.send_keys(username)

    def clear_full_name_input(self):
        self._full_name_input.clear()

    def enter_full_name(self, full_name):
        self._full_name_input.send_keys(full_name)

    def select_gender(self, option):
        element = self._gender_options.get(option)
        if element is not None:
            element.click()

    def clear_dob_input(self):
        self._date_of_birth_input.clear()

    def enter_dob(self, dob):
        self._date_of_birth_input.send_keys(dob)


class AdultForm(PersonForm):
    PHONE_NUMBER_INPUT = (By.CSS_SELECTOR, "input#id_phone_number")
    PHONE_NUMBER_LABEL = (By.CSS_SELECTOR, "label[for='id_phone_number']")

    @property
    def _phone_number_input(self):
        return self.browser.find_element(*self.PHONE_NUMBER_INPUT)

    @property
    def phone_number_label(self):
        return self.browser.find_element(*self.PHONE_NUMBER_LABEL).text

    def clear_phone_number_input(self):
        self._phone_number_input.clear()

    def enter_phone_number(self, phone_number):
        self._phone_number_input.send_keys(phone_number)


class ChildForm(PersonForm):
    IS_PARENT_CHECKBOX = (By.CSS_SELECTOR, "input#id_is_parent")
    IS_PARENT_CHECKBOX_LABEL = (By.CSS_SELECTOR, "label[for='id_is_parent']")

    @property
    def _is_parent_checkbox(self):
        return self.browser.find_element(*self.IS_PARENT_CHECKBOX)

    @property
    def is_parent_checkbox_label(self):
        return self.browser.find_element(*self.IS_PARENT_CHECKBOX_LABEL).text

    def click_is_parent_checkbox(self):
        self._is_parent_checkbox.click()


class PersonUsernameComponent:
    PERSON_USERNAME_INPUT = (By.CSS_SELECTOR, "input#id_person")
    PERSON_USERNAME_LABEL = (By.CSS_SELECTOR, "label[for='id_person']")


class InterpersonalRelationshipCreationForm(
    PersonUsernameComponent, SubmitFormComponent
):
    RELATIVE_USERNAME_INPUT = (By.CSS_SELECTOR, "input#id_relative")
    RELATIVE_USERNAME_LABEL = (By.CSS_SELECTOR, "label[for='id_relative']")
    RELATIONSHIP_TYPE_OPTION = (By.CSS_SELECTOR, "select#id_relation option")
    RELATIONSHIP_TYPE_LABEL = (By.CSS_SELECTOR, "label[for='id_relation']")

    @property
    def _person_username_input(self):
        return self.browser.find_element(*self.PERSON_USERNAME_INPUT)

    @property
    def person_username_label(self):
        return self.browser.find_element(*self.PERSON_USERNAME_LABEL).text

    @property
    def _relative_username_input(self):
        return self.browser.find_element(*self.RELATIVE_USERNAME_INPUT)

    @property
    def relative_username_label(self):
        return self.browser.find_element(*self.RELATIVE_USERNAME_LABEL).text

    @property
    def relationship_type_label(self):
        return self.browser.find_element(*self.RELATIONSHIP_TYPE_LABEL).text

    @property
    def _relationship_type_options(self):
        elements = self.browser.find_elements(*self.RELATIONSHIP_TYPE_OPTION)
        options = map(lambda el: el.text, elements)
        return dict(zip(options, elements))

    @property
    def relationship_type_options(self):
        return list(self._relationship_type_options.keys())

    def clear_person_username_input(self):
        self._person_username_input.clear()

    def enter_person_username(self, username):
        self._person_username_input.send_keys(username)

    def clear_relative_username_input(self):
        self._relative_username_input.clear()

    def enter_relative_username(self, username):
        self._relative_username_input.send_keys(username)

    def select_relationship_type(self, option):
        element = self._relationship_type_options.get(option)
        if element is not None:
            element.click()


class ParentChildRelationshipCreationForm(PersonUsernameComponent, SubmitFormComponent):
    @property
    def _parent_username_input(self):
        return self.browser.find_element(*self.PERSON_USERNAME_INPUT)

    @property
    def parent_username_label(self):
        return self.browser.find_element(*self.PERSON_USERNAME_LABEL).text

    def clear_parent_username_input(self):
        self._parent_username_input.clear()

    def enter_parent_username(self, username):
        self._parent_username_input.send_keys(username)


# records
class TemperatureRecordCreationForm(SubmitFormComponent):
    BODY_TEMPERATURE_INPUT = (By.CSS_SELECTOR, "input#id_body_temperature")
    BODY_TEMPERATURE_LABEL = (By.CSS_SELECTOR, "label[for='id_body_temperature']")

    @property
    def _body_temperature_input(self):
        return self.browser.find_element(*self.BODY_TEMPERATURE_INPUT)

    @property
    def body_temperature_label(self):
        return self.browser.find_element(*self.BODY_TEMPERATURE_LABEL).text

    def clear_body_temperature_input(self):
        self._body_temperature_input.clear()

    def enter_body_temperature(self, body_temperature):
        self._body_temperature_input.send_keys(body_temperature)
