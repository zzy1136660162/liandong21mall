# -*- encoding: utf-8 -*-
"""
商品分类初始化脚本
创建体表保健和功能食品两大类及其二级分类
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps import create_app, db
from apps.sp_mall.sp_models import SpProductCategory

app = create_app('apps.config.DebugConfig')


def init_categories():
    """初始化商品分类"""

    # 一级分类
    parent_categories = [
        {
            'category_code': 'BODY_HEALTH',
            'category_name': '体表保健',
            'sort': 1
        },
        {
            'category_code': 'FUNCTIONAL_FOOD',
            'category_name': '功能食品',
            'sort': 2
        }
    ]

    # 二级分类
    child_categories = {
        'BODY_HEALTH': [
            {'category_code': 'PAIN_RELIEF', 'category_name': '疼痛舒缓', 'sort': 1},
            {'category_code': 'NOSE_CARE', 'category_name': '鼻部护理', 'sort': 2},
            {'category_code': 'EYE_CARE', 'category_name': '眼部护理', 'sort': 3},
            {'category_code': 'SKIN_CARE', 'category_name': '皮肤护理', 'sort': 4},
            {'category_code': 'WOMEN_CARE', 'category_name': '女性调理', 'sort': 5},
            {'category_code': 'MEN_CARE', 'category_name': '男性养护', 'sort': 6},
            {'category_code': 'BABY_CARE', 'category_name': '小儿护理', 'sort': 7},
            {'category_code': 'SLIMMING', 'category_name': '纤体瘦身', 'sort': 8},
            {'category_code': 'HAIR_CARE', 'category_name': '养发护发', 'sort': 9},
            {'category_code': 'BATH_CARE', 'category_name': '泡浴养生', 'sort': 10},
        ],
        'FUNCTIONAL_FOOD': [
            {'category_code': 'GINSENG', 'category_name': '人参滋补', 'sort': 1},
            {'category_code': 'EJIAO', 'category_name': '阿胶膏滋', 'sort': 2},
            {'category_code': 'HERBAL_TEA', 'category_name': '草本茶饮', 'sort': 3},
            {'category_code': 'SOLID_DRINK', 'category_name': '固体饮料', 'sort': 4},
            {'category_code': 'TABLET_CANDY', 'category_name': '压片糖果', 'sort': 5},
            {'category_code': 'NUTRITION_GRANULE', 'category_name': '营养颗粒', 'sort': 6},
            {'category_code': 'PLANT_DRINK', 'category_name': '植物饮品', 'sort': 7},
            {'category_code': 'PREPARED_WINE', 'category_name': '配制酒', 'sort': 8},
        ]
    }

    with app.app_context():
        created_parents = {}

        # 创建一级分类
        for cat_data in parent_categories:
            existing = SpProductCategory.query.filter_by(category_code=cat_data['category_code']).first()
            if not existing:
                category = SpProductCategory(
                    category_name=cat_data['category_name'],
                    category_code=cat_data['category_code'],
                    parent_id=0,
                    sort=cat_data['sort'],
                    status=1
                )
                db.session.add(category)
                db.session.flush()
                created_parents[cat_data['category_code']] = category.id
                print(f'[OK] Create parent category: {cat_data["category_name"]} (ID: {category.id})')
            else:
                created_parents[cat_data['category_code']] = existing.id
                print(f'[SKIP] Parent category exists: {cat_data["category_name"]} (ID: {existing.id})')

        db.session.commit()

        # 创建二级分类
        for parent_code, children in child_categories.items():
            parent_id = created_parents.get(parent_code)
            if not parent_id:
                print(f'[ERROR] Parent not found: {parent_code}')
                continue

            for child_data in children:
                existing = SpProductCategory.query.filter_by(category_code=child_data['category_code']).first()
                if not existing:
                    category = SpProductCategory(
                        category_name=child_data['category_name'],
                        category_code=child_data['category_code'],
                        parent_id=parent_id,
                        sort=child_data['sort'],
                        status=1
                    )
                    db.session.add(category)
                    print(f'  [OK] Create child category: {child_data["category_name"]}')
                else:
                    print(f'  [SKIP] Child category exists: {child_data["category_name"]}')

        db.session.commit()
        print('\n[SUCCESS] Category initialization completed!')


if __name__ == '__main__':
    init_categories()
