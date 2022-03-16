import mysql.connector as mydb

class MySQL:
  def __init__(self, host, user, password, port, database):
    self.host_Mysql     = host
    self.user_Mysql     = user
    self.password_Mysql = password
    self.port_Mysql     = port
    self.database_Mysql = database

  def connect(self):
      conn = mydb.connect(
          host=self.host_Mysql,
          user=self.user_Mysql,
          password=self.password_Mysql,
          port=self.port_Mysql,
          database=self.database_Mysql,
      )
      conn.ping(reconnect=True)
      conn.autocommit = False
      print("接続成功")
      return conn


  def get_merchandise(self):
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


  def add_merchandise(self, asin_code, price):
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


  def del_merchandise(self, id):
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

  def ini_connect(self):
      
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