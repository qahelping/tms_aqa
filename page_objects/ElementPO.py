from page_objects.BasePage import BasePage
from page_objects.ElementLocators import ElementLocators


class ElementsObject(BasePage, ElementLocators):
    radio_button = "input[value=mails]"


    def click_on_radio_button(self):
        self.click(self.radio_button)


