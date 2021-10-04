from selenium.webdriver.common.by import By

from . import components


class BasePage:
    PATH = "/404/"
    HEADING = (By.TAG_NAME, "h1")
    MAIN_PARAGRAPHS = (By.CSS_SELECTOR, "main p")

    def __init__(self, test):
        self.test = test

    @property
    def browser(self):
        return self.test.browser

    @property
    def url(self):
        return self.test.live_server_url + self.PATH

    @property
    def title(self):
        return self.browser.title

    @property
    def heading(self):
        return self.browser.find_element(*self.HEADING).text

    @property
    def header(self):
        return components.Header(self.browser)

    @property
    def _main_paragraphs(self):
        return self.browser.find_elements(*self.MAIN_PARAGRAPHS)

    @property
    def main_text(self):
        return list(map(lambda p: p.text, self._main_paragraphs))

    @property
    def messages(self):
        return components.Messages(self.browser)

    @property
    def sidebar(self):
        return components.Sidebar(self.browser)

    @property
    def pagination(self):
        return components.Pagination(self.browser)

    @property
    def footer(self):
        return components.Footer(self.browser)

    def visit(self):
        self.browser.get(self.url)
        return self


class HomePage(BasePage):
    PATH = "/"
    PRIMARY_CTA = (By.CSS_SELECTOR, "a#primary")
    SECONDARY_CTA = (By.CSS_SELECTOR, "a#secondary")

    @property
    def _primary_cta(self):
        return self.browser.find_element(*self.PRIMARY_CTA)

    @property
    def _secondary_cta(self):
        return self.browser.find_element(*self.SECONDARY_CTA)

    @property
    def primary_cta_link(self):
        return self._primary_cta.get_attribute("href")

    @property
    def secondary_cta_link(self):
        return self._secondary_cta.get_attribute("href")


# authentication-related pages
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
        return components.FormComponent(self.browser)

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
    PATH = "/accounts/password/reset/key/invalid-token/"

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
    PATH = "/accounts/confirm-email/invalid-token/"

    @property
    def form(self):
        return components.FormComponent(self.browser)

    def confirm_email(self):
        self.form.submit()
        return self


# application-related pages
class Dashboard(BasePage):
    PATH = "/dashboard/"


class PeopleListPage(BasePage):
    PATH = "/people/"

    @property
    def form(self):
        return components.SearchForm(self.browser)

    @property
    def table(self):
        return components.Table(self.browser)

    def search(self, search_term):
        self.form.search(search_term=search_term)
        return self


class TemperatureRecordsListPage(BasePage):
    PATH = "/records/temperature/"

    @property
    def table(self):
        return components.Table(self.browser)
