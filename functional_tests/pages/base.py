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
        return components.Messages(self.browser).messages

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
