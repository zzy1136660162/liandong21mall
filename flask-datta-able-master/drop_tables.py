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

tables_to_drop = [
    'order_item',
    'cart',
    'product_sku',
    'product',
    'product_category'
]

for table in tables_to_drop:
    try:
        cursor.execute(f'DROP TABLE IF EXISTS `{table}`')
        print(f'删除表: {table}')
    except Exception as e:
        print(f'删除表失败 {table}: {e}')

connection.commit()
cursor.close()
connection.close()

print('旧表删除完成！')
