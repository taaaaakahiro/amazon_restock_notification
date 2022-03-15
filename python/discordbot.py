# インストールした discord.py を読み込む
import discord
import requests
from bs4 import BeautifulSoup
from sql import crud
# from sql import crud

# TOKEN
TOKEN = 'OTUwNzMwNzAyNTYxODczOTMx.YidK9w.mDA7lovwrRhQ5rzRCJbH9-Dctbw'

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    crud.connect()
    

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/amazon_now」と発言したらamazonへ情報収集
    if message.content == '/amazon_now':
        uri = "https://www.amazon.co.jp/dp/B07X41PNSM"
        ret = requests.get(uri)
        soup = BeautifulSoup(ret.content,"html.parser")
        get_price = soup.select('#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span > span:nth-child(2) > span.a-price-whole')
        price = '価格表示が取得できませんでした。' if get_price == None else  get_price[0].contents[0].replace(",","")

        is_add_button = soup.select('#add-to-cart-button')
        button = 'ボタンなし'  if is_add_button == None else 'ボタンあり' 

        await message.channel.send(price)
        await message.channel.send(button)
    
    if '!一覧' in message.content:
        await message.channel.send('一覧を表示')

    if '!登録' in message.content:
        tmp = message.content
        msg = tmp.split()
        try:
            msg[1],msg[2]
            await message.channel.send(msg[1]+'と'+msg[2]+'が登録されました')
        except IndexError:
            await message.channel.send('価格またはACINCODEを入力してください。')

    if '!削除' in message.content:
        tmp = message.content
        msg = tmp.split()
        try:
            msg[1]
            await message.channel.send('番号:'+msg[1]+'が削除されました')
        except IndexError:
            await message.channel.send('IDを入力してください')


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)   
