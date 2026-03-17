#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
执行 SQL 脚本
"""

import pymysql
import os

# 数据库配置
DB_HOST = '101.126.90.255'
DB_PORT = 63306
DB_USER = 'root'
DB_PASS = 'Gesoft9919.'
DB_NAME = 'liandong21mall'

def execute_sql_file(file_path):
    """执行 SQL 文件"""
    # 读取 SQL 文件
    with open(file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 连接数据库
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        charset='utf8mb4'
    )
    
    try:
        with conn.cursor() as cursor:
            # 分割 SQL 语句（按分号分隔）
            statements = sql_content.split(';')
            
            for statement in statements:
                statement = statement.strip()
                if statement:
                    print(f"执行 SQL: {statement[:50]}...")
                    cursor.execute(statement)
                    conn.commit()
                    print("✓ 执行成功")
        
        print("\n✅ 所有 SQL 执行完成！")
        
    except Exception as e:
        print(f"\n❌ 执行失败: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    sql_file = os.path.join(os.path.dirname(__file__), 'recreate_tables.sql')
    print(f"正在执行 SQL 文件: {sql_file}\n")
    execute_sql_file(sql_file)
