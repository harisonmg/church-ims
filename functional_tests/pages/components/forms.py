from selenium.webdriver.common.by import By

from .base import BaseComponent


class FormComponent(BaseComponent):
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    @property
    def _submit_button(self):
        return self.browser.find_element(*self.SUBMIT_BUTTON)

    @property
    def submit_button_label(self):
        return self._submit_button.text

    def submit(self):
        self._submit_button.click()
        return self


class SearchForm(FormComponent):
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search']")

    @property
    def _search_input(self):
        return self.browser.find_element(*self.SEARCH_INPUT)

    @property
    def search_input_placeholder(self):
        return self._search_input.get_attribute("placeholder")

    @property
    def search_input_aria_label(self):
        return self._search_input.get_attribute("aria-label")

    def search(self, search_term):
        self._search_input.send_keys(search_term)
        return self.submit()


class LoginForm(FormComponent):
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#id_login")
    EMAIL_LABEL = (By.CSS_SELECTOR, "label[for='id_login']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#id_password")
    PASSWORD_LABEL = (By.CSS_SELECTOR, "label[for='id_password']")
    REMEMBER_CHECKBOX = (By.CSS_SELECTOR, "input#id_remember")
    REMEMBER_CHECKBOX_LABEL = (By.CSS_SELECTOR, "label[for='id_remember']")
    SIGN_UP_LINK = (By.ID, "signup")
    PASSWORD_RESET_LINK = (By.ID, "reset_password")

    @property
    def _email_input(self):
        return self.browser.find_element(*self.EMAIL_INPUT)

    @property
    def email_label(self):
        return self.browser.find_element(*self.EMAIL_LABEL).text

    @property
    def _password_input(self):
        return self.browser.find_element(*self.PASSWORD_INPUT)

    @property
    def password_label(self):
        return self.browser.find_element(*self.PASSWORD_LABEL).text

    @property
    def _remember_checkbox(self):
        return self.browser.find_element(*self.REMEMBER_CHECKBOX)

    @property
    def remember_checkbox_label(self):
        return self.browser.find_element(*self.REMEMBER_CHECKBOX_LABEL).text

    @property
    def signup_link(self):
        element = self.browser.find_element(*self.SIGN_UP_LINK)
        return {element.text: element.get_attribute("href")}

    @property
    def password_reset_link(self):
        element = self.browser.find_element(*self.PASSWORD_RESET_LINK)
        return {element.text: element.get_attribute("href")}

    def send_keys(self, email, password, remember=False):
        self._email_input.send_keys(email)
        self._password_input.send_keys(password)
        if remember:
            self._remember_checkbox.click()
        return self.submit()


class PasswordResetRequestForm(FormComponent):
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#id_email")
    EMAIL_LABEL = (By.CSS_SELECTOR, "label[for='id_email']")

    @property
    def _email_input(self):
        return self.browser.find_element(*self.EMAIL_INPUT)

    @property
    def email_label(self):
        return self.browser.find_element(*self.EMAIL_LABEL).text

    def send_keys(self, email):
        self._email_input.send_keys(email)
        return self.submit()


class PasswordResetForm(FormComponent):
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#id_password1")
    PASSWORD_LABEL = (By.CSS_SELECTOR, "label[for='id_password1']")
    PASSWORD_CONFIRMATION_INPUT = (By.CSS_SELECTOR, "input#id_password2")
    PASSWORD_CONFIRMATION_LABEL = (By.CSS_SELECTOR, "label[for='id_password2']")

    @property
    def _password_input(self):
        return self.browser.find_element(*self.PASSWORD_INPUT)

    @property
    def password_label(self):
        return self.browser.find_element(*self.PASSWORD_LABEL).text

    @property
    def _password_confirmation_input(self):
        return self.browser.find_element(*self.PASSWORD_CONFIRMATION_INPUT)

    @property
    def password_confirmation_label(self):
        return self.browser.find_element(*self.PASSWORD_CONFIRMATION_LABEL).text

    def send_keys(self, password1, password2):
        self._password_input.send_keys(password1)
        self._password_confirmation_input.send_keys(password2)
        return self.submit()


