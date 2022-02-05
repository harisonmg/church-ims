from selenium.webdriver.common.by import By

from ..base import BaseComponent
from .generic import SubmitFormComponent


# generic components
class EmailComponent(BaseComponent):
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#id_email")
    EMAIL_LABEL = (By.CSS_SELECTOR, "label[for='id_email']")

    @property
    def _email_input(self):
        return self.browser.find_element(*self.EMAIL_INPUT)

    @property
    def email_label(self):
        return self.browser.find_element(*self.EMAIL_LABEL).text

    def clear_email_input(self):
        self._email_input.clear()

    def enter_email(self, email):
        self._email_input.send_keys(email)


class UsernameOrEmailComponent(EmailComponent):
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#id_login")
    EMAIL_LABEL = (By.CSS_SELECTOR, "label[for='id_login']")


class PasswordComponent(BaseComponent):
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#id_password")
    PASSWORD_LABEL = (By.CSS_SELECTOR, "label[for='id_password']")

    @property
    def _password_input(self):
        return self.browser.find_element(*self.PASSWORD_INPUT)

    @property
    def password_label(self):
        return self.browser.find_element(*self.PASSWORD_LABEL).text

    def clear_password_input(self):
        self._password_input.clear()

    def enter_password(self, password):
        self._password_input.send_keys(password)


class PasswordConfirmationComponent(PasswordComponent):
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#id_password1")
    PASSWORD_LABEL = (By.CSS_SELECTOR, "label[for='id_password1']")
    PASSWORD_CONFIRMATION_INPUT = (By.CSS_SELECTOR, "input#id_password2")
    PASSWORD_CONFIRMATION_LABEL = (By.CSS_SELECTOR, "label[for='id_password2']")

    @property
    def _password_confirmation_input(self):
        return self.browser.find_element(*self.PASSWORD_CONFIRMATION_INPUT)

    @property
    def password_confirmation_label(self):
        return self.browser.find_element(*self.PASSWORD_CONFIRMATION_LABEL).text

    def clear_password2_input(self):
        self._password_confirmation_input.clear()

    def enter_password2(self, password):
        self._password_confirmation_input.send_keys(password)


# forms
class LoginForm(UsernameOrEmailComponent, PasswordComponent, SubmitFormComponent):
    REMEMBER_CHECKBOX = (By.CSS_SELECTOR, "input#id_remember")
    REMEMBER_CHECKBOX_LABEL = (By.CSS_SELECTOR, "label[for='id_remember']")
    SIGN_UP_LINK = (By.ID, "signup")
    PASSWORD_RESET_LINK = (By.ID, "reset_password")

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

    def click_remember_checkbox(self):
        self._remember_checkbox.click()


class PasswordResetRequestForm(EmailComponent, SubmitFormComponent):
    pass


class PasswordResetForm(PasswordConfirmationComponent, SubmitFormComponent):
    pass


class SignupForm(EmailComponent, PasswordConfirmationComponent, SubmitFormComponent):
    LOGIN_LINK = (By.ID, "login")

    @property
    def login_link(self):
        element = self.browser.find_element(*self.LOGIN_LINK)
        return {element.text: element.get_attribute("href")}
