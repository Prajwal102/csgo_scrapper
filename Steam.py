from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import re
import json


# options = Options()
# options.headless = True
# driver = webdriver.Chrome(chrome_options=options)

# driver.implicitly_wait(20) # seconds
# name = "butterfly knife slaughter"


def steam(name):
    driver = webdriver.Chrome()
    url = f"https://steamcommunity.com/market/search?appid=730&q={name}"
    driver.get(url)
    # try:
    iteminfo = """/html[@class=' responsive']/body[@class=' responsive_page']/
                    div[@class='responsive_page_frame with_header']/
                    div[@class='responsive_page_content']/
                    div[@class='responsive_page_template_content']/
                    div[@class='pagecontent no_header ']/
                    div[@id='BG_bottom']/div[@id='mainContents']/
                    div[@id='searchResults']/div[@id='searchResultsTable']/div[@id='searchResultsRows']/
                    div[@class='market_listing_row market_recent_listing_row market_listing_searchresult']"""

    class_name = "market_listing_row market_recent_listing_row market_listing_searchresult"
    d = {
        'source':'steam',
        'conditions': {
        'Factory New': {'price': 'NA'},
        'Minimal Wear': {'price': 'NA'},
        'Field-Tested': {'price': 'NA'},
        'Well-Worn': {'price': 'NA'},
        'Battle-Scarred': {'price': 'NA'}
    }
    }
    # element = WebDriverWait(driver, 10).until(
    #     EC.visibility_of_all_elements_located((By.CLASS_NAME,class_name))
    # )
    el = driver.find_elements_by_class_name('market_listing_row_link')


    all_res = [e.text for e in el]

    for i in all_res:
        temp = i.split("\n")
        temp = temp[2:4]
        # print(temp[1][0])
        if not temp[1].startswith('StatTrak'):
            price = temp[0][:-4]
            condition = re.search(r'\((.*?)\)',temp[1]).group(1)
            d['conditions'][condition]['price'] = price
    # print(d)
    return json.dumps(d)
    # except:
    #     print("some error")
