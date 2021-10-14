from selenium.webdriver.common.by import By

from .base import BaseComponent


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
        return list(map(lambda row: row.find_elements(*self.DATA), rows))

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

    def get_column_index(self, column):
        return self.columns.index(column) - 1

    def get_column_data(self, column):
        col_index = self.get_column_index(column)
        return {row: data[col_index] for row, data in self.data.items()}

    def get_cell_data(self, row, column):
        row_data = self.data.get(row)
        return row_data[self.get_column_index(column)]


class PeopleTable(Table):
    ADD_TEMP_LINK = (By.CSS_SELECTOR, "td a.btn")

    @property
    def _add_temp_elements(self):
        elements = self.browser.find_elements(*self.ADD_TEMP_LINK)
        usernames = self.get_column_data("Username").values()
        return dict(zip(usernames, elements))

    @property
    def add_temp_links(self):
        hrefs = map(lambda a: a.get_attribute("href"), self._add_temp_elements.values())
        return dict(zip(self._add_temp_elements.keys(), hrefs))

    def add_temperature_for_person(self, username):
        link = self._add_temp_elements.get(username)
        if link is not None:
            link.click()
