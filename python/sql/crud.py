import mysql.connector as mydb

class MySQL:
  def __init__(self, host, user, password, port, database):
    self.host_mysql     = host
    self.user_mysql     = user
    self.password_mysql = password
    self.port_mysql     = port
    self.database_mysql = database

  def connect(self):
      conn = mydb.connect(
          host=self.host_mysql,
          user=self.user_mysql,
          password=self.password_mysql,
          port=self.port_mysql,
          database=self.database_mysql,
      )
      conn.ping(reconnect=True)
      conn.autocommit = False
      print("接続成功")
      return conn

  def get_merchandise(self):
      conn = mydb.connect(
          host=self.host_mysql,
          user=self.user_mysql,
          password=self.password_mysql,
          port=self.port_mysql,
          database=self.database_mysql,
      )
      cur = conn.cursor()
      try:
          cur.execute(
              "SELECT id,asin_code,price,name FROM merchandise WHERE deleted_at IS NULL"
          )
          data = cur.fetchall()
          return data

      except IndexError:
          return '商品が取得できませんでした'


  def add_merchandise(self, asin_code, price, name):
      conn = mydb.connect(
          host=self.host_mysql,
          user=self.user_mysql,
          password=self.password_mysql,
          port=self.port_mysql,
          database=self.database_mysql,
      )
      cur = conn.cursor()
      try:
          cur.execute(
              "INSERT INTO merchandise (asin_code, price, name, created_at ) VALUES (%s, %s, %s, NOW())",
              (asin_code, price, name)
          )
          conn.commit()
          return '登録が完了しました'

      except IndexError:
          return '入力値が不正です'

  def del_merchandise(self, id):
      # conn = connect()
      conn = mydb.connect(
          host=self.host_mysql,
          user=self.user_mysql,
          password=self.password_mysql,
          port=self.port_mysql,
          database=self.database_mysql,
      )
      cur = conn.cursor()
      try:
          cur.execute(
              "UPDATE merchandise SET deleted_at = NOW() WHERE id = %s",(id,)
              )
          conn.commit()
          return '削除しました'

      except IndexError:
          return False

  def ini_connect(self):
      conn = mydb.connect(
          host=self.host_mysql,
          user=self.user_mysql,
          password=self.password_mysql,
          port=self.port_mysql,
          database=self.database_mysql,
      )
      # コネクションが切れた時に再接続してくれるよう設定
      conn.ping(reconnect=True)

      # DB操作用にカーソルを作成
      cur = conn.cursor()
      # テーブルを（なければ）作成
      sql = '''
      CREATE TABLE IF NOT EXISTS merchandise(
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        asin_code VARCHAR(50) NOT NULL,
        name VARCHAR(255) NOT NULL,
        price INT(50) NOT NULl,
        created_at DATE NULL,
        deleted_at DATE NULL
      )'''
      cur.execute(sql)