import json
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from ui_tests.pages.cart_page import CartPage
from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.products_page import ProductsPage

load_dotenv()


def _load_test_users() -> dict:
    path = Path(__file__).resolve().parents[1] / "data" / "test_users.json"
    with path.open("r", encoding="utf-8") as users_file:
        return json.load(users_file)


@pytest.fixture(scope="module")
def users_data():
    return _load_test_users()


@pytest.fixture
def login_page(driver):
    page = LoginPage(driver, timeout=int(os.getenv("TIMEOUT", "10")))
    page.open(os.getenv("BASE_URL", "https://www.saucedemo.com"))
    return page


@pytest.fixture
def logged_in_products_page(login_page):
    username = os.getenv("TEST_USER", "standard_user")
    password = os.getenv("TEST_PASSWORD", "secret_sauce")
    login_page.login(username, password)
    return ProductsPage(login_page.driver, timeout=int(os.getenv("TIMEOUT", "10")))


@pytest.mark.ui
@pytest.mark.smoke
def test_user_can_login(login_page):
    username = os.getenv("TEST_USER", "standard_user")
    password = os.getenv("TEST_PASSWORD", "secret_sauce")
    login_page.login(username, password)
    assert login_page.is_logged_in()


@pytest.mark.ui
def test_locked_user_cannot_login(login_page, users_data):
    login_page.login(users_data["locked_user"]["username"], users_data["locked_user"]["password"])
    assert "locked out" in login_page.get_error().lower()


@pytest.mark.ui
def test_add_product_to_cart(logged_in_products_page):
    logged_in_products_page.add_to_cart("Sauce Labs Backpack")
    assert logged_in_products_page.cart_items_count() == 1


@pytest.mark.ui
def test_remove_product_from_cart(logged_in_products_page):
    logged_in_products_page.add_to_cart("Sauce Labs Backpack")
    assert logged_in_products_page.cart_items_count() == 1
    logged_in_products_page.remove_from_cart("Sauce Labs Backpack")
    assert logged_in_products_page.cart_items_count() == 0


@pytest.mark.ui
def test_products_count_on_page(logged_in_products_page):
    assert logged_in_products_page.products_count() == 6


@pytest.mark.ui
@pytest.mark.slow
def test_full_purchase_cycle(logged_in_products_page):
    logged_in_products_page.add_to_cart("Sauce Labs Backpack")
    logged_in_products_page.open_cart()
    cart_page = CartPage(logged_in_products_page.driver)
    assert cart_page.cart_items_count() == 1
    cart_page.start_checkout()
    cart_page.fill_checkout_form("Alex", "QA", "10000")
    cart_page.finish_checkout()
    assert "thank you" in cart_page.checkout_success_message().lower()


@pytest.mark.ui
def test_remove_item_in_cart_page(logged_in_products_page):
    logged_in_products_page.add_to_cart("Sauce Labs Backpack")
    logged_in_products_page.open_cart()
    cart_page = CartPage(logged_in_products_page.driver)
    cart_page.remove_item("Sauce Labs Backpack")
    assert cart_page.cart_items_count() == 0
