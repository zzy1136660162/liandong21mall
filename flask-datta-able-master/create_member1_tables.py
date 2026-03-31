# -*- encoding: utf-8 -*-
"""
创建成员1负责的数据库表
商品商城模块：商品分类、商品、SKU、购物车、订单、订单项、地址
"""

from apps import create_app, db
from apps.sp_mall.sp_models import (
    SpProductCategory, SpProduct, SpProductSku, 
    SpCart, SpOrder, SpOrderItem, SpAddress,
    init_sp_product_categories
)
from apps.config import config_dict

app = create_app(config_dict['Debug'])

with app.app_context():
    print("开始创建成员1负责的数据库表...")
    
    try:
        # 创建所有表
        db.create_all()
        print("✓ 所有表创建成功")
        
        # 初始化商品分类数据
        try:
            init_sp_product_categories()
            print("✓ 商品分类数据初始化成功")
        except Exception as e:
            print(f"✗ 商品分类数据初始化失败: {e}")
        
        # 验证表是否创建成功
        tables_to_check = [
            ('sp_product_category', SpProductCategory),
            ('sp_product', SpProduct),
            ('sp_product_sku', SpProductSku),
            ('sp_cart', SpCart),
            ('sp_order', SpOrder),
            ('sp_order_item', SpOrderItem),
            ('sp_address', SpAddress)
        ]
        
        print("\n验证表创建状态:")
        for table_name, model in tables_to_check:
            try:
                count = model.query.count()
                print(f"✓ {table_name} - 表存在，当前记录数: {count}")
            except Exception as e:
                print(f"✗ {table_name} - 表不存在或访问失败: {e}")
        
        print("\n数据库表创建完成！")
        print("现在您可以在 Navicat 中看到这些表了。")
        
    except Exception as e:
        print(f"✗ 创建表时发生错误: {e}")
        import traceback
        traceback.print_exc()