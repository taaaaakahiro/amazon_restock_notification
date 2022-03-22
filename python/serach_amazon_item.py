import requests
from bs4 import BeautifulSoup
from sql import crud
from dotenv import load_dotenv
import os
import sys
import time

load_dotenv()
db = crud.MySQL(
    os.getenv('PYTHON_HOST'),
    os.getenv('PYTHON_USER'),
    os.getenv('PYTHON_PASSWORD'),
    os.getenv('PYTHON_PORT'),
    os.getenv('PYTHON_DATABASE')
)
rows = db.get_merchandise()

load_dotenv()
hook_url = os.getenv('WEB_HOOK')  # ここにWebhook用に取得したURLを入れる

for row in rows:
    id = str(row[0])
    asin_code = row[1]
    price = str(row[2])
    name = str(row[3])

    uri = os.getenv('URI') + asin_code
    ret = requests.get(uri)
    soup = BeautifulSoup(ret.content, "html.parser")

    is_add_button = soup.select('#add-to-cart-button')
    button = False if is_add_button == None else True

    if button:
        get_price = soup.select(
            '#corePrice_feature_div > div > span > span.a-offscreen'
        )
        if (get_price != []):
            get_price[0].contents[0]
            amazon_price = get_price[0].contents[0].replace(",", "").replace("￥", "")
            print(uri)
            print(amazon_price)
        else:
            get_price = soup.select(
                '#corePrice_feature_div > div > span > span:nth-child(2) > span.a-price-whole'
            )
            try:
                amazon_price = get_price[0].contents[0].replace(",", "").replace("￥", "")
                print(amazon_price+'tryに入ってる')
                get_price[0].contents[0]

            except IndexError:
                amazon_price = 99999999
                print(uri)
                print(amazon_price)

        if (int(price) > int(amazon_price)):
            data = "[リストック通知] " + name + "\r" + uri
            payload = {
                "username": "amazon巡回マン",
                "avatar_url": "https://github.com/qiita.png",
                "content": data
            }
            result = requests.post(hook_url, data=payload)
        time.sleep(10)
