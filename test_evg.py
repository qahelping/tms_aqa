from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_1234():
    # создаем экземпляр драйвера Chrome
    driver = webdriver.Chrome()

    # открываем страницу
    driver.get('https://demoqa.com/droppable')
    driver.implicitly_wait(1)
    # находим элементы для drag and drop
    source_element = driver.find_element(By.XPATH, '//*[@id="draggable"]')
    target_element = driver.find_element(By.XPATH, '//*[@id="droppable"]')

    # создаем экземпляр класса ActionChains для выполнения drag and drop
    actions = ActionChains(driver)

    # перемещаем элемент source_element на элемент target_element
    actions.drag_and_drop(source_element, target_element).perform()

    # ожидаем, пока элемент target_element изменит свой текст, что означает успешное выполнение drag and drop
    wait = WebDriverWait(driver, 10)
    wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="droppable"]/p'), 'Dropped!'))

    # закрываем браузер
    driver.quit()
