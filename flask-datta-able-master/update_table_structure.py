# -*- encoding: utf-8 -*-
"""
更新成员1负责的数据库表结构
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
        
        # 商品表需要添加的字段
        product_updates = [
            # 佣金相关
            ("ALTER TABLE sp_product ADD COLUMN commission_amount DECIMAL(10,2) DEFAULT NULL COMMENT '佣金金额' AFTER commission_rate", "commission_amount"),
            
            # 库存销售统计
            ("ALTER TABLE sp_product ADD COLUMN month_sales INT DEFAULT 0 COMMENT '月销量' AFTER sales", "month_sales"),
            ("ALTER TABLE sp_product ADD COLUMN month_views INT DEFAULT 0 COMMENT '月浏览量' AFTER month_sales", "month_views"),
            ("ALTER TABLE sp_product ADD COLUMN month_daren VARCHAR(20) DEFAULT NULL COMMENT '月达人数量' AFTER month_views", "month_daren"),
            
            # 评价相关
            ("ALTER TABLE sp_product ADD COLUMN good_rate VARCHAR(10) DEFAULT NULL COMMENT '好评率' AFTER review_count", "good_rate"),
            ("ALTER TABLE sp_product ADD COLUMN review_tags JSON DEFAULT NULL COMMENT '评价标签JSON' AFTER good_rate", "review_tags"),
            
            # 商品信息
            ("ALTER TABLE sp_product ADD COLUMN location VARCHAR(100) DEFAULT NULL COMMENT '发货地' AFTER description", "location"),
            
            # 店铺相关
            ("ALTER TABLE sp_product ADD COLUMN shop_name VARCHAR(100) DEFAULT NULL COMMENT '店铺名称' AFTER location", "shop_name"),
            ("ALTER TABLE sp_product ADD COLUMN shop_logo VARCHAR(500) DEFAULT NULL COMMENT '店铺logo' AFTER shop_name", "shop_logo"),
            ("ALTER TABLE sp_product ADD COLUMN shop_sales VARCHAR(20) DEFAULT NULL COMMENT '店铺销量' AFTER shop_logo", "shop_sales"),
            ("ALTER TABLE sp_product ADD COLUMN shop_score VARCHAR(10) DEFAULT NULL COMMENT '店铺评分' AFTER shop_sales", "shop_score"),
            ("ALTER TABLE sp_product ADD COLUMN product_score VARCHAR(10) DEFAULT NULL COMMENT '商品评分' AFTER shop_score", "product_score"),
            ("ALTER TABLE sp_product ADD COLUMN logistics_score VARCHAR(10) DEFAULT NULL COMMENT '物流评分' AFTER product_score", "logistics_score"),
            ("ALTER TABLE sp_product ADD COLUMN service_score VARCHAR(10) DEFAULT NULL COMMENT '服务评分' AFTER logistics_score", "service_score"),
            
            # 达人相关
            ("ALTER TABLE sp_product ADD COLUMN daren_count INT DEFAULT 0 COMMENT '达人数量' AFTER review_tags", "daren_count"),
            ("ALTER TABLE sp_product ADD COLUMN tuanzhang_name VARCHAR(100) DEFAULT NULL COMMENT '团长名称' AFTER daren_count", "tuanzhang_name"),
            ("ALTER TABLE sp_product ADD COLUMN tuanzhang_avatar VARCHAR(500) DEFAULT NULL COMMENT '团长头像' AFTER tuanzhang_name", "tuanzhang_avatar"),
            ("ALTER TABLE sp_product ADD COLUMN tuanzhang_desc VARCHAR(200) DEFAULT NULL COMMENT '团长描述' AFTER tuanzhang_avatar", "tuanzhang_desc"),
            
            # 标签
            ("ALTER TABLE sp_product ADD COLUMN tags JSON DEFAULT NULL COMMENT '商品标签JSON' AFTER is_recommend", "tags")
        ]
        
        # 订单表需要添加的字段
        order_updates = [
            ("ALTER TABLE sp_order ADD COLUMN final_amount DECIMAL(10,2) NOT NULL COMMENT '最终金额' AFTER pay_amount", "final_amount"),
            ("ALTER TABLE sp_order ADD COLUMN remaining_seconds INT DEFAULT NULL COMMENT '剩余支付秒数' AFTER remark", "remaining_seconds")
        ]
        
        # 订单明细表需要添加的字段
        order_item_updates = [
            ("ALTER TABLE sp_order_item ADD COLUMN specs VARCHAR(200) DEFAULT NULL COMMENT '规格描述' AFTER sku_name", "specs")
        ]
        
        # 执行更新
        all_updates = [
            ("sp_product", product_updates),
            ("sp_order", order_updates),
            ("sp_order_item", order_item_updates)
        ]
        
        for table_name, updates in all_updates:
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
            'commission_amount', 'month_sales', 'month_views', 'month_daren',
            'good_rate', 'review_tags', 'location', 'shop_name', 'shop_logo',
            'shop_sales', 'shop_score', 'product_score', 'logistics_score',
            'service_score', 'daren_count', 'tuanzhang_name', 'tuanzhang_avatar',
            'tuanzhang_desc', 'tags'
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

if __name__ == "__main__":
    update_table_structure()