# -*- encoding: utf-8 -*-
"""
数据库表初始化和检查脚本
确保所有必要的表都存在
"""

from apps import create_app, db
from apps.sp_mall.sp_models import (
    SpProductCategory, SpProduct, SpProductSku,
    SpCart, SpOrder, SpOrderItem, SpAddress
)
from apps.sp_mall.sp_banner_models import SpBanner
import sys

def init_database():
    """初始化数据库表"""
    app = create_app()
    
    with app.app_context():
        try:
            print("="*60)
            print("开始检查数据库表...")
            print("="*60)
            
            # 获取数据库引擎和检查器
            inspector = db.inspect(db.engine)
            
            # 检查并创建所有表
            tables_to_check = [
                'sp_product_category',
                'sp_product',
                'sp_product_sku',
                'sp_cart',
                'sp_order',
                'sp_order_item',
                'sp_address',
                'sp_banner'
            ]
            
            existing_tables = inspector.get_table_names()
            print(f"\n已存在的表: {existing_tables}")
            
            for table_name in tables_to_check:
                if table_name in existing_tables:
                    print(f"\n✅ 表 {table_name} 已存在")
                    
                    # 检查列
                    columns = [col['name'] for col in inspector.get_columns(table_name)]
                    print(f"   字段数量: {len(columns)}")
                    
                    # 检查索引
                    indexes = inspector.get_indexes(table_name)
                    if indexes:
                        print(f"   索引: {[idx['name'] for idx in indexes]}")
                else:
                    print(f"\n❌ 表 {table_name} 不存在，需要创建")
            
            print("\n" + "="*60)
            print("尝试创建缺失的表...")
            print("="*60)
            
            # 创建所有表
            db.create_all()
            
            print("\n✅ 数据库表创建完成!")
            
            # 再次检查
            print("\n" + "="*60)
            print("检查更新后的表...")
            print("="*60)
            
            existing_tables = inspector.get_table_names()
            print(f"\n现在的表: {existing_tables}")
            
            # 初始化分类数据
            print("\n" + "="*60)
            print("初始化商品分类数据...")
            print("="*60)
            
            init_sp_product_categories()
            
            # 创建测试商品
            print("\n" + "="*60)
            print("创建测试商品数据...")
            print("="*60)
            
            create_test_products()
            
            print("\n" + "="*60)
            print("✅ 数据库初始化完成!")
            print("="*60)
            
            return True
            
        except Exception as e:
            print(f"\n❌ 数据库初始化失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def init_sp_product_categories():
    """初始化商品分类"""
    categories = [
        {'category_name': '护肤', 'category_code': 'skincare', 'sort': 1},
        {'category_name': '彩妆', 'category_code': 'makeup', 'sort': 2},
        {'category_name': '个护', 'category_code': 'personal_care', 'sort': 3},
        {'category_name': '食品', 'category_code': 'food', 'sort': 4},
        {'category_name': '家居', 'category_code': 'home', 'sort': 5}
    ]
    
    for cat_data in categories:
        existing = SpProductCategory.query.filter_by(category_code=cat_data['category_code']).first()
        if not existing:
            category = SpProductCategory(**cat_data)
            db.session.add(category)
            print(f"  ✅ 添加分类: {cat_data['category_name']}")
        else:
            print(f"  ℹ️ 分类已存在: {cat_data['category_name']}")
    
    db.session.commit()

def create_test_products():
    """创建测试商品"""
    # 检查是否已有商品
    product_count = SpProduct.query.count()
    print(f"  当前商品数量: {product_count}")
    
    if product_count > 0:
        print("  ℹ️ 商品数据已存在，跳过创建")
        return
    
    # 获取第一个分类
    category = SpProductCategory.query.first()
    if not category:
        print("  ❌ 没有商品分类，请先添加分类")
        return
    
    test_products = [
        {
            'product_name': '焕颜修护精华液',
            'product_code': 'P001',
            'main_image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&h=400&fit=crop',
            'images': ['https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800', 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800'],
            'price': 299.00,
            'original_price': 399.00,
            'member_price': 259.00,
            'stock': 1000,
            'sales': 500,
            'brief': '焕颜修护精华液，深层滋养肌肤',
            'status': 1,
            'is_hot': 1,
            'is_new': 1,
            'is_recommend': 1
        },
        {
            'product_name': '深层清洁洁面乳',
            'product_code': 'P002',
            'main_image': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop',
            'images': ['https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800'],
            'price': 158.00,
            'original_price': 198.00,
            'member_price': 138.00,
            'stock': 800,
            'sales': 300,
            'brief': '深层清洁洁面乳，温和不刺激',
            'status': 1,
            'is_hot': 1,
            'is_new': 0,
            'is_recommend': 1
        },
        {
            'product_name': '保湿修护面霜',
            'product_code': 'P003',
            'main_image': 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=400&h=400&fit=crop',
            'images': ['https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=800'],
            'price': 358.00,
            'original_price': 458.00,
            'member_price': 318.00,
            'stock': 500,
            'sales': 200,
            'brief': '保湿修护面霜，持久锁水',
            'status': 1,
            'is_hot': 1,
            'is_new': 1,
            'is_recommend': 1
        }
    ]
    
    for prod_data in test_products:
        product = SpProduct(
            category_id=category.id,
            **prod_data
        )
        db.session.add(product)
        db.session.flush()
        
        # 创建SKU
        sku = SpProductSku(
            product_id=product.id,
            sku_code=f"{prod_data['product_code']}-SKU001",
            sku_name='默认规格',
            spec={'规格': '默认'},
            price=prod_data['price'],
            original_price=prod_data.get('original_price'),
            member_price=prod_data.get('member_price'),
            stock=prod_data['stock'],
            status=1
        )
        db.session.add(sku)
        
        print(f"  ✅ 添加商品: {prod_data['product_name']} (ID: {product.id})")
    
    db.session.commit()
    print(f"\n  ✅ 共创建 {len(test_products)} 个商品")

def create_test_address():
    """创建测试地址"""
    address = SpAddress.query.filter_by(user_id=1).first()
    if address:
        print("  ℹ️ 测试地址已存在")
        return address
    
    address = SpAddress(
        user_id=1,
        name='张三',
        phone='13800138000',
        province='北京市',
        city='北京市',
        district='朝阳区',
        detail='XX街道XX号XX小区XX号楼XX室',
        is_default=1
    )
    db.session.add(address)
    db.session.commit()
    
    print("  ✅ 创建测试地址")
    return address

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
