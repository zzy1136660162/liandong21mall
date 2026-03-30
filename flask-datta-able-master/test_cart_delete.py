# -*- encoding: utf-8 -*-
"""
测试购物车删除功能
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpCart, SpProduct
from apps.sp_mall.sp_services import SpCartService

app = create_app(config_dict['Debug'])

def test_delete_cart():
    """测试删除购物车商品"""
    
    with app.app_context():
        print("=" * 60)
        print("测试购物车删除功能")
        print("=" * 60)
        
        # 测试用户ID
        test_user_id = 1
        
        # 1. 查看当前购物车
        print("\n1. 当前购物车列表:")
        cart_items = SpCart.query.filter_by(user_id=test_user_id).all()
        print(f"   共有 {len(cart_items)} 个商品")
        for item in cart_items:
            product = SpProduct.query.get(item.product_id)
            print(f"   - ID: {item.id}, 商品: {product.product_name if product else '未知'}, 数量: {item.quantity}")
        
        if len(cart_items) == 0:
            print("\n   购物车为空，添加测试商品...")
            
            # 添加测试商品
            products = SpProduct.query.limit(3).all()
            for product in products:
                cart = SpCart(
                    user_id=test_user_id,
                    product_id=product.id,
                    sku_id=None,
                    quantity=1,
                    selected=1
                )
                db.session.add(cart)
            
            db.session.commit()
            
            # 重新查询
            cart_items = SpCart.query.filter_by(user_id=test_user_id).all()
            print(f"\n   添加后共有 {len(cart_items)} 个商品:")
            for item in cart_items:
                product = SpProduct.query.get(item.product_id)
                print(f"   - ID: {item.id}, 商品: {product.product_name if product else '未知'}")
        
        # 2. 测试删除功能
        if len(cart_items) > 0:
            test_cart_id = cart_items[0].id
            product_name = SpProduct.query.get(cart_items[0].product_id).product_name
            
            print(f"\n2. 测试删除功能:")
            print(f"   要删除的商品: {product_name} (Cart ID: {test_cart_id})")
            
            result = SpCartService.delete_cart_item(test_cart_id, test_user_id)
            print(f"   删除结果: {'成功' if result else '失败'}")
            
            # 3. 验证删除结果
            print("\n3. 验证删除结果:")
            remaining_items = SpCart.query.filter_by(user_id=test_user_id).all()
            print(f"   剩余商品数量: {len(remaining_items)}")
            
            for item in remaining_items:
                product = SpProduct.query.get(item.product_id)
                print(f"   - ID: {item.id}, 商品: {product.product_name if product else '未知'}")
            
            # 检查被删除的商品是否还存在
            deleted_item = SpCart.query.get(test_cart_id)
            print(f"   被删除商品是否还存在: {'是（有问题）' if deleted_item else '否（正常）'}")
        
        print("\n" + "=" * 60)
        print("测试完成")
        print("=" * 60)

if __name__ == "__main__":
    test_delete_cart()
