from selenium.webdriver.common.by import By

from ..base import BaseComponent


class SubmitFormComponent(BaseComponent):
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


class SearchForm(SubmitFormComponent):
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

    def clear_search_query_input(self):
        self._search_input.clear()

    def enter_search_query(self, query):
        self._search_input.send_keys(query)
