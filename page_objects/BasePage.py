from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

WAIT_TIME = 10


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def get_element_by_xpath(self, selector):
        return self.driver.find_element(By.XPATH, selector)

    def get_element_by_contains_class(self, selector):
        return self.driver.find_element(By.XPATH, f'//div[contains(@class,"{selector}")]')

    def get_element_by_contains_text(self, text):
        return self.driver.find_element(By.XPATH, f'//*[contains(text(),"{text}")]')

    def click(self, selector, js=False):
        element = self.get_element_by_xpath(selector)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        if js == False:
            element.click()
        else:
            self.driver.execute_script("arguments[0].click();", element)

    def fill_field(self, selector, text):
        element = self.get_element_by_xpath(selector)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        element.clear()
        element.send_keys()

    def assert_that_element_is_selected(self, selector):
        return self.get_locator_by_css(selector).is_selected()
