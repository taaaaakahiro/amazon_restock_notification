# インストールした discord.py を読み込む
import discord
import requests
from bs4 import BeautifulSoup
from sql import crud
from dotenv import load_dotenv
import os

# 環境変数(.envファイル)読み込み
load_dotenv()

# 環境変数利用
TOKEN = os.getenv('TOKEN_DISCORD')

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理


@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    db = crud.MySQL(os.getenv('PYTHON_HOST'),os.getenv('PYTHON_USER'),os.getenv('PYTHON_PASSWORD'),os.getenv('PYTHON_PORT'),os.getenv('PYTHON_DATABASE'))
    db.connect()
    






# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/amazon_now」と発言したらamazonへ情報収集
    if message.content == '/amazon_now':
        uri = os.getenv('PYTHON_HOST') + "B07X41PNSM"
        ret = requests.get(uri)
        soup = BeautifulSoup(ret.content, "html.parser")
        get_price = soup.select(
            '#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span > span:nth-child(2) > span.a-price-whole')
        price = '価格表示が取得できませんでした。' if get_price == None else get_price[0].contents[0].replace(
            ",", "")

        is_add_button = soup.select('#add-to-cart-button')
        button = 'ボタンなし' if is_add_button == None else 'ボタンあり'

        await message.channel.send(price)
        await message.channel.send(button)

    if '!一覧' in message.content:
        rows = crud.get_merchandise()
        print(rows)
        for row in rows:
            id = str(row[0])
            asin_code = row[1]
            price = str(row[2])
            await message.channel.send('ID=' + id + ', 商品名:w, asincode='+ asin_code +', 価格='+ price)

    if '!登録' in message.content:
        tmp = message.content
        msg = tmp.split()
        try:
            msg[1], msg[2]
            asin_code = msg[1]
            price = msg[2]
            crud.add_merchandise(asin_code, price)
            await message.channel.send(crud.add_merchandise(asin_code, price))

        except IndexError:
            await message.channel.send('価格またはACINCODEを入力してください。')

    if '!削除' in message.content:
        tmp = message.content
        msg = tmp.split()
        try:
            msg[1]
            id = int(msg[1])
            await message.channel.send(crud.del_merchandise(id))

        except IndexError:
            await message.channel.send('IDを入力してください')

    if '!!初期DB作成' == message.content:
        crud.ini_connect()

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
