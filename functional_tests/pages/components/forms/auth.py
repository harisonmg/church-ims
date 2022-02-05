from selenium.webdriver.common.by import By

from .generic import SubmitFormComponent


class LoginForm(SubmitFormComponent):
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


class PasswordResetRequestForm(SubmitFormComponent):
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


class PasswordResetForm(SubmitFormComponent):
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


class SignupForm(SubmitFormComponent):
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