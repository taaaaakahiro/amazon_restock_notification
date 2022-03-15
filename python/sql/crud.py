import mysql.connector as mydb
import datetime

def connect():
    conn = mydb.connect(
        host='db',
        user='admin',
        password='admin',
        port='3306',
        database='amazonRestockBot',
    )
    # コネクションが切れた時に再接続してくれるよう設定
    conn.ping(reconnect=True)

    # 接続できているかどうか確認
    print(conn.is_connected())

    # DB操作用にカーソルを作成
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS merchandise")
    # テーブルを（すでにあればいったん消してから）作成
    sql = '''
    CREATE TABLE merchandise(
      id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
      asin_code VARCHAR(50) NULL,
      price INT(50) NULL,
      created_at DATE NULL,
      deleted_at DATE NUll
    )'''
    cur.execute(sql)


def tmp_connect():
    conn = mydb.connect(
        host='db',
        user='admin',
        password='admin',
        port='3306',
        database='amazonRestockBot',
    )
    return conn

def get_merchandise():
    conn = tmp_connect()
    cur = conn.cursor()
    try:
        cur.execute(
            'SELECT * FROM merchandise WHERE NOT NULL deleted_at'
        )
        data = cur.fetchall()
        return data

    except IndexError:
        return False


def add_merchandise(asin_code, price):
    conn = tmp_connect()
    cur = conn.cursor()
    try:
        cur.execute(
            'INSERT INTO merchandise (asin_code, price ) VALUES (%s, %s)',
            (asin_code, price)
        )
        return True

    except IndexError:
        return False

def del_merchandise(id):
    conn = tmp_connect()
    cur = conn.cursor()
    try:
        cur.execute(
            'UPDATE merchandise (deleted_at) VALUES (%s, %s)',
            (datetime.datetime.now())
        )
        return True

    except IndexError:
        return False