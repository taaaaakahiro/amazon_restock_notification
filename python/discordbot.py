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

# インスタンス化
db = crud.MySQL(os.getenv('PYTHON_HOST'),os.getenv('PYTHON_USER'),os.getenv('PYTHON_PASSWORD'),os.getenv('PYTHON_PORT'),os.getenv('PYTHON_DATABASE'))

@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    conn = db.connect() # 接続確認
    db.ini_connect() # テーブルが存在しなければ作成

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

    if '!一覧' == message.content[:3] and len(message.content) == 3:
        rows = db.get_merchandise()
        if rows == []:
            await message.channel.send('登録商品なし')
            return
        for row in rows:
            id = str(row[0])
            asin_code = row[1]
            price = str(row[2])
            name = str(row[3])
            await message.channel.send('ID=' + id + ', 商品名= '+ name +' , 価格='+ price, asincode='+ asin_code +')

    if '!登録' in message.content:
        tmp = message.content
        msg = tmp.split('/') #スペース区切り
        print(msg)
        try:
            msg[1], msg[2], msg[3]
            name = msg[1]
            price = msg[2]
            asin_code = msg[3]
            
            await message.channel.send(db.add_merchandise(asin_code, price, name))

        except IndexError:
            await message.channel.send('商品名、価格、ASINCODEを正しく入力してください。')

    if '!削除' in message.content:
        tmp = message.content
        msg = tmp.split('/')
        msg
        try:
            msg[1]
            id = int(msg[1])
            await message.channel.send(db.del_merchandise(id))

        except IndexError:
            await message.channel.send('IDを入力してください')

    if '!!初期DB作成' == message.content:
        db.ini_connect()

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
