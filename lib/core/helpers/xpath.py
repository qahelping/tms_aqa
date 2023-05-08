class XPath:

    # Methods for further refactoring

    @staticmethod
    def get_by_attribute_value(attribute, value, element='*'):
        attribute = XPath.set_attribute_prefix(attribute)
        return f'//{element}[{attribute}="{value}"]'

    @staticmethod
    def get_by_attribute_value_contained(attribute, value, element='*'):
        attribute = XPath.set_attribute_prefix(attribute)
        return f'//{element}[contains({attribute},"{value}")]'

    @staticmethod
    def set_attribute_prefix(attribute):
        return f'@{attribute}' if (not attribute.startswith('@') and (not attribute.endswith(')'))) else attribute

    # Methods in use

    @staticmethod
    def get_by_class(class_name, attr='*'):
        return f'//{attr}[@class="{class_name}"]'

    @staticmethod
    def get_by_class_and_text(class_name, text, attr='*'):
        return XPath.get_by_xpath_and_text(
            xpath=XPath.get_by_class(class_name, attr),
            text=text,
        )

    @staticmethod
    def get_by_contained_class(class_name, attr='*'):
        return XPath.get_item_by_contained_data('@class', class_name, attr)

    @staticmethod
    def get_by_contained_text(text, attr='*'):
        return XPath.get_item_by_contained_data('text()', text, attr)

    @staticmethod
    def get_item_by_contained_data(item, data, attr='*'):
        return f'//{attr}[contains({item},"{data}")]'

    @staticmethod
    def get_by_data_test_id(data_test_id, attr='*'):
        return f'//{attr}[@data-test-id="{data_test_id}"]'

    @staticmethod
    def get_by_data_ng_test_id(data_ng_test_id, attr='*'):
        return f'//{attr}[@data-ng-test-id="{data_ng_test_id}"]'

    @staticmethod
    def get_by_data_test_id_and_text(data_test_id, text, attr='*'):
        return XPath.get_by_xpath_and_text(
            xpath=XPath.get_by_data_test_id(data_test_id, attr),
            text=text,
        )

    @staticmethod
    def get_by_id(element_id, element='*'):
        return XPath.get_by_attribute_value('id', element_id, element)
        # return f'//{attr}[@id="{element_id}"]'

    @staticmethod
    def get_by_xpath_and_text(xpath, text):
        return f'{xpath} [contains(text(),"{text}")]'

    @staticmethod
    def get_disabled_by_data_test_id(data_test_id, attr='*'):
        return f'//{attr}[@data-test-id="{data_test_id}" and @aria-disabled="true"]'

    # Alias for 'get_disabled_by_data_test_id'
    @staticmethod
    def get_disabled_element(data_test_id, attr='*'):
        return XPath.get_disabled_by_data_test_id(data_test_id, attr)

    # Alias for 'get_by_xpath_and_text'
    @staticmethod
    def get_from_element_and_text(xpath, text):
        return XPath.get_by_xpath_and_text(xpath, text)
