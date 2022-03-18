import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('WEB_HOOK') #ここにWebhook用に取得したURLを入れる
data = ""
payload = {
  "username": "やましたえーいち",
  "avatar_url": "https://github.com/qiita.png",
  "content": "f{data}書き込めました\rいい感じ"
}
result = requests.post(url, data=payload)
