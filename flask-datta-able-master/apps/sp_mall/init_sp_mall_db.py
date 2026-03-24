# -*- encoding: utf-8 -*-
"""
初始化 sp_mall 模块数据库表
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from apps.config import config_dict
from apps import db
from apps.sp_mall.sp_models import (
    SpProductCategory, SpProduct, SpProductSku,
    SpCart, SpOrder, SpOrderItem, SpAddress
)

def init_sp_mall_tables():
    """初始化 sp_mall 模块数据库表"""
    app_config = config_dict['Debug']
    from apps import create_app
    app = create_app(app_config)
    
    with app.app_context():
        try:
            print('开始创建 sp_mall 模块数据库表...')
            
            db.create_all()
            print('✓ 数据库表创建成功')
            
            init_sp_product_categories()
            print('✓ 商品分类初始化成功')
            
            print('\nsp_mall 模块数据库初始化完成！')
            
        except Exception as e:
            print(f'✗ 数据库表创建失败: {e}')
            import traceback
            traceback.print_exc()

def init_sp_product_categories():
    """初始化商品分类数据"""
    categories = [
        {'parent_id': 0, 'category_name': '护肤', 'category_code': 'skincare', 'icon': '/static/images/category/skincare.png', 'sort': 1, 'status': 1},
        {'parent_id': 0, 'category_name': '彩妆', 'category_code': 'makeup', 'icon': '/static/images/category/makeup.png', 'sort': 2, 'status': 1},
        {'parent_id': 0, 'category_name': '个护', 'category_code': 'personal_care', 'icon': '/static/images/category/personal_care.png', 'sort': 3, 'status': 1},
        {'parent_id': 0, 'category_name': '食品', 'category_code': 'food', 'icon': '/static/images/category/food.png', 'sort': 4, 'status': 1},
        {'parent_id': 0, 'category_name': '家居', 'category_code': 'home', 'icon': '/static/images/category/home.png', 'sort': 5, 'status': 1}
    ]
    
    for category_data in categories:
        if not SpProductCategory.query.filter_by(category_code=category_data['category_code']).first():
            db.session.add(SpProductCategory(**category_data))
    db.session.commit()

if __name__ == '__main__':
    init_sp_mall_tables()
