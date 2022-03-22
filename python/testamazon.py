import requests
from bs4 import BeautifulSoup
import os
import sys

# requestテスト用
# 
# 

uri = 'https://www.amazon.co.jp/dp/B07B9HR5CR'
print(uri)
ret = requests.get(uri)
soup = BeautifulSoup(ret.content, "html.parser")

get_price = soup.select(
    '#corePrice_feature_div > div > span > span.a-offscreen'
)

is_add_button = soup.select('#add-to-cart-button')

print (get_price)
print (is_add_button)
if (get_price != []):
    get_price[0].contents[0]
    amazon_price = get_price[0].contents[0].replace(",", "")
    print(amazon_price)

else:
    print('取得できず')
