# -*- encoding: utf-8 -*-
"""
检查数据库中现有的表
"""

from apps import create_app, db
from apps.config import config_dict

app = create_app(config_dict['Debug'])

with app.app_context():
    # 查询所有表
    result = db.session.execute(db.text("SHOW TABLES"))
    tables = [row[0] for row in result.fetchall()]
    
    print("数据库中现有的表:")
    for table in tables:
        print(f"  - {table}")
    
    print(f"\n总共 {len(tables)} 个表")
    
    # 检查是否有冲突的表
    conflict_tables = ['order', 'order_item', 'product', 'product_sku']
    print("\n检查可能冲突的表:")
    for table in conflict_tables:
        if table in tables:
            print(f"  ✓ {table} - 已存在")
        else:
            print(f"  ✗ {table} - 不存在")