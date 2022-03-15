import mysql.connector as mydb

def connect():
    conn = mydb.connect(
        host='db',
        user='admin',
        password='admin',
        port='3306',
        database='amazonRestockBot',
    )
    conn.ping(reconnect=True)
    conn.autocommit = False
    return conn


def get_merchandise():
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id,asin_code,price FROM merchandise WHERE deleted_at IS NULL"
        )
        data = cur.fetchall()
        return data

    except IndexError:
        return False


def add_merchandise(asin_code, price):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO merchandise (asin_code, price, created_at ) VALUES (%s, %s, NOW())",
            (asin_code, price)
        )
        conn.commit()
        return True

    except IndexError:
        return False


def del_merchandise(id):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE merchandise SET deleted_at = NOW() WHERE id = %s",(id,)
            )
        conn.commit()
        return True

    except IndexError:
        return False

def ini_connect():
    
    conn = connect()
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