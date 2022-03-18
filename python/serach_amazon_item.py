import requests
from bs4 import BeautifulSoup
from sql import crud
from dotenv import load_dotenv
import os
import sys

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
    get_price = soup.select(
        '#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span > span:nth-child(2) > span.a-price-whole'
    )
    print(uri)
    try:
      get_price[0].contents[0]
      amazon_price =  get_price[0].contents[0].replace(",", "")
    except IndexError:
      print(get_price)
      amazon_price = 999999999999
    is_add_button = soup.select('#add-to-cart-button')
    button = False if is_add_button == None else True

    if (price > amazon_price and button):
        data = name + "が価格が下がってます\r"
        payload = {
            "username": "amazon巡回マン",
            "avatar_url": "https://github.com/qiita.png",
            "content": data
        }
        result = requests.post(hook_url, data=payload)
