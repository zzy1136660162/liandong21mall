# -*- encoding: utf-8 -*-
"""
创建测试订单并支付
"""

from apps import create_app, db
from apps.sp_mall.sp_services import SpOrderService
from apps.sp_mall.sp_models import SpOrder, SpProduct, SpProductSku, SpAddress
from apps.config import Config
from datetime import datetime

def create_and_pay_order():
    """创建订单并支付"""
    app = create_app(Config)
    
    with app.app_context():
        print("="*70)
        print("创建订单并测试支付")
        print("="*70)
        
        user_id = 1
        
        # 查找可用的商品
        product = SpProduct.query.filter_by(status=1).first()
        if not product:
            print("\n❌ 没有可用的商品")
            return False
        
        print(f"\n选择商品:")
        print(f"  商品ID: {product.id}")
        print(f"  商品名称: {product.product_name}")
        print(f"  价格: {product.price}")
        
        # 查找SKU
        sku = SpProductSku.query.filter_by(product_id=product.id, status=1).first()
        if not sku:
            print("\n❌ 商品没有可用的SKU")
            return False
        
        print(f"  SKU ID: {sku.id}")
        print(f"  SKU价格: {sku.price}")
        
        # 查找地址
        address = SpAddress.query.filter_by(user_id=user_id).first()
        if not address:
            print("\n❌ 没有收货地址")
            return False
        
        print(f"\n收货地址:")
        print(f"  收货人: {address.name}")
        print(f"  电话: {address.phone}")
        print(f"  地址: {address.province}{address.city}{address.district}{address.detail}")
        
        # 创建订单
        try:
            print(f"\n开始创建订单...")
            order_dict, message = SpOrderService.create_order(
                user_id=user_id,
                order_data={
                    'items': [{
                        'productId': product.id,
                        'skuId': sku.id,
                        'quantity': 1
                    }],
                    'address': {
                        'name': address.name,
                        'phone': address.phone,
                        'province': address.province,
                        'city': address.city,
                        'district': address.district,
                        'detail': address.detail
                    },
                    'remark': '测试订单'
                }
            )
            
            if order_dict:
                print(f"\n✅ 订单创建成功!")
                print(f"  订单ID: {order_dict['orderId']}")
                print(f"  订单号: {order_dict['orderNo']}")
                print(f"  状态: {order_dict['status']}")
                print(f"  订单金额: {order_dict['finalAmount']}")
                
                # 立即支付订单
                print(f"\n开始支付订单...")
                pay_result, pay_message = SpOrderService.pay_order(
                    order_dict['orderId'],
                    user_id,
                    payment_method='WECHAT_PAY'
                )
                
                if pay_result:
                    print(f"\n✅ 支付成功!")
                    print(f"  返回消息: {pay_message}")
                    print(f"\n支付后的订单信息:")
                    print(f"  订单ID: {pay_result['orderId']}")
                    print(f"  订单号: {pay_result['orderNo']}")
                    print(f"  状态: {pay_result['status']}")
                    print(f"  支付时间: {pay_result.get('payTime', 'N/A')}")
                    print(f"  支付方式: {pay_result.get('paymentMethod', 'N/A')}")
                    
                    # 验证数据库
                    order = SpOrder.query.get(order_dict['orderId'])
                    print(f"\n数据库验证:")
                    print(f"  状态: {order.status}")
                    print(f"  支付时间: {order.pay_time}")
                    print(f"  支付方式: {order.payment_method}")
                    
                    if order.status == 'PAID':
                        print(f"\n✅ 订单状态已正确更新为已支付")
                        return True
                    else:
                        print(f"\n❌ 订单状态未正确更新")
                        return False
                else:
                    print(f"\n❌ 支付失败: {pay_message}")
                    return False
            else:
                print(f"\n❌ 订单创建失败: {message}")
                return False
                
        except Exception as e:
            print(f"\n❌ 操作异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = create_and_pay_order()
    exit(0 if success else 1)
