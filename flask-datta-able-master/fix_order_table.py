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

print('修复 order 表的 id 字段类型...')

try:
    cursor.execute("ALTER TABLE `order` MODIFY COLUMN id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT")
    print('✓ order 表的 id 字段已修改为 BIGINT UNSIGNED')
    
    connection.commit()
    print('✓ 修改成功！')
except Exception as e:
    print(f'✗ 修改失败: {e}')
    connection.rollback()

print('\n验证修改后的表结构：')
cursor.execute("DESCRIBE `order`")
columns = cursor.fetchall()
for column in columns:
    print(f'  {column[0]} - {column[1]}')

cursor.close()
connection.close()
