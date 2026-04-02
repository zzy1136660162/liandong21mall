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
    # 获取所有分类
    categories = {cat.id: cat.name for cat in Category.query.all()}
    print("分类列表:")
    for cid, name in categories.items():
        print(f"  ID {cid}: {name}")
    
    print("\n商品分类情况:")
    products = Product.query.all()
    for p in products:
        cat_name = categories.get(p.category_id, "未知分类")
        print(f"  {p.name}: category_id={p.category_id} ({cat_name})")
