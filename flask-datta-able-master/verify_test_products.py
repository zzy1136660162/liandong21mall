# -*- encoding: utf-8 -*-
"""
验证测试商品数据
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpProduct, SpProductSku

app = create_app(config_dict['Debug'])

def verify_test_products():
    """验证测试商品数据"""
    
    with app.app_context():
        print("=" * 60)
        print("验证测试商品数据")
        print("=" * 60)
        
        # 查询所有商品
        products = SpProduct.query.order_by(SpProduct.sort).all()
        
        print(f"\n总共找到 {len(products)} 个商品\n")
        
        for product in products:
            print(f"商品ID: {product.id}")
            print(f"商品名称: {product.product_name}")
            print(f"商品编码: {product.product_code}")
            print(f"价格: ¥{product.price} (原价: ¥{product.original_price}, 会员价: ¥{product.member_price})")
            print(f"库存: {product.stock}, 销量: {product.sales}")
            print(f"简介: {product.brief}")
            print(f"描述长度: {len(product.description) if product.description else 0} 字符")
            print(f"图片数量: {len(product.images) if product.images else 0}")
            print(f"状态: {'上架' if product.status == 1 else '下架'}")
            print(f"标签: {'热销' if product.is_hot else ''} {'新品' if product.is_new else ''} {'推荐' if product.is_recommend else ''}")
            
            # 查询SKU
            skus = SpProductSku.query.filter_by(product_id=product.id).all()
            print(f"SKU数量: {len(skus)}")
            for sku in skus:
                print(f"  - {sku.sku_name}: ¥{sku.price}, 库存: {sku.stock}")
            
            print("-" * 60)
        
        # 显示第一个商品的详细描述
        if products:
            first_product = products[0]
            print("\n" + "=" * 60)
            print(f"商品详情预览: {first_product.product_name}")
            print("=" * 60)
            if first_product.description:
                # 只显示前500个字符
                preview = first_product.description[:500]
                print(preview + "..." if len(first_product.description) > 500 else preview)
            else:
                print("暂无详细描述")

if __name__ == "__main__":
    verify_test_products()