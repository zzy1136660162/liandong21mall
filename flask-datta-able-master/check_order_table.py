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

print('order 表结构：')
cursor.execute("DESCRIBE `order`")
columns = cursor.fetchall()
for column in columns:
    print(f'  {column[0]} - {column[1]}')

print('\nproduct_sku 表结构：')
cursor.execute("DESCRIBE product_sku")
columns = cursor.fetchall()
for column in columns:
    print(f'  {column[0]} - {column[1]}')

cursor.close()
connection.close()
