import time
import requests
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from grabbers.realtor_numbers_grabber.file_manager import add_to_file

driver = Firefox()
# go to olx
driver.get("http://chernovtsy.chv.olx.ua/nedvizhimost/?search[private_business]=business")

next_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.next .pageNextPrev')))
while next_page is not None:
    # find all links to publications on current page
    links = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, '#offers_table .link.linkWithHash.detailsLink')))
    for link in links:
        # define id of publication from link
        link_address = link.get_attribute('href')
        start_id = link_address.find('ID') + 2
        end_id = link_address.find('.html')
        ID = link_address[start_id:end_id]
        try:
            # get request with phone number of owner of publication
            response = requests.get('http://chernovtsy.chv.olx.ua/ajax/misc/contact/phone/' + ID + '/')
            print response
            print response.json()['value']
            # format phone number and add to file
            add_to_file(response.json()['value'])
        except:
            pass
    # if there is a link to next page than click on it and continue grabbing
    # else quit grabbing
    try:
        next_page = driver.find_element_by_css_selector('.next .pageNextPrev')
        next_page.click()
        time.sleep(5)
    except:
        driver.quit()
        next_page = None
