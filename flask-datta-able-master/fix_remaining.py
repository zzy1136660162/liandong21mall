# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.config import config_dict
from apps import create_app, db
from apps.xp_product.models import Product, Category

config_mode = os.getenv('FLASK_CONFIG', 'Debug')
app = create_app(config_dict[config_mode])

with app.app_context():
    # 获取分类名称到ID的映射
    categories = {cat.name: cat.id for cat in Category.query.all()}
    print("分类映射:", categories)
    
    # 查找分类ID不在新分类中的商品
    valid_category_ids = set(categories.keys())
    products = Product.query.all()
    
    updated_count = 0
    for p in products:
        if p.category_id not in valid_category_ids:
            # 根据商品名称判断分类
            if '鼻' in p.name:
                new_cat = '鼻部护理'
            elif '痛' in p.name or '康' in p.name:
                new_cat = '疼痛舒缓'
            elif '眼' in p.name:
                new_cat = '眼部护理'
            elif '皮肤' in p.name or '抑菌' in p.name:
                new_cat = '皮肤护理'
            elif '发' in p.name:
                new_cat = '养发护发'
            elif '浴' in p.name or '足' in p.name:
                new_cat = '泡浴养生'
            else:
                new_cat = '体表保健'
            
            new_id = categories.get(new_cat)
            if new_id:
                print(f"修复: {p.name} | 旧分类ID: {p.category_id} -> 新分类ID: {new_id} ({new_cat})")
                p.category_id = new_id
                updated_count += 1
    
    db.session.commit()
    print(f"\n共修复 {updated_count} 个商品!")
