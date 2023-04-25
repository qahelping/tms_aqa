import time

from BasePage import BasePage
from ElementObject import ElementsObject


def test_1(browser, open_page):
    base_page = BasePage(browser)

    base_page.driver.get('https://ultimateqa.com/simple-html-elements-for-automation/')

    radio_button = base_page.click("input[value=other]")
    browser.save_screenshot("test_1(2).png")
    assert radio_button.is_selected()


def test_21(browser):
    base_page = BasePage(browser)
    base_page.driver.get('https://ultimateqa.com/simple-html-elements-for-automation/')
    base_page.click(ElementsObject.radio_button)
    browser.save_screenshot("test_1(2).png")
    assert base_page.assert_that_element_is_selected(ElementsObject.radio_button)