class SignupForm(FormComponent):
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#id_email")
    EMAIL_LABEL = (By.CSS_SELECTOR, "label[for='id_email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#id_password1")
    PASSWORD_LABEL = (By.CSS_SELECTOR, "label[for='id_password1']")
    PASSWORD_CONFIRMATION_INPUT = (By.CSS_SELECTOR, "input#id_password2")
    PASSWORD_CONFIRMATION_LABEL = (By.CSS_SELECTOR, "label[for='id_password2']")
    LOGIN_LINK = (By.ID, "login")

    @property
    def _email_input(self):
        return self.browser.find_element(*self.EMAIL_INPUT)

    @property
    def email_label(self):
        return self.browser.find_element(*self.EMAIL_LABEL).text

    @property
    def _password_input(self):
        return self.browser.find_element(*self.PASSWORD_INPUT)

    @property
    def password_label(self):
        return self.browser.find_element(*self.PASSWORD_LABEL).text

    @property
    def _password_confirmation_input(self):
        return self.browser.find_element(*self.PASSWORD_CONFIRMATION_INPUT)

    @property
    def password_confirmation_label(self):
        return self.browser.find_element(*self.PASSWORD_CONFIRMATION_LABEL).text

    @property
    def login_link(self):
        element = self.browser.find_element(*self.LOGIN_LINK)
        return {element.text: element.get_attribute("href")}

    def send_keys(self, email, password1, password2):
        self._email_input.send_keys(email)
        self._password_input.send_keys(password1)
        self._password_confirmation_input.send_keys(password2)
        return self.submit()


class TemperatureRecordCreationForm(FormComponent):
    BODY_TEMPERATURE_INPUT = (By.CSS_SELECTOR, "input#id_body_temperature")
    BODY_TEMPERATURE_LABEL = (By.CSS_SELECTOR, "label[for='id_body_temperature']")

    @property
    def _body_temperature_input(self):
        return self.browser.find_element(*self.BODY_TEMPERATURE_INPUT)

    @property
    def body_temperature_label(self):
        return self.browser.find_element(*self.BODY_TEMPERATURE_LABEL).text

    def send_keys(self, temperature):
        self._body_temperature_input.send_keys(temperature)
        return self.submit()


class PersonForm(FormComponent):
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

    def select_gender(self, option):
        element = self._gender_options.get(option)
        if element is not None:
            element.click()

    @property
    def _date_of_birth_input(self):
        return self.browser.find_element(*self.DATE_OF_BIRTH_INPUT)

    @property
    def date_of_birth_label(self):
        return self.browser.find_element(*self.DATE_OF_BIRTH_LABEL).text

    def send_keys(self, username=None, full_name=None, gender=None, dob=None):
        if username is not None:
            self._username_input.clear()
            self._username_input.send_keys(username)

        if full_name is not None:
            self._full_name_input.clear()
            self._full_name_input.send_keys(full_name)

        if gender is not None:
            self.select_gender(gender)

        if dob is not None:
            self._date_of_birth_input.clear()
            self._date_of_birth_input.send_keys(dob)
        return self.submit()


class AdultForm(PersonForm):
    PHONE_NUMBER_INPUT = (By.CSS_SELECTOR, "input#id_phone_number")
    PHONE_NUMBER_LABEL = (By.CSS_SELECTOR, "label[for='id_phone_number']")

    @property
    def _phone_number_input(self):
        return self.browser.find_element(*self.PHONE_NUMBER_INPUT)

    @property
    def phone_number_label(self):
        return self.browser.find_element(*self.PHONE_NUMBER_LABEL).text

    def send_keys(
        self, username=None, full_name=None, gender=None, dob=None, phone_number=None
    ):
        if phone_number is not None:
            self._phone_number_input.clear()
            self._phone_number_input.send_keys(phone_number)

        kwargs = dict(username=username, full_name=full_name, gender=gender, dob=dob)
        return super().send_keys(**kwargs)


class ChildForm(PersonForm):
    IS_PARENT_CHECKBOX = (By.CSS_SELECTOR, "input#id_is_parent")
    IS_PARENT_CHECKBOX_LABEL = (By.CSS_SELECTOR, "label[for='id_is_parent']")

    @property
    def _is_parent_checkbox(self):
        return self.browser.find_element(*self.IS_PARENT_CHECKBOX)

    @property
    def is_parent_checkbox_label(self):
        return self.browser.find_element(*self.IS_PARENT_CHECKBOX_LABEL).text

    def send_keys(
        self, username=None, full_name=None, gender=None, dob=None, is_parent=False
    ):
        if is_parent:
            self._is_parent_checkbox.click()
        kwargs = dict(username=username, full_name=full_name, gender=gender, dob=dob)
        return super().send_keys(**kwargs)


class InterpersonalRelationshipCreationForm(FormComponent):
    PERSON_USERNAME_INPUT = (By.CSS_SELECTOR, "input#id_person")
    PERSON_USERNAME_LABEL = (By.CSS_SELECTOR, "label[for='id_person']")
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

    def select_relationship_type(self, option):
        element = self._relationship_type_options.get(option)
        if element is not None:
            element.click()

    def send_keys(self, person_username, relative_username, relationship_type):
        self._person_username_input.send_keys(person_username)
        self._relative_username_input.send_keys(relative_username)
        self.select_relationship_type(relationship_type)
        return self.submit()
