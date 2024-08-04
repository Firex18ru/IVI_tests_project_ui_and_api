import os

import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from ivi_tests_API_and_Ui_framework.utils import attach


def video_url():
    return None


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.base_url = "https://www.ivi.ru"

    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "126.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }

    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
        options=options)

    browser.config.driver = driver

    yield

    attach.add_screenshot(browser)
    attach.add_html(browser)
    attach.add_logs(browser)
    attach.add_video(browser)
    browser.quit()
