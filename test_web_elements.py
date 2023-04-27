from page_objects.BasePage import BasePage


def test_elements_1(browser, open_page):
    main_window = browser.current_window_handle
    base_page = BasePage(browser)
    click_here = base_page.get_locator_by_css('#content a')
    click_here.click()
    new_window = [window for window in browser.window_handles if window != main_window][0]
    browser.switch_to.window(new_window)
    assert 'New Window' == base_page.get_locator_by_css('h3').text
    browser.close()
    browser.switch_to.window(main_window)
    assert click_here.is_displayed()


def test_elements_2(browser, open_page):
    main_window = browser.current_window_handle
    base_page = BasePage(browser)
    click_here = base_page.get_locator_by_css('#content a')
    click_here.click()
    new_window = [window for window in browser.window_handles if window != main_window][0]
    browser.switch_to.window(new_window)
    assert 'New Window' == base_page.get_locator_by_css('h3').text
    browser.close()
    browser.switch_to.window(main_window)
    assert click_here.is_displayed()


def test_elements_3(browser, open_page):
    main_window = browser.current_window_handle
    base_page = BasePage(browser)
    click_here = base_page.get_locator_by_css('#content a')
    click_here.click()
    new_window = [window for window in browser.window_handles if window != main_window][0]
    browser.switch_to.window(new_window)
    assert 'New Window' == base_page.get_locator_by_css('h3').text
    browser.close()
    browser.switch_to.window(main_window)
    assert not click_here.is_displayed()


def test_4(browser, open_page):

