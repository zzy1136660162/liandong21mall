# -*- encoding: utf-8 -*-
"""
快速诊断和修复数据库问题
"""

from apps import create_app, db
from apps.sp_mall.sp_models import (
    SpProductCategory, SpProduct, SpProductSku,
    SpCart, SpOrder, SpOrderItem, SpAddress
)
from apps.config import Config
import sys

def diagnose_and_fix():
    """诊断并修复数据库问题"""
    app = create_app(Config)
    
    with app.app_context():
        try:
            print("="*70)
            print("开始诊断数据库...")
            print("="*70)
            
            # 获取数据库引擎和检查器
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            print(f"\n当前数据库表: {len(existing_tables)}个")
            for table in existing_tables:
                print(f"  - {table}")
            
            # 检查必要的表
            required_tables = {
                'sp_product_category': SpProductCategory,
                'sp_product': SpProduct,
                'sp_product_sku': SpProductSku,
                'sp_cart': SpCart,
                'sp_order': SpOrder,
                'sp_order_item': SpOrderItem,
                'sp_address': SpAddress
            }
            
            print("\n" + "="*70)
            print("检查必要表...")
            print("="*70)
            
            missing_tables = []
            for table_name, model_class in required_tables.items():
                if table_name in existing_tables:
                    print(f"✅ 表 {table_name} 存在")
                    
                    # 检查列
                    columns = [col['name'] for col in inspector.get_columns(table_name)]
                    print(f"   字段: {', '.join(columns)}")
                    
                    # 检查索引
                    indexes = inspector.get_indexes(table_name)
                    if indexes:
                        print(f"   索引: {', '.join([idx['name'] for idx in indexes])}")
                else:
                    print(f"❌ 表 {table_name} 不存在")
                    missing_tables.append(table_name)
            
            if missing_tables:
                print("\n" + "="*70)
                print("创建缺失的表...")
                print("="*70)
                
                db.create_all()
                print("✅ 表创建完成")
            else:
                print("\n" + "="*70)
                print("检查订单表字段...")
                print("="*70)
                
                # 检查订单表是否有新字段
                order_columns = [col['name'] for col in inspector.get_columns('sp_order')]
                print(f"\n订单表当前字段: {len(order_columns)}个")
                
                required_order_fields = [
                    'payment_method', 'logistics_company', 'logistics_no',
                    'invoice_type', 'invoice_title', 'order_source',
                    'coupon_id', 'coupon_amount'
                ]
                
                missing_fields = [f for f in required_order_fields if f not in order_columns]
                
                if missing_fields:
                    print(f"❌ 缺失字段: {', '.join(missing_fields)}")
                    print("\n需要运行 update_order_table.py 来添加这些字段")
                else:
                    print("✅ 所有必需字段都存在")
            
            # 测试查询
            print("\n" + "="*70)
            print("测试数据库查询...")
            print("="*70)
            
            try:
                # 测试商品查询
                product_count = SpProduct.query.count()
                print(f"✅ 商品查询成功: {product_count}个商品")
            except Exception as e:
                print(f"❌ 商品查询失败: {str(e)}")
            
            try:
                # 测试订单查询
                order_count = SpOrder.query.count()
                print(f"✅ 订单查询成功: {order_count}个订单")
            except Exception as e:
                print(f"❌ 订单查询失败: {str(e)}")
            
            try:
                # 测试订单统计查询
                test_user_id = 1
                total_orders = SpOrder.query.filter_by(user_id=test_user_id).count()
                print(f"✅ 订单统计查询成功: 用户{test_user_id}有{total_orders}个订单")
            except Exception as e:
                print(f"❌ 订单统计查询失败: {str(e)}")
                import traceback
                traceback.print_exc()
            
            # 检查是否有测试数据
            print("\n" + "="*70)
            print("检查测试数据...")
            print("="*70)
            
            category_count = SpProductCategory.query.count()
            product_count = SpProduct.query.count()
            address_count = SpAddress.query.count()
            
            print(f"分类: {category_count}个")
            print(f"商品: {product_count}个")
            print(f"地址: {address_count}个")
            
            if category_count == 0:
                print("\n⚠️ 没有商品分类，正在添加...")
                init_sp_product_categories()
            
            if product_count == 0:
                print("\n⚠️ 没有商品数据")
                print("建议运行 init_sp_mall_tables.py 创建测试商品")
            
            if address_count == 0:
                print("\n⚠️ 没有收货地址")
                print("建议在小程序中添加收货地址")
            
            print("\n" + "="*70)
            print("诊断完成!")
            print("="*70)
            
            return True
            
        except Exception as e:
            print(f"\n❌ 诊断失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def init_sp_product_categories():
    """初始化商品分类"""
    categories = [
        {'category_name': '护肤', 'category_code': 'skincare', 'sort': 1},
        {'category_name': '彩妆', 'category_code': 'makeup', 'sort': 2},
        {'category_name': '个护', 'category_code': 'personal_care', 'sort': 3},
        {'category_name': '食品', 'category_code': 'food', 'sort': 4},
        {'category_name': '家居', 'category_code': 'home', 'sort': 5}
    ]
    
    for cat_data in categories:
        existing = SpProductCategory.query.filter_by(category_code=cat_data['category_code']).first()
        if not existing:
            category = SpProductCategory(**cat_data)
            db.session.add(category)
            print(f"  ✅ 添加分类: {cat_data['category_name']}")
    
    db.session.commit()

if __name__ == '__main__':
    success = diagnose_and_fix()
    sys.exit(0 if success else 1)
