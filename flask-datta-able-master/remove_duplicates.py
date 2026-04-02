# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.config import config_dict
from apps import create_app, db
from apps.xp_product.models import Product
from sqlalchemy import func

config_mode = os.getenv('FLASK_CONFIG', 'Debug')
app = create_app(config_dict[config_mode])

with app.app_context():
    # 查找重复的商品名称
    duplicate_names = db.session.query(
        Product.name,
        func.count(Product.id).label('count')
    ).group_by(Product.name).having(func.count(Product.id) > 1).all()
    
    print("重复的商品名称:")
    for name, count in duplicate_names:
        print(f"  {name}: {count}个")
        
        # 查找所有重复的商品
        products = Product.query.filter_by(name=name).all()
        print(f"    商品ID: {[p.id for p in products]}")
    
    # 删除重复的，保留ID最小的那个
    deleted_count = 0
    for name, count in duplicate_names:
        products = Product.query.filter_by(name=name).order_by(Product.id).all()
        # 保留第一个，删除其余的
        for p in products[1:]:
            print(f"删除重复商品: ID={p.id}, 名称={p.name}")
            db.session.delete(p)
            deleted_count += 1
    
    db.session.commit()
    print(f"\n共删除 {deleted_count} 个重复商品!")
    
    # 验证
    print("\n验证 - 商品总数:")
    total = Product.query.count()
    print(f"  总数: {total}")
