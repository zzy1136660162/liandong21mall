#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清理乱码的测试数据
"""

import pymysql

# 数据库配置
DB_HOST = '101.126.90.255'
DB_PORT = 63306
DB_USER = 'root'
DB_PASS = 'Gesoft9919.'
DB_NAME = 'liandong21mall'

def cleanup_data():
    """清理乱码数据"""
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
            # 先查看所有数据
            cursor.execute("SELECT id, demand_no, title, submitter_id FROM rd_demand ORDER BY id")
            results = cursor.fetchall()
            
            print("当前数据：")
            print("-" * 80)
            for row in results:
                print(f"ID: {row[0]}, 编号: {row[1]}, 标题: {row[2]}, 提交人: {row[3]}")
            print("-" * 80)
            
            # 删除乱码数据（ID 1 和 2）
            print("\n正在删除 ID 1 和 2 的乱码数据...")
            cursor.execute("DELETE FROM rd_demand_progress WHERE demand_id IN (1, 2)")
            cursor.execute("DELETE FROM rd_demand WHERE id IN (1, 2)")
            conn.commit()
            print("✅ 删除完成！")
            
            # 查看剩余数据
            cursor.execute("SELECT id, demand_no, title, submitter_id FROM rd_demand ORDER BY id")
            results = cursor.fetchall()
            
            print("\n剩余数据：")
            print("-" * 80)
            for row in results:
                print(f"ID: {row[0]}, 编号: {row[1]}, 标题: {row[2]}, 提交人: {row[3]}")
            print("-" * 80)
        
    except Exception as e:
        print(f"\n❌ 操作失败: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    cleanup_data()
