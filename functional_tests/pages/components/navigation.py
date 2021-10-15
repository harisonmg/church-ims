from selenium.webdriver.common.by import By

from .base import BaseComponent


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
        for name, classes in self._link_classes.items():
            if "active" in classes:
                active[name] = self.links[name]
        return active

    @property
    def disabled_links(self):
        disabled = []
        for name, classes in self._link_classes.items():
            if "disabled" in classes:
                disabled.append(name)
        return disabled


class Sidebar(NavigationComponent):
    CONTAINER = (By.ID, "sidebarMenu")

    @property
    def active_links(self):
        active = {}
        for name, element in self._link_elements.items():
            if "active" in element.get_attribute("class"):
                active[name] = self.links[name]
        return active
