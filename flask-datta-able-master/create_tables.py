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

with open('apps/product/sql/product_module.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

statements = [s.strip() for s in sql.split(';') if s.strip()]

for statement in statements:
    if statement:
        try:
            cursor.execute(statement)
            print(f'执行成功: {statement[:50]}...')
        except Exception as e:
            print(f'执行失败: {e}')
            print(f'SQL: {statement[:100]}...')

connection.commit()
cursor.close()
connection.close()

print('数据库表创建完成！')
