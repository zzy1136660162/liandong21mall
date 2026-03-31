# -*- encoding: utf-8 -*-
"""
检查购物车数据一致性
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpCart, SpProduct
from apps.sp_mall.sp_services import SpCartService

app = create_app(config_dict['Debug'])

def check_cart_consistency():
    """检查购物车数据一致性"""
    
    with app.app_context():
        print("=" * 60)
        print("检查购物车数据一致性")
        print("=" * 60)
        
        # 检查所有用户的购物车
        print("\n1. 所有用户的购物车商品:")
        all_carts = SpCart.query.all()
        print(f"   总共有 {len(all_carts)} 条购物车记录\n")
        
        # 按用户分组
        user_carts = {}
        for cart in all_carts:
            user_id = cart.user_id
            if user_id not in user_carts:
                user_carts[user_id] = []
            
            product = db.session.get(SpProduct, cart.product_id)
            user_carts[user_id].append({
                'cart_id': cart.id,
                'product_id': cart.product_id,
                'product_name': product.product_name if product else '未知',
                'quantity': cart.quantity
            })
        
        for user_id, carts in user_carts.items():
            print(f"\n   用户 {user_id} 的购物车 ({len(carts)} 个商品):")
            for cart in carts:
                print(f"      - Cart ID: {cart['cart_id']}, 商品: {cart['product_name']}, 数量: {cart['quantity']}")
        
        # 模拟前端请求的用户ID
        print("\n" + "=" * 60)
        print("2. 模拟前端请求:")
        print("   前端默认用户ID: 1")
        
        # 查询用户1的购物车
        user1_carts = SpCart.query.filter_by(user_id=1).all()
        print(f"\n   用户1的购物车商品: {len(user1_carts)} 个")
        
        if len(user1_carts) == 0:
            print("   ⚠️  购物车为空，请添加测试数据")
        
        print("\n" + "=" * 60)
        print("3. 潜在问题检查:")
        print("=" * 60)
        
        # 检查是否有重复的商品（同一用户、同一商品）
        print("\n   检查重复商品...")
        for user_id, carts in user_carts.items():
            # 按商品ID分组
            product_groups = {}
            for cart in carts:
                product_id = cart['product_id']
                if product_id not in product_groups:
                    product_groups[product_id] = []
                product_groups[product_id].append(cart)
            
            # 检查是否有重复
            has_duplicates = False
            for product_id, items in product_groups.items():
                if len(items) > 1:
                    has_duplicates = True
                    product = db.session.get(SpProduct, product_id)
                    print(f"\n   ⚠️  用户 {user_id} 有重复商品:")
                    print(f"      商品: {product.product_name if product else '未知'}")
                    for item in items:
                        print(f"      - Cart ID: {item['cart_id']}, 数量: {item['quantity']}")
            
            if not has_duplicates:
                print(f"\n   ✓ 用户 {user_id}: 无重复商品")
        
        # 检查商品是否还存在
        print("\n   检查商品是否存在...")
        for user_id, carts in user_carts.items():
            for cart in carts:
                product = db.session.get(SpProduct, cart['product_id'])
                if not product:
                    print(f"\n   ⚠️  购物车中的商品已不存在:")
                    print(f"      Cart ID: {cart['cart_id']}, Product ID: {cart['product_id']}")
        
        print("\n" + "=" * 60)
        print("检查完成")
        print("=" * 60)

if __name__ == "__main__":
    check_cart_consistency()
