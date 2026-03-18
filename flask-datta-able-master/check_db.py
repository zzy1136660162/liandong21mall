import pymysql

connection = pymysql.connect(
    host='101.126.90.255',
    port=63306,
    user='root',
    password='Gesoft9919.',
    database='liandong21mall',
    charset='utf8mb4'
)

cursor = connection.cursor()

cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

print('数据库中的表：')
for table in tables:
    print(f'  - {table[0]}')

print('\nproduct_category 表结构：')
cursor.execute("DESCRIBE product_category")
columns = cursor.fetchall()
for column in columns:
    print(f'  {column[0]} - {column[1]}')

print('\nproduct 表结构：')
cursor.execute("DESCRIBE product")
columns = cursor.fetchall()
for column in columns:
    print(f'  {column[0]} - {column[1]}')

print('\nproduct_category 表数据：')
cursor.execute("SELECT * FROM product_category LIMIT 5")
rows = cursor.fetchall()
for row in rows:
    print(f'  {row}')

cursor.close()
connection.close()
