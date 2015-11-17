# coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from grabbers.realtor_numbers_grabber.file_manager import add_to_file


driver = webdriver.Firefox()
retail_driver = webdriver.Firefox()
# go to dom.ria.com
driver.get('https://dom.ria.com/ru/search/#page=157&limit=10&from_realty_id=&to_realty_id=&sort=0&category=1&realty_type=0&operation_type=3&state_id=10')
next_page = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.big-controls .fl-r')))
while next_page is not None:
    # find all links to publications on current page
    links = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.view-all a.more')))
    for link in links:
        # open link to publication in retail driver
        print link.get_attribute('href')
        retail_driver.get(link.get_attribute('href'))
        # get phone numbers of owner of publication
        try:
            numbers_blocks = WebDriverWait(retail_driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.phone')))
            # format phone numbers and add to file
            for numbers in numbers_blocks:
                print numbers.text
                add_to_file(numbers.text)
        except:
            continue
        time.sleep(2)
    # if there is a link to next page than click on it and continue grabbing
    # else quit grabbing
    try:
        next_page = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.big-controls .fl-r')))
        next_page.click()
    except:
        next_page = None
        page_url = driver.current_url
        print(page_url)
        driver.quit()
        retail_driver.quit()
