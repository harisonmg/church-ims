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
    SIGN_UP_LINK = (By.LINK_TEXT, "Sign up")
    PASSWORD_RESET_LINK = (By.LINK_TEXT, "I don't remember my password")

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
        link_element = self.browser.find_element(*self.SIGN_UP_LINK)
        return link_element.get_attribute("href")

    @property
    def password_reset_link(self):
        link_element = self.browser.find_element(*self.PASSWORD_RESET_LINK)
        return link_element.get_attribute("href")

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
    LOGIN_LINK = (By.LINK_TEXT, "Log in")

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
        link_element = self.browser.find_element(*self.LOGIN_LINK)
        return link_element.get_attribute("href")

    def send_keys(self, email, password1, password2):
        self._email_input.send_keys(email)
        self._password_input.send_keys(password1)
        self._password_confirmation_input.send_keys(password2)
        return self.submit()


class TemperatureRecordForm(FormComponent):
    BODY_TEMPERATURE_INPUT = (By.CSS_SELECTOR, "input#id_body_temperature")
    BODY_TEMPERATURE_LABEL = (By.CSS_SELECTOR, "label[for='id_body_temperature']")

    @property
    def _body_temperature_input(self):
        return self.browser.find_element(*self.BODY_TEMPERATURE_INPUT)

    @property
    def body_temperature_label(self):
        return self.browser.find_element(*self.BODY_TEMPERATURE_LABEL).text

    def send_keys(self, temperature):
        self._body_temperature_input.send_keys(str(temperature))
        return self.submit()


class PersonForm(FormComponent):
    USERNAME_INPUT = (By.CSS_SELECTOR, "input#id_username")
    USERNAME_LABEL = (By.CSS_SELECTOR, "label[for='id_username']")
    FULL_NAME_INPUT = (By.CSS_SELECTOR, "input#id_full_name")
    FULL_NAME_LABEL = (By.CSS_SELECTOR, "label[for='id_full_name']")

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

    def send_keys(self, username=None, full_name=None):
        if username is not None:
            self._username_input.clear()
            self._username_input.send_keys(username)

        if full_name is not None:
            self._full_name_input.clear()
            self._full_name_input.send_keys(full_name)
        return self.submit()
