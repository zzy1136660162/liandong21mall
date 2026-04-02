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
    products = Product.query.all()
    print(f"总共有 {len(products)} 个商品\n")
    for p in products:
        print(f"ID: {p.id}, 名称: {p.name}")
        print(f"  图片: {p.main_image}")
        print(f"  图片列表: {p.images}")
        print()
