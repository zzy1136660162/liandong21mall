# -*- encoding: utf-8 -*-
"""
商品商城模块 - 数据初始化脚本
运行此脚本初始化 sp_product_category 和 sp_product 表
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps import create_app, db
from apps.sp_mall.sp_models import SpProductCategory, SpProduct, SpOrder, SpOrderItem

app = create_app('apps.config.DevelopmentConfig')


def init_sp_categories():
    """初始化商品分类"""
    categories = [
        {'category_code': 'ELECTRONICS', 'category_name': '数码电子', 'icon': '', 'sort': 1, 'status': 1},
        {'category_code': 'CLOTHING', 'category_name': '服装鞋包', 'icon': '', 'sort': 2, 'status': 1},
        {'category_code': 'FOOD', 'category_name': '食品生鲜', 'icon': '', 'sort': 3, 'status': 1},
        {'category_code': 'HOME', 'category_name': '家居生活', 'icon': '', 'sort': 4, 'status': 1},
        {'category_code': 'COSMETICS', 'category_name': '美妆护肤', 'icon': '', 'sort': 5, 'status': 1},
        {'category_code': 'SPORTS', 'category_name': '运动户外', 'icon': '', 'sort': 6, 'status': 1},
        {'category_code': 'BOOKS', 'category_name': '图书文具', 'icon': '', 'sort': 7, 'status': 1},
        {'category_code': 'OTHER', 'category_name': '其他商品', 'icon': '', 'sort': 8, 'status': 1},
    ]
    
    with app.app_context():
        for cat_data in categories:
            existing = SpProductCategory.query.filter_by(category_code=cat_data['category_code']).first()
            if not existing:
                category = SpProductCategory(**cat_data)
                db.session.add(category)
        
        db.session.commit()
        print('✓ 商品分类初始化完成')


def init_demo_products():
    """初始化示例商品"""
    products = [
        {
            'category_code': 'ELECTRONICS',
            'products': [
                {
                    'product_code': 'ELEC001',
                    'product_name': 'iPhone 15 Pro Max 256GB',
                    'main_image': 'https://via.placeholder.com/400x400/333333/FFFFFF?text=iPhone+15',
                    'price': 9999.00,
                    'original_price': 10999.00,
                    'member_price': 9499.00,
                    'stock': 100,
                    'sales': 50,
                    'brief': '全新iPhone 15 Pro Max，钛金属设计，A17 Pro芯片',
                    'is_hot': 1,
                    'is_new': 1,
                    'is_recommend': 1
                },
                {
                    'product_code': 'ELEC002',
                    'product_name': 'AirPods Pro 2',
                    'main_image': 'https://via.placeholder.com/400x400/333333/FFFFFF?text=AirPods',
                    'price': 1899.00,
                    'original_price': 1999.00,
                    'member_price': 1799.00,
                    'stock': 200,
                    'sales': 120,
                    'brief': '全新升级的主动降噪功能',
                    'is_hot': 1,
                    'is_new': 0,
                    'is_recommend': 1
                }
            ]
        },
        {
            'category_code': 'CLOTHING',
            'products': [
                {
                    'product_code': 'CLOTH001',
                    'product_name': '男士纯棉休闲T恤',
                    'main_image': 'https://via.placeholder.com/400x400/4A90E2/FFFFFF?text=T-Shirt',
                    'price': 99.00,
                    'original_price': 199.00,
                    'member_price': 89.00,
                    'stock': 500,
                    'sales': 300,
                    'brief': '舒适纯棉面料，多色可选',
                    'is_hot': 0,
                    'is_new': 1,
                    'is_recommend': 0
                }
            ]
        },
        {
            'category_code': 'FOOD',
            'products': [
                {
                    'product_code': 'FOOD001',
                    'product_name': '新鲜有机红富士苹果 5斤装',
                    'main_image': 'https://via.placeholder.com/400x400/E24A4A/FFFFFF?text=Apple',
                    'price': 49.90,
                    'original_price': 69.90,
                    'member_price': 39.90,
                    'stock': 1000,
                    'sales': 800,
                    'brief': '产自甘肃静宁的有机红富士，口感脆甜',
                    'is_hot': 1,
                    'is_new': 0,
                    'is_recommend': 1
                }
            ]
        }
    ]
    
    with app.app_context():
        for cat_data in products:
            category = SpProductCategory.query.filter_by(category_code=cat_data['category_code']).first()
            if not category:
                print(f'⚠ 分类 {cat_data["category_code"]} 不存在，跳过')
                continue
            
            for prod_data in cat_data['products']:
                existing = SpProduct.query.filter_by(product_code=prod_data['product_code']).first()
                if not existing:
                    product = SpProduct(
                        category_id=category.id,
                        **prod_data
                    )
                    db.session.add(product)
        
        db.session.commit()
        print('✓ 示例商品初始化完成')


def init_demo_orders():
    """初始化示例订单"""
    import random
    from datetime import datetime, timedelta
    
    statuses = ['PENDING_PAY', 'PAID', 'SHIPPED', 'FINISHED', 'CANCELLED']
    
    with app.app_context():
        products = SpProduct.query.limit(5).all()
        if not products:
            print('⚠ 没有商品数据，跳过订单初始化')
            return
        
        for i in range(1, 6):
            order = SpOrder(
                order_no=f'SP{datetime.now().strftime("%Y%m%d")}{i:04d}',
                user_id=1000 + i,
                total_amount=199.00 + i * 10,
                discount_amount=10.00,
                pay_amount=189.00 + i * 10,
                freight_amount=0.00,
                receiver_name=f'张{i}',
                receiver_phone=f'138{i:08d}',
                receiver_province='北京市',
                receiver_city='北京市',
                receiver_district='朝阳区',
                receiver_address=f'建国路{i}号',
                status=random.choice(statuses),
                created_at=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            
            if order.status == 'PAID':
                order.pay_time = order.created_at + timedelta(hours=1)
            elif order.status == 'SHIPPED':
                order.pay_time = order.created_at + timedelta(hours=1)
                order.ship_time = order.created_at + timedelta(days=1)
            elif order.status == 'FINISHED':
                order.pay_time = order.created_at + timedelta(hours=1)
                order.ship_time = order.created_at + timedelta(days=1)
                order.finish_time = order.created_at + timedelta(days=3)
            
            db.session.add(order)
            db.session.flush()
            
            for j in range(random.randint(1, 3)):
                product = random.choice(products)
                item = SpOrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.product_name,
                    product_image=product.main_image,
                    price=product.price,
                    member_price=product.member_price,
                    quantity=random.randint(1, 3),
                    total_amount=product.price * random.randint(1, 3)
                )
                db.session.add(item)
        
        db.session.commit()
        print('✓ 示例订单初始化完成')


def run():
    """运行所有初始化"""
    print('开始初始化商品商城模块数据...')
    print('=' * 50)
    
    init_sp_categories()
    init_demo_products()
    init_demo_orders()
    
    print('=' * 50)
    print('数据初始化完成！')


if __name__ == '__main__':
    run()
