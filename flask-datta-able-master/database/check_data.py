#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查数据库中的中文数据
"""

import pymysql

# 数据库配置
DB_HOST = '101.126.90.255'
DB_PORT = 63306
DB_USER = 'root'
DB_PASS = 'Gesoft9919.'
DB_NAME = 'liandong21mall'

def check_data():
    """查询数据"""
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
            cursor.execute("SELECT id, demand_no, title, target_audience, submitter_name FROM rd_demand ORDER BY id DESC LIMIT 5")
            results = cursor.fetchall()
            
            print("数据库中的数据：")
            print("-" * 80)
            for row in results:
                print(f"ID: {row[0]}")
                print(f"需求编号: {row[1]}")
                print(f"标题: {row[2]}")
                print(f"目标人群: {row[3]}")
                print(f"提交人: {row[4]}")
                print("-" * 80)
        
    except Exception as e:
        print(f"查询失败: {str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    check_data()
