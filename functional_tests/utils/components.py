from selenium.webdriver.common.by import By


class BaseComponent:
    def __init__(self, browser):
        self.browser = browser


# generic page components
class Messages(BaseComponent):
    ALERT = (By.CSS_SELECTOR, "div[role='alert']")

    @property
    def _alerts(self):
        return self.browser.find_elements(*self.ALERT)

    @property
    def messages(self):
        return [msg.text for msg in self._alerts]


# navigation
class NavigationComponent(BaseComponent):
    CONTAINER = (By.TAG_NAME, "main")
    LINK = (By.TAG_NAME, "a")

    @property
    def _container(self):
        return self.browser.find_element(*self.CONTAINER)

    @property
    def _link_elements(self):
        elements = self._container.find_elements(*self.LINK)
        text = map(lambda a: a.text, elements)
        return dict(zip(text, elements))

    @property
    def links(self):
        hrefs = map(lambda a: a.get_attribute("href"), self._link_elements.values())
        return dict(zip(self._link_elements.keys(), hrefs))

    def go_to_page(self, link_text):
        page_link = self._link_elements.get(link_text)
        if page_link is not None:
            page_link.click()


class AccountDropdownMenu(NavigationComponent):
    CONTAINER = (By.CSS_SELECTOR, "[aria-labelledby='accountDropdownMenu']")


class Header(BaseComponent):
    ACCOUNT_DROPDOWN_TOGGLE = (By.ID, "accountDropdownMenu")
    SIDEBAR_TOGGLE = (By.CSS_SELECTOR, "button[data-bs-target='#sidebarMenu']")
    TITLE = (By.CSS_SELECTOR, "#site_header > a")

    def toggle_account_dropdown(self):
        toggle_link = self.browser.find_element(*self.ACCOUNT_DROPDOWN_TOGGLE)
        return toggle_link.click()

    def toggle_sidebar(self):
        toggle_link = self.browser.find_element(*self.SIDEBAR_TOGGLE)
        return toggle_link.click()

    @property
    def account_dropdown(self):
        return AccountDropdownMenu(self.browser)

    @property
    def title(self):
        link = self.browser.find_element(*self.TITLE)
        return {link.text: link.get_attribute("href")}


class Footer(NavigationComponent):
    CONTAINER = (By.ID, "site_footer")

    @property
    def text(self):
        return self._container.text


class Pagination(NavigationComponent):
    CONTAINER = (By.CSS_SELECTOR, "nav .pagination")
    PAGE_ITEM = (By.CLASS_NAME, "page-item")

    @property
    def _link_classes(self):
        page_items = self._container.find_elements(*self.PAGE_ITEM)
        link_classes = map(lambda el: el.get_attribute("class"), page_items)
        return dict(zip(self.links.keys(), list(link_classes)))

    @property
    def active_links(self):
        active = {}
        for link, classes in self._link_classes.items():
            if "active" in classes:
                active[link] = self.links[link]
        return active

    @property
    def disabled_links(self):
        disabled = []
        for link, classes in self._link_classes.items():
            if "disabled" in classes:
                disabled.append(link)
        return disabled


class Sidebar(NavigationComponent):
    CONTAINER = (By.ID, "sidebarMenu")

    @property
    def active_links(self):
        active = {}
        for link, element in self._link_elements.items():
            if "active" in element.get_attribute("class"):
                active[link] = self.links[link]
        return active


# tables
class Table(BaseComponent):
    COLUMN = (By.CSS_SELECTOR, "thead th[scope='col']")
    ROW_HEADER = (By.CSS_SELECTOR, "tbody th[scope='row']")
    ROW = (By.CSS_SELECTOR, "tbody tr")
    DATA = (By.TAG_NAME, "td")

    @property
    def columns(self):
        elements = self.browser.find_elements(*self.COLUMN)
        return list(map(lambda el: el.text, elements))

    @property
    def _row_headers(self):
        return self.browser.find_elements(*self.ROW_HEADER)

    @property
    def _row_data(self):
        """Returns table data elements for each row in a list of lists"""
        rows = self.browser.find_elements(*self.ROW)
        return map(lambda row: row.find_elements(*self.DATA), rows)

    @property
    def data(self):
        """Returns a dictionary with row headers as keys and lists
        containing row data as values
        """
        row_headers = map(lambda el: el.text, self._row_headers)
        row_data = []
        for row in self._row_data:
            row_data.append(list(map(lambda el: el.text, row)))
        return dict(zip(row_headers, row_data))


# forms
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
