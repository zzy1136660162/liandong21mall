# -*- encoding: utf-8 -*-
"""
商品详情模块数据库初始化脚本
"""

import pymysql
import os
import sys

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from dotenv import load_dotenv

# 加载环境变量
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)


def get_db_config():
    """获取数据库配置"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USERNAME', 'root'),
        'password': os.getenv('DB_PASS', ''),
        'database': os.getenv('DB_NAME', 'liandong_mall')
    }


def execute_sql_file(file_path):
    """执行SQL文件"""
    config = get_db_config()
    
    connection = pymysql.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database'],
        charset='utf8mb4'
    )
    
    try:
        with connection.cursor() as cursor:
            with open(file_path, 'r', encoding='utf-8') as f:
                sql = f.read()
                
                statements = sql.split(';')
                for statement in statements:
                    statement = statement.strip()
                    if statement:
                        cursor.execute(statement)
                
        connection.commit()
        print(f'成功执行SQL文件: {file_path}')
    except Exception as e:
        connection.rollback()
        print(f'执行SQL文件失败: {e}')
    finally:
        connection.close()


def init_sp_product_detail_tables():
    """初始化商品详情数据库表"""
    sql_file = os.path.join(project_root, 'apps', 'sp_product', 'sql', 'sp_product_detail_module.sql')
    execute_sql_file(sql_file)


def init_sp_product_detail_demo_data():
    """初始化商品详情测试数据"""
    sql_file = os.path.join(project_root, 'apps', 'sp_product', 'sql', 'sp_product_detail_demo_data.sql')
    execute_sql_file(sql_file)


if __name__ == '__main__':
    print('开始初始化商品详情模块数据库...')
    init_sp_product_detail_tables()
    init_sp_product_detail_demo_data()
    print('商品详情模块数据库初始化完成！')
