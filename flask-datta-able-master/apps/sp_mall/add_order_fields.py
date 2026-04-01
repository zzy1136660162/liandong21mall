# -*- encoding: utf-8 -*-
"""
直接添加订单表缺失字段
"""

import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(os.path.dirname(basedir), '.env')
load_dotenv(env_path)

def add_missing_fields():
    """添加缺失的字段"""
    
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
    print("开始添加订单表缺失字段...")
    print("="*70)
    
    try:
        # 连接数据库
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        
        # 定义要添加的字段
        fields_to_add = [
            {
                'name': 'payment_method',
                'type': "VARCHAR(50) DEFAULT 'WECHAT_PAY' COMMENT '支付方式'",
                'after': 'pay_time'
            },
            {
                'name': 'logistics_company',
                'type': "VARCHAR(100) COMMENT '物流公司'",
                'after': 'payment_method'
            },
            {
                'name': 'logistics_no',
                'type': "VARCHAR(100) COMMENT '物流单号'",
                'after': 'logistics_company'
            },
            {
                'name': 'invoice_type',
                'type': "VARCHAR(20) DEFAULT 'NONE' COMMENT '发票类型'",
                'after': 'logistics_no'
            },
            {
                'name': 'invoice_title',
                'type': "VARCHAR(200) COMMENT '发票抬头'",
                'after': 'invoice_type'
            },
            {
                'name': 'order_source',
                'type': "VARCHAR(20) DEFAULT 'MINIPROGRAM' COMMENT '订单来源'",
                'after': 'invoice_title'
            },
            {
                'name': 'coupon_id',
                'type': "INT COMMENT '优惠券ID'",
                'after': 'order_source'
            },
            {
                'name': 'coupon_amount',
                'type': "DECIMAL(10,2) DEFAULT 0.00 COMMENT '优惠券金额'",
                'after': 'coupon_id'
            }
        ]
        
        print(f"\n需要添加 {len(fields_to_add)} 个字段\n")
        
        # 添加每个字段
        success_count = 0
        for i, field in enumerate(fields_to_add, 1):
            sql = f"ALTER TABLE sp_order ADD COLUMN {field['name']} {field['type']} AFTER {field['after']}"
            try:
                print(f"[{i}/{len(fields_to_add)}] 添加字段 {field['name']}...")
                cursor.execute(sql)
                connection.commit()
                success_count += 1
                print(f"  ✅ 成功")
            except pymysql.MySQLError as e:
                error_code = e.args[0]
                if error_code == 1060:  # 字段已存在
                    print(f"  ⚠️ 字段已存在，跳过")
                    connection.rollback()
                else:
                    print(f"  ❌ 失败: {e}")
                    connection.rollback()
        
        print("\n" + "="*70)
        print(f"完成! 成功添加 {success_count}/{len(fields_to_add)} 个字段")
        print("="*70)
        
        # 验证更新
        print("\n验证订单表字段...")
        cursor.execute("DESCRIBE sp_order")
        columns = cursor.fetchall()
        print(f"订单表现在有 {len(columns)} 个字段:")
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
    success = add_missing_fields()
    exit(0 if success else 1)
