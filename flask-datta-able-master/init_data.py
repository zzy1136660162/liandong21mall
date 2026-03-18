#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
初始化数据库数据
"""
from apps import create_app, db
from apps.product.models import Product, Category
from apps.config import config_dict
import time

app = create_app(config_dict['Debug'])

with app.app_context():
    # 创建分类
    if Category.query.count() == 0:
        categories = [
            Category(name='数码家电', sort=1),
            Category(name='服装鞋包', sort=2),
            Category(name='美妆护肤', sort=3),
            Category(name='食品饮料', sort=4),
            Category(name='家居日用', sort=5),
        ]
        for cat in categories:
            db.session.add(cat)
        db.session.commit()
        print('分类创建成功!')
    
    # 创建商品
    if Product.query.count() == 0:
        current_time = time.strftime('%Y%m%d%H%M%S')
        products = [
            Product(
                product_no=f'P{current_time}001',
                name='iPhone 15 Pro Max',
                subtitle='苹果最新旗舰手机',
                category_id=1,
                main_image='https://example.com/iphone15.jpg',
                price=9999.00,
                original_price=10999.00,
                supply_price=8000.00,
                stock=100,
                sales=50,
                status=1,
                commission_rate=5,
                is_hot=True,
                is_recommend=True
            ),
            Product(
                product_no=f'P{current_time}002',
                name='小米14 Ultra',
                subtitle='徕卡影像旗舰',
                category_id=1,
                main_image='https://example.com/mi14.jpg',
                price=5999.00,
                original_price=6499.00,
                supply_price=4500.00,
                stock=200,
                sales=120,
                status=1,
                commission_rate=8,
                is_hot=True
            ),
            Product(
                product_no=f'P{current_time}003',
                name='SK-II神仙水',
                subtitle='护肤精华露',
                category_id=3,
                main_image='https://example.com/sk2.jpg',
                price=1540.00,
                supply_price=1000.00,
                stock=50,
                sales=30,
                status=1,
                commission_rate=10,
                is_recommend=True
            ),
        ]
        for p in products:
            db.session.add(p)
        db.session.commit()
        print(f'创建了 {len(products)} 个商品!')
    
    print(f'当前商品总数: {Product.query.count()}')
    print(f'当前分类总数: {Category.query.count()}')
