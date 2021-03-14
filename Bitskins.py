import pyotp
import requests
import json
import concurrent.futures
from requests import Request


def get_responce(url):
    # print(url)
    return requests.get(url).json()
    # return res.json()



def bitskins(name):
    api_key = "e274eea4-0a51-4ae7-b2d6-f854f639a279"
    #C6A3F5F4AN6G47HS


    my_token = pyotp.TOTP("C6A3F5F4AN6G47HS")

    code = my_token.now()

    # name = "talon knife fade"
    payload = {
        'api_key': api_key,
        'code': code,
        'page': 1,
        'app_id': 730,
        'sort_by': 'price',
        'order': 'asc',
        'market_hash_name': name,
        'per_page': 24,

    }

    item_wears = ['Factory New',  'Minimal Wear', 'Field-Tested', 'Well-Worn','Battle-Scarred']
    # item_wears = ['Well-Worn']
    items_details = {
        'source':'bitskins',
        'conditions': {
        'Factory New': {'price': 'NA'},
        'Minimal Wear': {'price': 'NA'},
        'Field-Tested': {'price': 'NA'},
        'Well-Worn': {'price': 'NA'},
        'Battle-Scarred': {'price': 'NA'}
    }
    }
    futures =[]
    bitskins_endpoint = "https://bitskins.com/api/v1/get_inventory_on_sale/"
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for wear in item_wears:
            payload['item_wear'] = wear
            req = Request('GET',bitskins_endpoint,params=payload).prepare()
            future = executor.submit(get_responce,url=req.url)
            futures.append(future)
            
            # res = requests.get(bitskins_endpoint,params=payload)
        for future in concurrent.futures.as_completed(futures):
            # print(json.dumps(future.result()["data"]["items"]))
            json_object = future.result()
            if json_object["data"]["items"]:
                first_res = json_object["data"]["items"][0]
                price = first_res['price']
                exterior = first_res['tags']['exterior']
                # first_res = json.dumps(json_object["data"]["items"][0],indent = 3)
                items_details['conditions'][exterior]['price'] = '$'+price

            # items_details[wear]['url'] = res.url


        # return json.dumps(items_details)
    return json.dumps(items_details)