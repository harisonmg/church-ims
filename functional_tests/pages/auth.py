from selenium.webdriver.common.by import By

from . import components
from .base import BasePage


class LoginPage(BasePage):
    PATH = "/accounts/login/"

    @property
    def form(self):
        return components.LoginForm(self.browser)


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
