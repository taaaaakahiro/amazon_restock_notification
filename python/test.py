import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('WEB_HOOK') #ここにWebhook用に取得したURLを入れる

payload = {'content': [111,222,333]}
result = requests.post(url, data=payload)
