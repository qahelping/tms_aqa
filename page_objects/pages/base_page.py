from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)


class BasePage:

    def __init__(self, driver=None, wait_timeout=10):
        self.driver = driver
        self.config = driver.config if driver else None
        self.wait = WebDriverWait(self.driver, wait_timeout)

    def check_exists_by_xpath(self, xpath):
        """
        Needed for asserts, returns:
            True - if element exist
            False - if element not exist
        """
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False, None
        return True, self.driver.find_element_by_xpath(xpath)

    def clear_cookies(self):
        self.driver.delete_all_cookies()

    def click_on_dropdown(self, first_element, second_element):
        self.move_mouse_to_element(first_element)
        self.click_on_element(second_element)

    def dropdown_click(self, first_element, second_element):
        """
        Temporary alternative to the above method. TODO eliminate one of the methods
        """
        self.move_mouse_to_element(first_element)
        self.click_on_element(second_element)

    def click_on_element(self, xpath, using_js=False):
        element = self.get_element(xpath)
        self.scroll_to_element(xpath)
        # TODO: Refactor this, we need some working 'wait_for_clickable' here
        # Next code line (commented) doesn't work as expected for some cases
        # self.wait_for_clickable(xpath)
        if using_js:
            self.driver.execute_script('arguments[0].click();', element)
        else:
            element.click()

    def close_tab(self):
        self.driver.close()
        self.switch_to_the_last_window()

    def get_element(self, xpath):
        # Just an alias for 'wait_for_visible' method
        return self.wait_for_visible(xpath)

    def get_selected_option_text(self, xpath):
        select = Select(self.get_element(xpath))
        selected_option = select.first_selected_option.text
        return selected_option

    def fill_field(self, xpath, value, is_invisible=False, clear=True):
        if is_invisible:
            # Get element by low-level method without waits
            element = self.driver.find_element_by_xpath(xpath)
        else:
            element = self.get_element(xpath)
            self.scroll_to_element(xpath)
        if clear:
            element.clear()
        element.send_keys(value)

    def move_mouse_to_element(self, xpath):
        element = self.get_element(xpath)
        ActionChains(self.driver).move_to_element(element).perform()

    def open_page(self, url):
        self.driver.get(url)

    def select_from_autocomplete_list(self, xpath, option):
        """Select from dropdown autocomplete by option"""
        self.wait_for_visible(xpath)
        self.scroll_to_element(xpath)
        self.fill_field(xpath, option)
        # TODO: Rework this to do not use a hardcoded value
        locator_option = f'//*[contains(@class, "mat-option-text") and contains(.,"{option}")]'
        self.click_on_element(locator_option)

    def scroll_to_element(self, xpath):
        element = self.get_element(xpath)
        self.driver.execute_script('arguments[0].scrollIntoView();', element)

    def switch_to_frame(self, number):
        self.driver.switch_to.frame(number)

    def switch_to_iframe_by_xpath(self, xpath):
        frame = self.driver.find_element_by_xpath(xpath)
        self.driver.switch_to.frame(frame)

    def switch_to_iframe_by_tag(self, tag_name):
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name(tag_name))

    def switch_to_parent_frame(self):
        self.driver.switch_to.parent_frame()

    def switch_to_window(self, number):
        try:
            self.driver.switch_to.window(self.driver.window_handles[number])
        except IndexError:
            assert False, f'Failed to switch window {number}'

    def switch_to_the_last_window(self):
        self.switch_to_window(len(self.driver.window_handles) - 1)

    def switch_to_main_window(self):
        self.driver.switch_to.default_content()

    def wait_for_visible(self, xpath):
        # Simple method to detect visible element
        try:
            return self.wait.until(ec.element_to_be_clickable((By.XPATH, xpath)))
        except WebDriverException:
            assert False, f'Failed to find element by XPATH {xpath}'

    def wait_for_clickable(self, xpath):
        return self.wait.until(ec.element_to_be_clickable((By.XPATH, xpath)))

    def wait_for_visible_by_hard(self, xpath, retry=5):
        # Time consuming method to detect visible element
        element = None
        for _ in range(retry):
            try:
                element = self.driver.find_element_by_xpath(xpath)
                break
            except WebDriverException:
                print(f'Failed to find element, will try again. XPATH {xpath}')
                sleep(1)  # Is there any way to avoid sleep()?

        assert element, f'Did not find element. XPATH {xpath}'  # Is assert needed here?
        return element

    def get_text_from_element(self, xpath):
        return self.wait_for_visible_by_hard(xpath).text

    def refresh_page(self):
        self.driver.refresh()

    def screenshot(self):
        pass
        # TODO no allure reports yet, enable later
        """allure.attach(self.driver.get_screenshot_as_png(),
                      name='screenshot_{date}'.format(date=datetime.now()),
                      attachment_type=AttachmentType.PNG)"""

    def wait_until_element_disappears(self, xpath, timeout=5):
        """
        Wait till target element is not longer visible
        """
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
            wait.until_not(ec.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            pass

    def select_option_by_visible_text(self, xpath, text):
        self.wait_for_clickable(xpath)
        select = Select(self.wait_for_visible_by_hard(xpath))
        select.select_by_visible_text(text)

    def accept_alert(self):
        alert = self.driver.switch_to.alert
        alert.accept()

    def wait_angular_loader_disappear(self):
        angular_loader = '//div[@class="angular-loader angular-loader--local angular-loader--modal modal"]'
        self.wait_until_element_disappears(angular_loader)

    def wait_overlay_disappear(self):
        overlay = '//div[@class"load-overlay"]'
        self.wait_until_element_disappears(overlay)

    def scroll_to_basement(self):
        # TODO this method didn't work last time I've checked, investigate and fix later
        body = self.driver.find_element_by_css_selector('body')
        body.send_keys(Keys.END)

    def upload_file_field(self, xpath, value):
        _, element = self.check_exists_by_xpath(xpath)
        element.send_keys(value)

    def select_campaign_hq(self, xpath, option):
        """
        Select chosen campaign in auto-complete in hq
        """
        choose_campaign_button = '//a[contains(@class,"ui-corner-all") and contains(.,"{campaign}")]'
        self.fill_field(xpath, option)
        self.click_on_element(choose_campaign_button.format(campaign=option))

    def select_option_by_value(self, xpath, value):
        self.wait_for_visible(xpath)
        select = Select(self.wait_for_visible(xpath))
        select.select_by_value(str(value))

    def wait_for_present_in_element_value(self, xpath, text):
        element = None
        for _ in range(5):
            try:
                element = self.wait.until(ec.text_to_be_present_in_element_value((By.XPATH, xpath), text))
                break
            except WebDriverException:
                print(f'Failed to find change value element. XPATH {xpath}')
        assert element, f'Didn`t find change value element. XPATH {xpath}'
        return element

    def click_on_enter(self):
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()

    def multi_select_by_visible_text(self, xpath, data):
        items = data.split(', ')
        for item in items:
            self.select_option_by_visible_text(xpath, item)

    def get_attribute_value(self, locator, attr):
        """Getting attribute value of the target element as a string"""
        element = self.wait_for_visible(locator)
        self.scroll_to_element(locator)
        return str(element.get_attribute(attr))

    def check_if_element_is_displayed(self, xpath):
        element = self.driver.find_element_by_xpath(xpath)
        return element.is_displayed()

    def select_from_list(self, xpath, option):
        """select from usual selector for angular"""
        OPTION = '//*[contains(@class, "mat-option-text") and contains(.,"{option}")]'
        self.scroll_to_element(xpath)
        self.click_on_element(xpath)
        self.click_on_element(OPTION.format(option=option))

    # Assertions (from legacy Assertions class)

    def assert_that_attribute_present(self, xpath, attribute):
        element = self.wait_for_visible_by_hard(xpath)
        value = element.get_attribute(attribute)
        if value is not None:
            return True
        return False

    def assert_that_element_is_visible(self, xpath):
        element = self.wait_for_visible(xpath)
        assert element, f'Element {xpath} is not visible on page.'

    def assert_exist_element(self, xpath):
        is_exists, _ = self.check_exists_by_xpath(xpath)
        assert is_exists, f"Element {xpath} doesn't exist on the page!"

    def assert_not_exist_element(self, xpath):
        is_exists, _ = self.check_exists_by_xpath(xpath)
        assert not is_exists, f"Element {xpath} exists on the page!"

    def assert_text_on_page(self, contains_text):
        xpath = f'//*[contains(.,"{contains_text}")]'
        check_element, _ = self.check_exists_by_xpath(xpath)
        assert check_element, f"Text isn't visible on the page! TEXT: {xpath}"

    def assert_text_not_on_page(self, contains_text):
        xpath = f'//*[contains(.,"{contains_text}")]'
        check_element, _ = self.check_exists_by_xpath(xpath)
        assert not check_element, f"Text is visible on the page! TEXT: {xpath}"

    def assert_text_in_element(self, xpath, text):
        """Check that the text has a specific element"""
        text_in_elt = self.get_text_from_element(xpath)
        assert text in text_in_elt, f"Text {text} is not on element {xpath}, but found {text_in_elt}"

    def assert_text_variants_in_element(self, xpath, texts):
        """Check that in specific element there is one variant of the text"""
        text_in_elt = self.get_text_from_element(xpath)
        text_variant_was_found = False
        for text in texts:
            if text in text_in_elt:
                text_variant_was_found = True
                break
        assert text_variant_was_found, f"Texts {texts} is not on element {xpath}, but found {text_in_elt}"

    def assert_not_text_in_element(self, xpath, text):
        """Проверяем отсутствие нужного текста в опеределенном элементе"""
        element = self.get_text_from_element(xpath)
        assert text not in element, f"Text {xpath} is on element {element}"

    def assert_disable_attribute(self, xpath):
        """Check that element is blocked for editing"""
        assert self.assert_that_attribute_present(xpath, 'disabled'), f"Element '{xpath}' doesn't have attr disabled"

    def assert_value_of_attribute(self, xpath, attr, value):
        element = self.get_element(xpath)
        actual_value = element.get_attribute(attr)
        assert str(value) == str(actual_value), f"Attr of '{xpath}', value: '{value}' != actual_value: '{actual_value}'"

    def reload_page(self):
        self.driver.refresh()

    def assert_element_not_visible_but_exists(self, xpath, another_element_on_page=None):
        """Check that the element is not displayed but exists in the DOM"""
        if another_element_on_page:
            self.wait_for_visible(another_element_on_page)
        element = self.wait.until(ec.invisibility_of_element_located((By.XPATH, xpath)))
        assert element, f"Element '{xpath}' is visible on the page!"

    def assert_element_is_not_displayed(self, xpath):
        try:
            displayed = self.driver.find_element_by_xpath(xpath).is_displayed()
            assert not displayed, f"Text {xpath} displayed"
        except NoSuchElementException:
            print(f'Failed to find element. XPATH {xpath}')

    def assert_checkbox_selected(self, xpath):
        checkbox = self.wait_for_visible_by_hard(xpath)
        assert checkbox.is_selected(), f'Checkbox {xpath} is not selected'

    def assert_checkbox_not_selected(self, xpath):
        checkbox = self.wait_for_visible_by_hard(xpath)
        assert not checkbox.is_selected(), f'Checkbox {xpath} is selected'
