import os

import allure
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()


def _to_bool(value: str) -> bool:
    return str(value).lower() in ("1", "true", "yes", "on")


@pytest.fixture
def driver(request):
    headless = _to_bool(os.getenv("HEADLESS", "False"))
    timeout = int(os.getenv("TIMEOUT", "10"))
    grid_url = os.getenv("SELENIUM_GRID_URL")

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = None
    if grid_url:
        try:
            browser = webdriver.Remote(
                command_executor=grid_url,
                options=options,
            )
        except Exception:
            browser = None

    if browser is None:
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)

    browser.implicitly_wait(timeout)
    request.node._driver = browser  # pylint: disable=protected-access
    yield browser
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        browser = getattr(item, "_driver", None)
        if browser:
            try:
                allure.attach(
                    browser.get_screenshot_as_png(),
                    name=f"failure_{item.name}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                # Browser may already be gone in remote-grid flaky failures.
                pass
