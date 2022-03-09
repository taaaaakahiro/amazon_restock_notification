import psycopg2

def get_connection():
  username = 'root'
  password = 'admin'
  database = 'amazonRestockBot'
  hostname = 'db'
  port = 5432
  dburl = f'postgresql://{username}:{password}@{hostname}:{port}/{database}'
  conn = psycopg2.connect(dburl)
  print(1111)
  return conn

# id, name, priceを持つテーブルを（すでにあればいったん消してから）作成
# table = 'test_table'
# cur.execute("DROP TABLE IF EXISTS `%s`;", table)
# cur.execute(
#     """
#     CREATE TABLE IF NOT EXISTS `%s` (
#     `id` int auto_increment primary key,
#     `name` varchar(50) not null,
#     `price` int(11) not null
#     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
#     """, table)

