# -*- encoding: utf-8 -*-
"""
模拟前端删除请求
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpCart, SpProduct
from apps.sp_mall.sp_services import SpCartService
import requests
import json

app = create_app(config_dict['Debug'])

def simulate_frontend_delete():
    """模拟前端删除请求"""
    
    with app.app_context():
        print("=" * 60)
        print("模拟前端删除购物车商品")
        print("=" * 60)
        
        # 添加测试数据
        test_user_id = 1
        print("\n1. 添加测试商品到购物车...")
        
        products = SpProduct.query.limit(3).all()
        added_products = []
        
        for product in products:
            # 检查是否已经在购物车中
            existing = SpCart.query.filter_by(
                user_id=test_user_id,
                product_id=product.id
            ).first()
            
            if not existing:
                cart = SpCart(
                    user_id=test_user_id,
                    product_id=product.id,
                    sku_id=None,
                    quantity=1,
                    selected=1
                )
                db.session.add(cart)
                added_products.append(product.product_name)
        
        db.session.commit()
        print(f"   添加了 {len(added_products)} 个商品")
        for name in added_products:
            print(f"   - {name}")
        
        # 查询当前购物车
        cart_items = SpCart.query.filter_by(user_id=test_user_id).all()
        print(f"\n2. 当前购物车有 {len(cart_items)} 个商品:")
        for item in cart_items:
            product = db.session.get(SpProduct, item.product_id)
            print(f"   - Cart ID: {item.id}, 商品: {product.product_name}")
        
        if len(cart_items) == 0:
            print("\n   ⚠️ 购物车为空，无法测试删除功能")
            return
        
        # 测试删除第一个商品
        test_cart_id = cart_items[0].id
        product_to_delete = db.session.get(SpProduct, cart_items[0].product_id).product_name
        
        print(f"\n3. 模拟前端删除请求:")
        print(f"   删除商品: {product_to_delete}")
        print(f"   Cart ID: {test_cart_id}")
        print(f"   User ID: {test_user_id}")
        
        # 调用删除服务
        result = SpCartService.delete_cart_item(test_cart_id, test_user_id)
        
        print(f"\n4. 删除结果:")
        print(f"   返回值: {result}")
        print(f"   成功: {'✓' if result else '✗'}")
        
        # 验证删除
        print(f"\n5. 验证删除:")
        remaining_carts = SpCart.query.filter_by(user_id=test_user_id).all()
        print(f"   剩余商品数: {len(remaining_carts)}")
        
        deleted_cart = SpCart.query.get(test_cart_id)
        if deleted_cart:
            print(f"   ⚠️  删除失败，商品仍然存在")
        else:
            print(f"   ✓ 删除成功，商品已不存在")
        
        print(f"\n6. 剩余商品列表:")
        for item in remaining_carts:
            product = db.session.get(SpProduct, item.product_id)
            print(f"   - Cart ID: {item.id}, 商品: {product.product_name}")
        
        print("\n" + "=" * 60)
        print("测试完成")
        print("=" * 60)
        
        print("\n⚠️  可能的问题：")
        print("1. 删除操作本身是否成功？")
        print("2. 前端是否显示了正确的删除结果？")
        print("3. 刷新页面后是否重新加载了数据？")
        print("4. 用户ID是否正确？")
        print("5. 商品是否被其他地方重新添加了？")

if __name__ == "__main__":
    simulate_frontend_delete()
