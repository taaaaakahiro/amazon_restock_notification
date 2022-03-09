# インストールした discord.py を読み込む
import discord
import requests
from bs4 import BeautifulSoup
from sql import crud

# TOKEN
TOKEN = 'OTUwNzMwNzAyNTYxODczOTMx.YidK9w.mDA7lovwrRhQ5rzRCJbH9-Dctbw'

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/amazon_now」と発言したらamazonへ情報収集
    if message.content == '/amazon_now':
        uri = "https://www.amazon.co.jp/gp/offer-listing/4873117380/"
        ret = requests.get(uri)
        soup = BeautifulSoup(ret.content,"lxml")
        log = soup.find('a', {'class':'nav_a'})
        await message.channel.send(log)
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)   