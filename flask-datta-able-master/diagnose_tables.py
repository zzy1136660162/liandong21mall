# -*- encoding: utf-8 -*-
"""
诊断数据库表存在情况
"""

from apps import create_app, db
from apps.config import config_dict

app = create_app(config_dict['Debug'])

with app.app_context():
    print("=" * 60)
    print("数据库连接诊断")
    print("=" * 60)
    
    # 显示数据库连接信息
    print(f"\n当前连接的数据库: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # 查询所有表
    result = db.session.execute(db.text("SHOW TABLES"))
    all_tables = [row[0] for row in result.fetchall()]
    
    print(f"\n数据库中总共有 {len(all_tables)} 个表")
    
    # 成员1负责的表
    member1_tables = [
        'sp_product_category',  # 商品分类表
        'sp_product',           # 商品表
        'sp_product_sku',       # 商品SKU表
        'sp_cart',              # 购物车表
        'sp_order',             # 订单表
        'sp_order_item',        # 订单项表
        'sp_address'            # 收货地址表
    ]
    
    print("\n" + "=" * 60)
    print("成员1负责的表检查结果:")
    print("=" * 60)
    
    all_found = True
    for table_name in member1_tables:
        if table_name in all_tables:
            # 查询表的记录数
            try:
                count_result = db.session.execute(db.text(f"SELECT COUNT(*) FROM {table_name}"))
                count = count_result.fetchone()[0]
                print(f"✓ {table_name:20s} - 存在，记录数: {count}")
            except Exception as e:
                print(f"✓ {table_name:20s} - 存在，但查询记录数失败: {e}")
        else:
            print(f"✗ {table_name:20s} - 不存在")
            all_found = False
    
    print("\n" + "=" * 60)
    if all_found:
        print("✓ 所有成员1负责的表都已存在！")
        print("\n在 Navicat 中查找这些表的步骤:")
        print("1. 确保连接到 liandong21mall 数据库")
        print("2. 展开数据库，点击 '表' 节点")
        print("3. 在表列表中查找以下表名:")
        for table in member1_tables:
            print(f"   - {table}")
        print("4. 如果看不到，请右键点击连接名，选择 '刷新'")
    else:
        print("✗ 部分表不存在，需要创建")
    
    print("=" * 60)