# インストールした discord.py を読み込む
import discord
import requests
from bs4 import BeautifulSoup
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
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/amazon_now':
        uri = "https://www.amazon.co.jp/gp/offer-listing/4873117380/"
        ret = requests.get(uri)
        await message.channel.send('にゃーん')
        soup = BeautifulSoup(ret.content,"lxml")
        soup.find('div', {'class':'a-row a-spacing-mini olpOffer'})
        
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)   