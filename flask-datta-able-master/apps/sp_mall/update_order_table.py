# -*- encoding: utf-8 -*-
"""
订单表结构更新脚本
为sp_order表添加缺失的字段
"""

from apps import create_app, db
from apps.sp_mall.sp_models import SpOrder
from apps.config import Config
import sys

def update_order_table():
    """更新订单表结构"""
    app = create_app(Config)
    
    with app.app_context():
        try:
            # 检查现有字段
            print("开始检查订单表结构...")
            
            # 获取表信息
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('sp_order')]
            print(f"当前订单表字段: {columns}")
            
            # 需要添加的新字段
            new_columns = {
                'payment_method': 'ALTER TABLE sp_order ADD COLUMN payment_method VARCHAR(20) NULL COMMENT "支付方式"',
                'logistics_company': 'ALTER TABLE sp_order ADD COLUMN logistics_company VARCHAR(50) NULL COMMENT "物流公司"',
                'logistics_no': 'ALTER TABLE sp_order ADD COLUMN logistics_no VARCHAR(50) NULL COMMENT "物流单号"',
                'invoice_type': 'ALTER TABLE sp_order ADD COLUMN invoice_type VARCHAR(20) NULL COMMENT "发票类型"',
                'invoice_title': 'ALTER TABLE sp_order ADD COLUMN invoice_title VARCHAR(100) NULL COMMENT "发票抬头"',
                'order_source': "ALTER TABLE sp_order ADD COLUMN order_source VARCHAR(20) DEFAULT 'MINI_APP' COMMENT '订单来源'",
                'coupon_id': 'ALTER TABLE sp_order ADD COLUMN coupon_id BIGINT NULL COMMENT "使用的优惠券ID"',
                'coupon_amount': 'ALTER TABLE sp_order ADD COLUMN coupon_amount DECIMAL(10, 2) DEFAULT 0.00 COMMENT "优惠券金额"'
            }
            
            # 添加缺失的字段
            for col_name, alter_sql in new_columns.items():
                if col_name not in columns:
                    print(f"添加字段: {col_name}")
                    db.session.execute(db.text(alter_sql))
                else:
                    print(f"字段已存在: {col_name}")
            
            db.session.commit()
            print("订单表结构更新完成!")
            
            # 验证更新后的字段
            columns = [col['name'] for col in inspector.get_columns('sp_order')]
            print(f"更新后订单表字段: {columns}")
            
            # 检查索引
            indexes = inspector.get_indexes('sp_order')
            print(f"当前索引: {[idx['name'] for idx in indexes]}")
            
            # 添加缺失的索引
            index_columns_list = [idx['column_names'] for idx in indexes]
            
            if ['user_id'] not in index_columns_list:
                print("添加索引: idx_user_status")
                db.session.execute(db.text('CREATE INDEX idx_user_status ON sp_order (user_id, status)'))
            
            if ['created_at'] not in index_columns_list:
                print("添加索引: idx_user_created")
                db.session.execute(db.text('CREATE INDEX idx_user_created ON sp_order (user_id, created_at)'))
            
            db.session.commit()
            print("索引更新完成!")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"更新失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = update_order_table()
    sys.exit(0 if success else 1)
