# -*- encoding: utf-8 -*-
"""
执行SQL脚本更新订单表
"""

import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(os.path.dirname(basedir), '.env')
load_dotenv(env_path)

def execute_sql_file():
    """执行SQL文件"""
    
    # 数据库连接配置
    db_config = {
        'host': os.getenv('DB_HOST', '101.126.90.255'),
        'port': int(os.getenv('DB_PORT', 63306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASS', 'Gesoft9919.'),
        'database': os.getenv('DB_NAME', 'liandong21mall'),
        'charset': 'utf8mb4'
    }
    
    print("="*70)
    print("开始更新订单表字段...")
    print("="*70)
    print(f"数据库: {db_config['host']}:{db_config['port']}/{db_config['database']}")
    
    try:
        # 连接数据库
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        
        # 读取SQL文件
        sql_file = os.path.join(os.path.dirname(__file__), 'update_order_fields.sql')
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 分割SQL语句（按分号分割）
        sql_statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
        
        print(f"\n找到 {len(sql_statements)} 条SQL语句")
        
        # 执行每条SQL语句
        success_count = 0
        for i, sql in enumerate(sql_statements, 1):
            try:
                print(f"\n[{i}/{len(sql_statements)}] 执行: {sql[:50]}...")
                cursor.execute(sql)
                connection.commit()
                success_count += 1
                print(f"  ✅ 执行成功")
            except pymysql.MySQLError as e:
                error_code = e.args[0]
                if error_code == 1061:  # 索引已存在
                    print(f"  ⚠️ 索引已存在，跳过")
                    connection.rollback()
                elif error_code == 1060:  # 字段已存在
                    print(f"  ⚠️ 字段已存在，跳过")
                    connection.rollback()
                else:
                    print(f"  ❌ 执行失败: {e}")
                    connection.rollback()
        
        print("\n" + "="*70)
        print(f"更新完成! 成功执行 {success_count}/{len(sql_statements)} 条语句")
        print("="*70)
        
        # 验证更新
        print("\n验证订单表字段...")
        cursor.execute("DESCRIBE sp_order")
        columns = cursor.fetchall()
        print(f"订单表当前有 {len(columns)} 个字段:")
        for col in columns:
            print(f"  - {col[0]} ({col[1]})")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ 执行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = execute_sql_file()
    exit(0 if success else 1)
