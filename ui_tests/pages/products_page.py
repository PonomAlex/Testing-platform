from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from ui_tests.pages.base_page import BasePage


class ProductsPage(BasePage):
    PAGE_TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    INVENTORY_ITEM = (By.CSS_SELECTOR, ".inventory_item")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def _wait_for_cart_count(self, expected_count: int) -> None:
        def condition(_driver):
            badges = self.driver.find_elements(*self.CART_BADGE)
            if expected_count == 0:
                return len(badges) == 0
            return len(badges) == 1 and badges[0].text.strip() == str(expected_count)

        self.wait.until(condition)

    def add_to_cart(self, product_name: str) -> None:
        button = (By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button")
        self.click(button)
        self._wait_for_cart_count(1)

    def remove_from_cart(self, product_name: str) -> None:
        button = (
            By.XPATH,
            f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button[contains(text(),'Remove')]",
        )
        self.click_via_js(button)
        self._wait_for_cart_count(0)

    def products_count(self) -> int:
        return self.count(self.INVENTORY_ITEM)

    def cart_items_count(self) -> int:
        if self.is_visible(self.CART_BADGE):
            return int(self.text_of(self.CART_BADGE))
        return 0

    def open_cart(self) -> None:
        self.click_via_js(self.CART_LINK)
        self.wait.until(ec.url_contains("cart.html"))
