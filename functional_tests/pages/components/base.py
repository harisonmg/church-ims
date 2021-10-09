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
