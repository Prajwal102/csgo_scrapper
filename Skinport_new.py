from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import re
import json



def scrapper_func(url):
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    try:
        iteminfo = "//div[@class='ItemPreview-itemInfo']"
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,iteminfo))
        )

        price = element.find_element_by_xpath(f"{iteminfo}/div[@class='ItemPreview-price']/div[@class='ItemPreview-priceValue']/div[@class='Tooltip-link']").text
        return price
    except:
        return 

    
def get_root_url(name):
    driver = webdriver.Chrome()
    driver.get("https://skinport.com/")

    elem = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME,"SearchField-input"))
        )
    elem =  driver.find_element_by_class_name("SearchField-input")
    elem.send_keys(name)
                
    root_url = WebDriverWait(driver, 40).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "SearchField-listItem")))[2].get_attribute('href')
    driver.quit()

    return root_url

def skinport(name):

    # options = Options()
    # options.headless = True
    # driver = webdriver.Chrome(chrome_options=options)
    root_url = get_root_url(name)
    
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


    # futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # endpt = f"{root_url}&sort=price&order=asc&exterior={ext}&stattrak=0"
        futures = {executor.submit(scrapper_func,url = f"{root_url}&sort=price&order=asc&exterior={ext}&stattrak=0") : ext for ext in [1,2,3,4,5]}


        for future in concurrent.futures.as_completed(futures):
            # print(future.result())
            future_res = futures[future]
            condition = wear_name[future_res]
            d['conditions'][condition]['price'] = future.result()

    
    return (json.dumps(d))


print(skinport("butterfly knife slaughter"))