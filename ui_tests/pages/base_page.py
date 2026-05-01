from typing import Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


Locator = Tuple[str, str]


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def wait_visible(self, locator: Locator):
        return self.wait.until(ec.visibility_of_element_located(locator))

    def wait_clickable(self, locator: Locator):
        return self.wait.until(ec.element_to_be_clickable(locator))

    def click(self, locator: Locator) -> None:
        self.wait_clickable(locator).click()

    def click_via_js(self, locator: Locator) -> None:
        element = self.wait_clickable(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator: Locator, text: str) -> None:
        element = self.wait_visible(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator: Locator) -> str:
        return self.wait_visible(locator).text.strip()

    def count(self, locator: Locator) -> int:
        # Count should support "0 elements" state (for remove-from-cart checks).
        return len(self.driver.find_elements(*locator))

    def is_visible(self, locator: Locator) -> bool:
        try:
            self.wait_visible(locator)
            return True
        except Exception:
            return False
