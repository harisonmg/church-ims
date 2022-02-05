from selenium.webdriver.common.by import By

from . import components
from .base import BasePage


class LoginPage(BasePage):
    PATH = "/accounts/login/"

    @property
    def form(self):
        return components.LoginForm(self.browser)

    def login(self, email, password, remember=False):
        self.form.send_keys(email=email, password=password, remember=remember)
        return self


class LogoutPage(BasePage):
    PATH = "/accounts/logout/"

    @property
    def form(self):
        return components.SubmitFormComponent(self.browser)

    def logout(self):
        self.form.submit()
        return self


class AccountInactivePage(BasePage):
    PATH = "/accounts/inactive/"


class PasswordResetRequestPage(BasePage):
    PATH = "/accounts/password/reset/"

    @property
    def form(self):
        return components.PasswordResetRequestForm(self.browser)

    def request_password_reset(self, email):
        self.form.send_keys(email=email)
        return self


class PasswordResetRequestDonePage(BasePage):
    PATH = "/accounts/password/reset/done/"


class PasswordResetPage(BasePage):
    def __init__(self, test, token="invalid-token"):
        super().__init__(test)
        self.token = token

    @property
    def PATH(self):
        return f"/accounts/password/reset/key/{self.token}/"

    @property
    def form(self):
        return components.PasswordResetForm(self.browser)

    def set_password(self, password1, password2):
        self.form.send_keys(password1=password1, password2=password2)
        return self


class PasswordResetDonePage(BasePage):
    PATH = "/accounts/password/reset/key/done/"
    LOGIN_LINK = (By.LINK_TEXT, "log in")

    @property
    def login_link(self):
        link_element = self.browser.find_element(*self.LOGIN_LINK)
        return link_element.get_attribute("href")


class SignupPage(BasePage):
    PATH = "/accounts/signup/"

    @property
    def form(self):
        return components.SignupForm(self.browser)

    def signup(self, email, password1, password2):
        self.form.send_keys(email=email, password1=password1, password2=password2)
        return self


class EmailVerificationRequiredPage(BasePage):
    PATH = "/accounts/confirm-email/"


class EmailConfirmationPage(BasePage):
    def __init__(self, test, token="invalid-token"):
        super().__init__(test)
        self.token = token

    @property
    def PATH(self):
        return f"/accounts/confirm-email/{self.token}/"

    @property
    def form(self):
        return components.SubmitFormComponent(self.browser)

    def confirm_email(self):
        self.form.submit()
        return self
