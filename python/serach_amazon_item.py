import requests
from bs4 import BeautifulSoup
from sql import crud
from dotenv import load_dotenv
import os

db = crud.MySQL(
    os.getenv('PYTHON_HOST'),
    os.getenv('PYTHON_USER'),
    os.getenv('PYTHON_PASSWORD'),
    os.getenv('PYTHON_PORT'),
    os.getenv('PYTHON_DATABASE')
)
rows = db.get_merchandise()

for row in rows:
    id = str(row[0])
    asin_code = row[1]
    price = str(row[2])
    name = str(row[3])

    uri = os.getenv('PYTHON_HOST') + asin_code
    ret = requests.get(uri)
    soup = BeautifulSoup(ret.content, "html.parser")
    get_price = soup.select(
        '#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span > span:nth-child(2) > span.a-price-whole')
    amazon_price = '価格表示が取得できませんでした。' if get_price == None else get_price[0].contents[0].replace(
        ",", "")

    is_add_button = soup.select('#add-to-cart-button')
    button = False if is_add_button == None else True

    if (price > amazon_price):
      print(name+'の商品が安くなっています')