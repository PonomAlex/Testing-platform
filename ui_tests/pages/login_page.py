from selenium.webdriver.common.by import By

from ui_tests.pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    PRODUCTS_TITLE = (By.CSS_SELECTOR, "[data-test='title']")

    def login(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def get_error(self) -> str:
        return self.text_of(self.ERROR_MESSAGE)

    def is_logged_in(self) -> bool:
        return self.is_visible(self.PRODUCTS_TITLE)
