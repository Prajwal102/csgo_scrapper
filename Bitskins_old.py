import pyotp
import requests
import json


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
        # 'item_wear': 'Battle-Scared'

    }

    item_wears = ['Factory New',  'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
    items_details = {
                    'source':'bitskins',
                    'conditions': {}
                    }

    bitskins_endpoint = "https://bitskins.com/api/v1/get_inventory_on_sale/"
    for wear in item_wears:
        items_details['conditions'][wear] = {}
        payload['item_wear'] = wear
        res = requests.get(bitskins_endpoint,params=payload)
        json_object = res.json()
        if json_object["data"]["items"]:
            first_res = json_object["data"]["items"][0]
            # first_res = json.dumps(json_object["data"]["items"][0],indent = 3)
            items_details['conditions'][wear]['price'] = '$'+first_res['price']
        else:
            items_details['conditions'][wear]['price'] = "NA"
        # items_details[wear]['url'] = res.url


    return json.dumps(items_details)