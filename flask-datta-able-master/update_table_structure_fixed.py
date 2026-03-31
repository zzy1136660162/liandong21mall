# -*- encoding: utf-8 -*-
"""
更新成员1负责的数据库表结构 - 修正版
根据小程序实际使用字段添加新字段
"""

from apps import create_app, db
from apps.config import config_dict

app = create_app(config_dict['Debug'])

def update_table_structure():
    """更新表结构，添加新字段"""
    
    with app.app_context():
        print("=" * 60)
        print("开始更新数据库表结构")
        print("=" * 60)
        
        # 商品表需要添加的字段（不使用AFTER，直接添加到末尾）
        product_updates = [
            # 佣金相关
            ("ALTER TABLE sp_product ADD COLUMN commission_rate DECIMAL(4,2) DEFAULT 10.00 COMMENT '佣金比例'", "commission_rate"),
            ("ALTER TABLE sp_product ADD COLUMN commission_amount DECIMAL(10,2) DEFAULT NULL COMMENT '佣金金额'", "commission_amount"),
            
            # 评价相关
            ("ALTER TABLE sp_product ADD COLUMN review_count INT DEFAULT 0 COMMENT '评价数量'", "review_count"),
            ("ALTER TABLE sp_product ADD COLUMN good_rate VARCHAR(10) DEFAULT NULL COMMENT '好评率'", "good_rate"),
            ("ALTER TABLE sp_product ADD COLUMN review_tags JSON DEFAULT NULL COMMENT '评价标签JSON'", "review_tags"),
            
            # 达人相关
            ("ALTER TABLE sp_product ADD COLUMN daren_count INT DEFAULT 0 COMMENT '达人数量'", "daren_count"),
            ("ALTER TABLE sp_product ADD COLUMN tuanzhang_name VARCHAR(100) DEFAULT NULL COMMENT '团长名称'", "tuanzhang_name"),
            ("ALTER TABLE sp_product ADD COLUMN tuanzhang_avatar VARCHAR(500) DEFAULT NULL COMMENT '团长头像'", "tuanzhang_avatar"),
            ("ALTER TABLE sp_product ADD COLUMN tuanzhang_desc VARCHAR(200) DEFAULT NULL COMMENT '团长描述'", "tuanzhang_desc")
        ]
        
        # 订单表需要添加的字段（已经添加过了，跳过）
        order_updates = []
        
        # 订单明细表需要添加的字段（已经添加过了，跳过）
        order_item_updates = []
        
        # 执行更新
        all_updates = [
            ("sp_product", product_updates),
            ("sp_order", order_updates),
            ("sp_order_item", order_item_updates)
        ]
        
        for table_name, updates in all_updates:
            if not updates:
                continue
                
            print(f"\n更新表: {table_name}")
            print("-" * 60)
            
            for sql, field_name in updates:
                try:
                    db.session.execute(db.text(sql))
                    db.session.commit()
                    print(f"✓ 添加字段: {field_name}")
                except Exception as e:
                    error_msg = str(e)
                    if "Duplicate column name" in error_msg:
                        print(f"○ 字段已存在: {field_name}")
                    else:
                        print(f"✗ 添加字段失败: {field_name} - {error_msg}")
                    db.session.rollback()
        
        print("\n" + "=" * 60)
        print("表结构更新完成！")
        print("=" * 60)
        
        # 验证更新结果
        print("\n验证更新结果:")
        print("-" * 60)
        
        # 检查商品表字段
        result = db.session.execute(db.text("DESCRIBE sp_product"))
        product_fields = [row[0] for row in result.fetchall()]
        
        important_fields = [
            'commission_rate', 'commission_amount', 'review_count', 'good_rate',
            'review_tags', 'daren_count', 'tuanzhang_name', 'tuanzhang_avatar',
            'tuanzhang_desc'
        ]
        
        print("\nsp_product 表关键字段:")
        for field in important_fields:
            status = "✓" if field in product_fields else "✗"
            print(f"  {status} {field}")
        
        # 检查订单表字段
        result = db.session.execute(db.text("DESCRIBE sp_order"))
        order_fields = [row[0] for row in result.fetchall()]
        
        order_important_fields = ['final_amount', 'remaining_seconds']
        
        print("\nsp_order 表关键字段:")
        for field in order_important_fields:
            status = "✓" if field in order_fields else "✗"
            print(f"  {status} {field}")
        
        # 检查订单明细表字段
        result = db.session.execute(db.text("DESCRIBE sp_order_item"))
        order_item_fields = [row[0] for row in result.fetchall()]
        
        order_item_important_fields = ['specs']
        
        print("\nsp_order_item 表关键字段:")
        for field in order_item_important_fields:
            status = "✓" if field in order_item_fields else "✗"
            print(f"  {status} {field}")
        
        # 显示完整的更新后表结构
        print("\n" + "=" * 60)
        print("更新后的完整表结构")
        print("=" * 60)
        
        print("\nsp_product 完整字段列表:")
        print("-" * 60)
        result = db.session.execute(db.text("DESCRIBE sp_product"))
        for row in result.fetchall():
            print(f"  {row[0]:25s} {row[1]:20s} {row[2]:10s}")

if __name__ == "__main__":
    update_table_structure()