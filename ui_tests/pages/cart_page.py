from selenium.webdriver.common.by import By

from ui_tests.pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM = (By.CSS_SELECTOR, ".cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    ZIP_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    COMPLETE_MESSAGE = (By.CSS_SELECTOR, "[data-test='complete-header']")

    def cart_items_count(self) -> int:
        return self.count(self.CART_ITEM)

    def remove_item(self, product_name: str) -> None:
        button = (By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='cart_item']//button")
        self.click(button)

    def start_checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)

    def fill_checkout_form(self, first_name: str, last_name: str, zip_code: str) -> None:
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.ZIP_CODE, zip_code)
        self.click(self.CONTINUE_BUTTON)

    def finish_checkout(self) -> None:
        self.click(self.FINISH_BUTTON)

    def checkout_success_message(self) -> str:
        return self.text_of(self.COMPLETE_MESSAGE)
