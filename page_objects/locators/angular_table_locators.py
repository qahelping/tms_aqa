from collections import namedtuple

from lib.core.helpers import XPath


class AngularTableLocators:
    _TABLE_STATUS = namedtuple('_TABLE_STATUS',
                               ['active', 'processing', 'rejected', 'edit', 'close'])

    STATUS = _TABLE_STATUS(
        active=XPath.get_by_contained_class('status_active'),
        processing=XPath.get_by_contained_class('status_processing'),
        rejected=XPath.get_by_contained_class('status_rejected'),
        edit=XPath.get_by_contained_class('status_edit'),
        close=XPath.get_by_contained_class('status_closed'))

    TABLE_COLUMN_1 = '//table/tbody/tr/td[1]'
    TABLE_COLUMN_2 = '//table/tbody/tr/td[2]'
    TABLE_COLUMN_3 = '//table/tbody/tr/td[3]'
    TABLE_COLUMN_4 = '//table/tbody/tr/td[4]'
    TABLE_COLUMN_5 = '//table/tbody/tr/td[5]'
    TABLE_COLUMN_6 = '//table/tbody/tr/td[6]'

    TABLE_COLUMN_1_TEXT = '//table/tbody/tr/td[1]//span'

    BUTTON_LINK = XPath.get_by_class('btn-link')

    EDIT_BUTTON = '//icon-edit'
    REPEAT_BUTTON = '//icon-repeat'
    DELETE_BUTTON = '//icon-bin'
    EXCEPTION = '//icon-exception'
    EMPTY_PAGE = '//empty-page'

    TABLE = '//table'

