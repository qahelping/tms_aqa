import allure

from lib.monolith.constants.constant_urls import CATALOG_PAGE_URL, WORKAROUND_SETTINGS_URL_WEB
from page_objects.monolith.locators.webmaster import WebmasterCatalogLocators
from page_objects.monolith.pages.common import BasePage


class WebmasterCatalogPage(BasePage, WebmasterCatalogLocators):
    def __init__(self, driver=None):
        super(WebmasterCatalogPage, self).__init__(driver)

    @allure.step('Open catalog page')
    def open_catalog_page(self):
        self.open_page(CATALOG_PAGE_URL)

    @allure.step('Check that catalog page displays a list of sort options')
    def assert_that_catalog_page_has_sorting_options(self):
        self.assert_exist_element(self.CATALOG_SORTING_OPTIONS_LIST)

        self.screenshot()

    @allure.step('Check that catalog page displays a list of filters')
    def assert_that_catalog_page_has_filters(self):
        self.assert_exist_element(self.CATALOG_FILTER_PANEL)

        self.screenshot()

    @allure.step('Check that page footer is displayed on the catalog page')
    def assert_that_page_footer_is_present(self):
        self.assert_exist_element(self.PAGE_FOOTER)

        self.screenshot()

    @allure.step('Check that tabs are displayed in web settings')
    def assert_that_web_settings_tabs_are_present(self):
        self.open_page(WORKAROUND_SETTINGS_URL_WEB)
        self.assert_exist_element(self.SETTINGS_WEBSITES_TAB)
        self.assert_exist_element(self.SETTINGS_GUESTS_TAB)

        self.screenshot()
