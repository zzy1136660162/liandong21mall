import pymysql

try:
    connection = pymysql.connect(
        host='101.126.90.255',
        port=63306,
        user='root',
        password='Gesoft9919.',
        database='liandong21mall',
        charset='utf8mb4'
    )
    
    cursor = connection.cursor()
    
    cursor.execute('SHOW TABLES')
    tables = cursor.fetchall()
    
    print('数据库连接成功！')
    print('现有表：')
    for table in tables:
        print(f'  - {table[0]}')
    
    cursor.execute('DESCRIBE product')
    columns = cursor.fetchall()
    
    print('\nproduct表结构：')
    for column in columns:
        print(f'  - {column[0]} ({column[1]})')
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f'数据库连接失败：{e}')
