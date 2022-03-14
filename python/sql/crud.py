import mysql.connector as mydb

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
  # id, name, priceを持つテーブルを（すでにあればいったん消してから）作成
  sql = '''
    CREATE TABLE merchandise(
       id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
       asin_code VARCHAR(50) NULL,
       price INT(50) NULL,
       created_at DATE NULL,
       deleted_at DATE NUll
    )'''
  cur.execute(sql)
    

connect()


