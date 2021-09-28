from selenium.webdriver.common.by import By


class BaseComponent:
    def __init__(self, browser):
        self.browser = browser


# generic page components
class Header(BaseComponent):
    ACCOUNT_DROPDOWN_TOGGLE = (By.ID, "accountDropdownMenu")
    ACCOUNT_DROPDOWN = (By.CSS_SELECTOR, "[aria-labelledby='accountDropdownMenu']")
    DROPDOWN_LINKS = (By.CSS_SELECTOR, "a.dropdown-item")
    HOME_PAGE_LINK = (By.CSS_SELECTOR, "#site_header > a")
    SIDEBAR_TOGGLE = (By.CSS_SELECTOR, "button[data-bs-target='#sidebarMenu']")

    @property
    def _account_dropdown_toggle(self):
        return self.browser.find_element(*self.ACCOUNT_DROPDOWN_TOGGLE)

    @property
    def _account_dropdown(self):
        return self.browser.find_element(*self.ACCOUNT_DROPDOWN)

    @property
    def _account_dropdown_links(self):
        return self.account_dropdown.find_elements(*self.DROPDOWN_LINKS)

    @property
    def _home_page_link(self):
        return self.browser.find_element(*self.HOME_PAGE_LINK)

    @property
    def _sidebar_toggle(self):
        return self.browser.find_element(*self.SIDEBAR_TOGGLE)

    @property
    def title(self):
        return self._home_page_link.text


class Messages(BaseComponent):
    ALERT = (By.CSS_SELECTOR, "div[role='alert']")

    @property
    def _alerts(self):
        return self.browser.find_elements(*self.ALERT)

    @property
    def messages(self):
        return [msg.text for msg in self._alerts]


class Sidebar(BaseComponent):
    SIDEBAR_LINK = (By.CSS_SELECTOR, "#sidebarMenu a")

    @property
    def _links(self):
        return self.browser.find_elements(*self.SIDEBAR_LINK)


class Pagination(BaseComponent):
    PAGE_ITEM = (By.CLASS_NAME, "page-item")
    PAGE_LINK = (By.CLASS_NAME, "page-link")

    @property
    def _items(self):
        return self.browser.find_elements(*self.PAGE_ITEM)

    @property
    def _links(self):
        return self.browser.find_elements(*self.PAGE_LINK)


class Footer(BaseComponent):
    FOOTER = (By.ID, "site_footer")
    FOOTER_LINK = (By.CSS_SELECTOR, "#site_footer a")

    @property
    def _text(self):
        return self.browser.find_element(*self.FOOTER).text

    @property
    def _links(self):
        return self.browser.find_elements(*self.FOOTER_LINK)


# forms
class BaseForm(BaseComponent):
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


class GenericSearchForm(BaseForm):
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search']")

    @property
    def _search_input(self):
        return self.browser.find_element(*self.SEARCH_INPUT)

    def search(self, search_term):
        self._search_input.send_keys(search_term)
        return self.submit()


class LoginForm(BaseForm):
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#id_login")
    EMAIL_LABEL = (By.CSS_SELECTOR, "label[for='id_login']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#id_password")
    PASSWORD_LABEL = (By.CSS_SELECTOR, "label[for='id_password']")
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
    def signup_link(self):
        link_element = self.browser.find_element(*self.SIGN_UP_LINK)
        return link_element.get_attribute("href")

    @property
    def password_reset_link(self):
        link_element = self.browser.find_element(*self.PASSWORD_RESET_LINK)
        return link_element.get_attribute("href")

    def send_keys(self, email, password):
        self._email_input.send_keys(email)
        self._password_input.send_keys(password)
        return self.submit()


class PasswordResetRequestForm(BaseForm):
    pass


class PasswordResetForm(BaseForm):
    pass


class SignupForm(BaseForm):
    pass
