# -*- encoding: utf-8 -*-
"""
检查现有表结构
"""

from apps import create_app, db
from apps.config import config_dict

app = create_app(config_dict['Debug'])

with app.app_context():
    print("=" * 60)
    print("检查现有表结构")
    print("=" * 60)
    
    # 检查商品表结构
    print("\nsp_product 表结构:")
    print("-" * 60)
    result = db.session.execute(db.text("DESCRIBE sp_product"))
    for row in result.fetchall():
        print(f"  {row[0]:25s} {row[1]:20s} {row[2]:10s} {row[3]:10s}")
    
    # 检查订单表结构
    print("\nsp_order 表结构:")
    print("-" * 60)
    result = db.session.execute(db.text("DESCRIBE sp_order"))
    for row in result.fetchall():
        print(f"  {row[0]:25s} {row[1]:20s} {row[2]:10s} {row[3]:10s}")
    
    # 检查订单明细表结构
    print("\nsp_order_item 表结构:")
    print("-" * 60)
    result = db.session.execute(db.text("DESCRIBE sp_order_item"))
    for row in result.fetchall():
        print(f"  {row[0]:25s} {row[1]:20s} {row[2]:10s} {row[3]:10s}")