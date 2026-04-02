# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.config import config_dict
from apps import create_app, db
from apps.xp_product.models import Product

config_mode = os.getenv('FLASK_CONFIG', 'Debug')
app = create_app(config_dict[config_mode])

with app.app_context():
    products = Product.query.order_by(Product.name).all()
    print(f"总共有 {len(products)} 个商品\n")
    
    # 按名称分组
    from collections import defaultdict
    name_groups = defaultdict(list)
    for p in products:
        name_groups[p.name].append(p)
    
    # 显示所有商品
    for name, items in sorted(name_groups.items()):
        if len(items) > 1:
            print(f"【重复】{name}: {len(items)}个")
            for p in items:
                print(f"    ID={p.id}, 分类ID={p.category_id}, 图片={p.main_image[:50] if p.main_image else '无'}...")
        else:
            p = items[0]
            print(f"{name}: ID={p.id}, 分类ID={p.category_id}")
