from selenium.webdriver.common.by import By

from ui_tests.pages.base_page import BasePage


class ProductsPage(BasePage):
    PAGE_TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    INVENTORY_ITEM = (By.CSS_SELECTOR, ".inventory_item")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def add_to_cart(self, product_name: str) -> None:
        button = (By.XPATH, f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button")
        self.click(button)

    def remove_from_cart(self, product_name: str) -> None:
        button = (
            By.XPATH,
            f"//div[text()='{product_name}']/ancestor::div[@class='inventory_item']//button[contains(text(),'Remove')]",
        )
        self.click(button)

    def products_count(self) -> int:
        return self.count(self.INVENTORY_ITEM)

    def cart_items_count(self) -> int:
        if self.is_visible(self.CART_BADGE):
            return int(self.text_of(self.CART_BADGE))
        return 0

    def open_cart(self) -> None:
        self.click(self.CART_LINK)
