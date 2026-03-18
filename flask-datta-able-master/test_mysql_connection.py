import pymysql

try:
    print('尝试连接MySQL数据库...')
    connection = pymysql.connect(
        host='101.126.90.255',
        port=63306,
        user='root',
        password='Gesoft9919.',
        database='liandong21mall',
        charset='utf8mb4'
    )
    
    print('✓ MySQL连接成功！')
    
    cursor = connection.cursor()
    
    cursor.execute('SELECT VERSION()')
    version = cursor.fetchone()
    print(f'MySQL版本: {version[0]}')
    
    cursor.execute('SHOW TABLES')
    tables = cursor.fetchall()
    print(f'数据库表数量: {len(tables)}')
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f'✗ MySQL连接失败: {e}')
    print(f'错误类型: {type(e).__name__}')
