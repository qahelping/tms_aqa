import pytest
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

@pytest.fixture
def browser():
    print("-------")
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    yield driver

    driver.close()
    driver.quit()

    print("+++++++++")


@pytest.fixture
def browser_firefox():
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.implicitly_wait(5)

    yield driver

    driver.close()
    driver.quit()

@pytest.fixture
def open_page(browser):
    browser.get('https://ultimateqa.com/simple-html-elements-for-automation/')