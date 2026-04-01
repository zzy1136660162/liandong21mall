# -*- encoding: utf-8 -*-
"""
创建测试订单 - 用于验证订单详情功能
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpOrder, SpOrderItem, SpProduct
from apps.sp_mall.sp_services import SpOrderService

app = create_app(config_dict['Debug'])

def create_test_order():
    """创建测试订单"""
    
    with app.app_context():
        print("=" * 60)
        print("创建测试订单")
        print("=" * 60)
        
        # 1. 查询可用商品
        print("\n1. 查询可用商品...")
        products = SpProduct.query.filter_by(status=1).limit(3).all()
        
        if len(products) == 0:
            print("   ✗ 没有可用商品，请先添加商品数据")
            return
        
        print(f"   找到 {len(products)} 个商品:")
        for product in products:
            print(f"      - {product.product_name} (ID: {product.id}, 价格: ¥{product.price})")
        
        # 2. 选择商品创建订单
        print("\n2. 创建测试订单...")
        
        # 准备订单数据
        order_data = {
            'items': [
                {
                    'productId': products[0].id,
                    'skuId': None,
                    'quantity': 2
                }
            ],
            'address': {
                'name': '张三',
                'phone': '13800138000',
                'province': '广东省',
                'city': '深圳市',
                'district': '南山区',
                'detail': '科技园xxx路xxx号'
            }
        }
        
        print(f"\n   订单信息:")
        print(f"      商品: {products[0].product_name}")
        print(f"      数量: 2")
        print(f"      收货人: {order_data['address']['name']}")
        print(f"      电话: {order_data['address']['phone']}")
        print(f"      地址: {order_data['address']['province']}{order_data['address']['city']}{order_data['address']['district']}{order_data['address']['detail']}")
        
        # 3. 创建订单
        try:
            order, message = SpOrderService.create_order(
                user_id=1,
                order_data=order_data
            )
            
            if order:
                print(f"\n3. ✓ 订单创建成功!")
                print(f"\n   订单详情:")
                print(f"      订单ID: {order['orderId']}")
                print(f"      订单编号: {order['orderNo']}")
                print(f"      用户ID: {order['userId']}")
                print(f"      订单状态: {order['status']} ({order['statusText']})")
                print(f"      总金额: ¥{order['totalAmount']}")
                print(f"      实付金额: ¥{order['payAmount']}")
                print(f"      最终金额: ¥{order['finalAmount']}")
                
                if order.get('items'):
                    print(f"\n   商品明细:")
                    for item in order['items']:
                        print(f"      - {item['productName']} x {item['quantity']} = ¥{item['totalAmount']}")
                
                print(f"\n   收货信息:")
                print(f"      收货人: {order['receiverName']}")
                print(f"      电话: {order['receiverPhone']}")
                print(f"      地址: {order['receiverAddress']}")
                
                print(f"\n4. ✓ 现在可以在小程序中测试订单详情功能了")
                print(f"\n   测试步骤:")
                print(f"   1. 打开小程序")
                print(f"   2. 进入订单列表页面")
                print(f"   3. 点击刚才创建的订单")
                print(f"   4. 应该能看到完整的订单详情")
                
            else:
                print(f"\n3. ✗ 订单创建失败: {message}")
        
        except Exception as e:
            print(f"\n3. ✗ 订单创建失败: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    create_test_order()
