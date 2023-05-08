import os
import sys

from pytest import fixture, Class
from selenium import webdriver

from lib.core.base_test import BaseTest


class BaseGUITest(BaseTest):

    driver = None

    @fixture(scope='class', autouse=True)
    def setup_chrome_webdriver(self, pytestconfig, request):
        selenium_config = pytestconfig.conf.selenium
        # Set Chrome options
        options = webdriver.ChromeOptions()
        no_words = ('disable', 'disabled', 'no', 'off')
        headless = not bool(pytestconfig.getoption('headless') in no_words)  # headless mode is enabled by default
        # TODO: Review chrome options, remove deprecated
        if headless:
            options.add_argument('headless')
            options.add_argument('no-sandbox')
        options.add_argument('disable-gpu')
        options.add_argument(f'remote-debugging-port={selenium_config.remote_port}')
        options.add_argument('window-size=1900x1600')
        preferences = {'download.default_directory': selenium_config.downloads}
        options.add_experimental_option('prefs', preferences)

        # TODO: Seems that capabilities are deprecated, check and remove if necessary
        # Set capabilities
        # capabilities = DesiredCapabilities.CHROME
        # capabilities['goog:loggingPrefs'] = {'performance': 'DEBUG', 'browser': 'ALL', 'driver': 'ALL'}

        # Start driver
        driver = webdriver.Remote(
            command_executor=selenium_config.url,
            # desired_capabilities=capabilities,
            options=options,
        )
        # Pages are initiated with driver, this allows to pass configuration data to pages within driver
        driver.config = pytestconfig.conf
        driver.implicitly_wait(5)
        driver.maximize_window()

        # Assign driver to existing test classes
        session = request.node.session
        for item in session.items:
            if issubclass(item.getparent(Class).cls, BaseGUITest):
                item.cls.driver = driver

        yield

        driver.close()

    @fixture(scope='function', autouse=True)
    def cleanup_driver_data_after_test(self):
        yield
        # TODO: The next was copied as is, review and refactor it
        self.driver.delete_all_cookies()
        try:
            if len(self.driver.window_handles) > 1:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
        except:
            print('Unexpected error: ', sys.exc_info()[0])
        self.driver.get('data:,')

    # Checking every test for failure to make a screenshot
    @fixture(scope='function', autouse=True)
    def make_failed_screenshot(self, request):
        yield
        if request.node.report:  # See pytest_runtest_makereport() in conftest.py
            if request.node.report.failed:
                # TODO: refactor the next string to use path from the config: request.config.conf.pytest.screenshots
                path = 'p3_failed_tests_data/'
                self.make_dir(path)
                file_path = 'p3_failed_tests_data/' + f'{request.node.name}.png'
                self.driver.save_screenshot(path + f'{request.node.name}.png')
                print('\nError path ', self.driver.current_url)
                print('\nScreenshot ', file_path)

    # Create directory if it doesn't exist already
    @staticmethod
    def make_dir(directory_name):
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
