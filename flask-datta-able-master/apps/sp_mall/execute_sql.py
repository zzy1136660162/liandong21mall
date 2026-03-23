# -*- encoding: utf-8 -*-
"""
执行 SQL 文件创建 sp_mall 模块数据库表
"""

import pymysql
import os

# 数据库配置
DB_CONFIG = {
    'host': '101.126.90.255',
    'port': 63306,
    'user': 'root',
    'password': 'Gesoft9919.',
    'database': 'liandong21mall',
    'charset': 'utf8mb4'
}

def execute_sql_file():
    """执行 SQL 文件"""
    
    # 获取 SQL 文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file_path = os.path.join(current_dir, 'sql', 'sp_mall_module.sql')
    
    print(f'SQL 文件路径: {sql_file_path}')
    
    # 读取 SQL 文件
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 连接数据库
    connection = pymysql.connect(**DB_CONFIG)
    
    try:
        with connection.cursor() as cursor:
            # 分割 SQL 语句
            sql_statements = sql_content.split(';')
            
            for statement in sql_statements:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        cursor.execute(statement)
                        print(f'✓ 执行成功: {statement[:50]}...')
                    except Exception as e:
                        print(f'✗ 执行失败: {statement[:50]}...')
                        print(f'  错误: {e}')
            
            connection.commit()
            print('\n✓ SQL 文件执行完成！')
            
    except Exception as e:
        print(f'✗ 数据库操作失败: {e}')
        connection.rollback()
    finally:
        connection.close()

if __name__ == '__main__':
    execute_sql_file()
