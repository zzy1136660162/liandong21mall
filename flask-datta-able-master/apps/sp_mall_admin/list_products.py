# -*- encoding: utf-8 -*-
"""
列出所有商品
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps import create_app, db
from apps.sp_mall.sp_models import SpProduct

app = create_app('apps.config.DebugConfig')

with app.app_context():
    products = SpProduct.query.all()
    print(f'Total products: {len(products)}\n')
    for p in products:
        print(f'ID: {p.id}, Name: {p.product_name}, Category ID: {p.category_id}')
