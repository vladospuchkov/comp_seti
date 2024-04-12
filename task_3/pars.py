from time import sleep
from urllib.parse import unquote

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement



class pathes():
    main_banner = '/html/body/div[2]/div/div/div[3]/div[1]/div/div/div/div[2]'
    cookie_banner = '/html/body/div[2]/div/div/div[3]/footer/div[2]'
    items_count = '/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[1]/header/div[3]/div/div[1]/div/div/a/span'
    main_block = '/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[2]/div'
    title = '/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/h1/span[1]'
    phone_btn = '/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div[1]/div/div[3]/div[2]/div/button'
    phone = '/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div[2]/div/a/bdo'
    address = '/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/div/div[2]/div[1]'
    next_page_btn = '/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div[2]/div[2]'


TABLE_COLUMNS = ['Название', 'Телефон', 'Адрес', 'Ссылка']
TABLE = {column: [] for column in TABLE_COLUMNS}

def get_element_text(driver: WebDriver, path: str) -> str:
    try:
        return driver.find_element(By.XPATH, path).text
    except NoSuchElementException:
        return ''

def move_to_element(driver: WebDriver, element: WebElement | WebDriver) -> None:
    try:
        webdriver.ActionChains(driver).move_to_element(element).perform()
    except StaleElementReferenceException:
        pass


def element_click(driver: WebDriver | WebElement, path: str) -> bool:
    try:
        driver.find_element(By.XPATH, path).click()
        return True
    except:
        return False

def main():
    search_query = 'сексшоп'
    url = f'https://2gis.ru/novosibirsk/search/{search_query}'
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    element_click(driver, pathes.main_banner)
    element_click(driver, pathes.cookie_banner)
    count_all_items = int(get_element_text(driver, pathes.items_count))
    pages = round(count_all_items / 12 + 0.5)

    for _ in range(pages):
        main_block = driver.find_element(By.XPATH, pathes.main_block)
        count_items = len(main_block.find_elements(By.XPATH, 'div'))
        
        for item in range(1, count_items + 1):
            if main_block.find_element(By.XPATH, f'div[{item}]').get_attribute('class'):
                continue
            item_clicked = element_click(main_block, f'div[{item}]/div/div[2]')
            
            if not item_clicked:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                element_click(main_block, f'div[{item}]/div/div[2]')
            
            title = get_element_text(driver, pathes.title)
            phone_btn_clicked = element_click(driver, pathes.phone_btn)
            phone = get_element_text(driver, pathes.phone) if phone_btn_clicked else ''
            move_to_element(driver, main_block)
            link = unquote(driver.current_url)
            address = get_element_text(driver, pathes.address)
            
            TABLE['Название'].append(title)
            TABLE['Телефон'].append(phone)
            TABLE['Адрес'].append(address)
            TABLE['Ссылка'].append(link)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element_click(driver, pathes.next_page_btn)
        sleep(0.5)
    driver.quit()
    pd.DataFrame(TABLE).to_csv("result.csv")


if __name__ == '__main__':
    main()

    