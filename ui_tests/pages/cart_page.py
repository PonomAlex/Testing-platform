from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

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
        for _ in range(2):
            self.click_via_js(button)
            try:
                WebDriverWait(self.driver, 3).until(lambda _driver: self.cart_items_count() == 0)
                return
            except Exception:
                pass
        self.wait.until(lambda _driver: self.cart_items_count() == 0)

    def start_checkout(self) -> None:
        self.click_via_js(self.CHECKOUT_BUTTON)
        self.wait.until(ec.url_contains("checkout-step-one.html"))
        self.wait_visible(self.FIRST_NAME)

    def fill_checkout_form(self, first_name: str, last_name: str, zip_code: str) -> None:
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.ZIP_CODE, zip_code)
        # Force values in remote-grid mode where key events can be flaky.
        self.driver.execute_script(
            """
            document.getElementById('first-name').value = arguments[0];
            document.getElementById('last-name').value = arguments[1];
            document.getElementById('postal-code').value = arguments[2];
            """,
            first_name,
            last_name,
            zip_code,
        )
        self.click_via_js(self.CONTINUE_BUTTON)
        try:
            WebDriverWait(self.driver, 3).until(ec.visibility_of_element_located(self.FINISH_BUTTON))
        except Exception:
            self.click(self.CONTINUE_BUTTON)
        self.wait_visible(self.FINISH_BUTTON)

    def finish_checkout(self) -> None:
        self.click_via_js(self.FINISH_BUTTON)
        self.wait.until(ec.url_contains("checkout-complete.html"))
        self.wait_visible(self.COMPLETE_MESSAGE)

    def checkout_success_message(self) -> str:
        return self.text_of(self.COMPLETE_MESSAGE)
