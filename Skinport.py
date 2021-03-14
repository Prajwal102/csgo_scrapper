from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import re
import json


def skinport(name):


    # options = Options()
    # options.headless = True
    # driver = webdriver.Chrome(chrome_options=options)
   
    driver = webdriver.Chrome()


    # name = "butterfly knife slaughter"
    driver.get("https://skinport.com/")

    elem = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME,"SearchField-input"))
        )
    elem =  driver.find_element_by_class_name("SearchField-input")
    elem.send_keys(name)

                
    root_url = WebDriverWait(driver, 40).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "SearchField-listItem")))[2].get_attribute('href')

    d = {
    'source':'skinport',
    'conditions': {
    'Factory New': {'price': 'NA'},
    'Minimal Wear': {'price': 'NA'},
    'Field-Tested': {'price': 'NA'},
    'Well-Worn': {'price': 'NA'},
    'Battle-Scarred': {'price': 'NA'}
    }
    }

    wear_name = {
    1: 'Battle-Scarred',
    2: 'Factory New',
    3: 'Field-Tested',
    4: 'Minimal Wear',
    5: 'Well-Worn'
    }

    for ext in [1,2,3,4,5]:
        url = f"{root_url}&sort=price&order=asc&exterior={ext}&stattrak=0"
        driver.get(url)
        try:
            iteminfo = "//div[@class='ItemPreview-itemInfo']"
            element = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH,iteminfo))
            )

            price = element.find_element_by_xpath(f"{iteminfo}/div[@class='ItemPreview-price']/div[@class='ItemPreview-priceValue']/div[@class='Tooltip-link']").text
            d['conditions'][wear_name[ext]]['price'] = price

        except:
            # print(wear_name[ext])
            pass

    return json.dumps(d)
