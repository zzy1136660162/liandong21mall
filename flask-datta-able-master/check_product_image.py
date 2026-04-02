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
    # 查找筋骨祛痛保健膏
    product = Product.query.filter(Product.name.like('%筋骨祛痛保健膏%')).first()
    if product:
        print(f"商品名称: {product.name}")
        print(f"商品ID: {product.id}")
        print(f"main_image: {product.main_image}")
        print(f"images: {product.images}")
    else:
        print("未找到筋骨祛痛保健膏")
        
    # 列出所有带"筋骨"的商品
    print("\n所有带'筋骨'的商品:")
    products = Product.query.filter(Product.name.like('%筋骨%')).all()
    for p in products:
        print(f"  - {p.name}: main_image={p.main_image[:50] if p.main_image else '无'}...")
