# -*- encoding: utf-8 -*-
"""
更新商品分类脚本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps import create_app, db
from apps.product.models import ProductCategory

app = create_app()

with app.app_context():
    # 先删除旧分类
    ProductCategory.query.delete()
    
    # 添加新分类
    categories = [
        {
            'parent_id': 0,
            'category_name': '鼻部护理',
            'category_code': 'nasal_care',
            'icon': '/static/images/category/nasal.png',
            'sort': 1,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '缓解疼痛',
            'category_code': 'pain_relief',
            'icon': '/static/images/category/pain.png',
            'sort': 2,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '护眼',
            'category_code': 'eye_care',
            'icon': '/static/images/category/eye.png',
            'sort': 3,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '调理亚健康',
            'category_code': 'sub_health',
            'icon': '/static/images/category/health.png',
            'sort': 4,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '固肾养肾',
            'category_code': 'kidney_care',
            'icon': '/static/images/category/kidney.png',
            'sort': 5,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '狐臭护理',
            'category_code': 'body_odor',
            'icon': '/static/images/category/odor.png',
            'sort': 6,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '美肤护肤',
            'category_code': 'skin_care',
            'icon': '/static/images/category/skin.png',
            'sort': 7,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '面瘫康复',
            'category_code': 'facial_rehab',
            'icon': '/static/images/category/facial.png',
            'sort': 8,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '女性调理',
            'category_code': 'women_health',
            'icon': '/static/images/category/women.png',
            'sort': 9,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '固体饮料',
            'category_code': 'solid_drink',
            'icon': '/static/images/category/drink.png',
            'sort': 10,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '压片糖果',
            'category_code': 'tablet_candy',
            'icon': '/static/images/category/candy.png',
            'sort': 11,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '膏滋',
            'category_code': 'herbal_paste',
            'icon': '/static/images/category/paste.png',
            'sort': 12,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '植物饮品',
            'category_code': 'herbal_drink',
            'icon': '/static/images/category/herbal.png',
            'sort': 13,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '配制酒',
            'category_code': 'prepared_wine',
            'icon': '/static/images/category/wine.png',
            'sort': 14,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '代用茶',
            'category_code': 'tea_substitute',
            'icon': '/static/images/category/tea.png',
            'sort': 15,
            'status': 1
        }
    ]
    
    for cat_data in categories:
        cat = ProductCategory(**cat_data)
        db.session.add(cat)
    
    db.session.commit()
    print('分类更新成功!')
    
    # 显示当前分类
    cats = ProductCategory.query.order_by(ProductCategory.sort).all()
    print(f'共 {len(cats)} 个分类:')
    for c in cats:
        print(f'  {c.sort}. {c.category_name} ({c.category_code})')
