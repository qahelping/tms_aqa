import pytest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


@pytest.fixture
def browser(request):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    browser = request.config.getoption("--browser")
    if browser == 'chrome':
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(5)
    else:
        driver = webdriver.Firefox()
        driver.implicitly_wait(5)

    yield driver

    driver.quit()


@pytest.fixture
def open_page(browser):
    # browser.get('https://ultimateqa.com/simple-html-elements-for-automation/')
    browser.get('http://the-internet.herokuapp.com/windows')


def pytest_addoption(parser):
    parser.addoption("--address", action="store", default="http://192.168.122.244/", help="HuntBox web address")
    parser.addoption("--browser", action="store", default="firefox", help="Browser name")
