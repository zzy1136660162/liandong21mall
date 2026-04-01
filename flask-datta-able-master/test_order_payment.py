# -*- encoding: utf-8 -*-
"""
测试订单支付功能
"""

from apps import create_app, db
from apps.sp_mall.sp_services import SpOrderService
from apps.sp_mall.sp_models import SpOrder
from apps.config import Config
from datetime import datetime

def test_order_payment():
    """测试订单支付功能"""
    app = create_app(Config)
    
    with app.app_context():
        print("="*70)
        print("测试订单支付功能")
        print("="*70)
        
        # 查找一个待付款的订单
        user_id = 1
        pending_orders = SpOrder.query.filter_by(
            user_id=user_id,
            status='PENDING_PAY'
        ).all()
        
        if not pending_orders:
            print("\n❌ 没有找到待付款的订单")
            print("请先创建一个订单")
            return False
        
        print(f"\n找到 {len(pending_orders)} 个待付款订单")
        
        # 选择第一个订单进行测试
        test_order = pending_orders[0]
        print(f"\n测试订单:")
        print(f"  订单ID: {test_order.id}")
        print(f"  订单号: {test_order.order_no}")
        print(f"  当前状态: {test_order.status}")
        print(f"  订单金额: {test_order.final_amount}")
        
        try:
            # 调用支付服务
            print(f"\n开始支付订单...")
            order_dict, message = SpOrderService.pay_order(
                test_order.id,
                user_id,
                payment_method='WECHAT_PAY'
            )
            
            if order_dict:
                print(f"\n✅ 支付成功!")
                print(f"  返回消息: {message}")
                print(f"\n更新后的订单信息:")
                print(f"  订单ID: {order_dict['orderId']}")
                print(f"  订单号: {order_dict['orderNo']}")
                print(f"  状态: {order_dict['status']}")
                print(f"  支付时间: {order_dict.get('payTime', 'N/A')}")
                print(f"  支付方式: {order_dict.get('paymentMethod', 'N/A')}")
                
                # 验证数据库中的状态
                updated_order = SpOrder.query.get(test_order.id)
                print(f"\n数据库验证:")
                print(f"  状态: {updated_order.status}")
                print(f"  支付时间: {updated_order.pay_time}")
                print(f"  支付方式: {updated_order.payment_method}")
                
                if updated_order.status == 'PAID':
                    print(f"\n✅ 订单状态已正确更新为已支付")
                    return True
                else:
                    print(f"\n❌ 订单状态未正确更新")
                    return False
            else:
                print(f"\n❌ 支付失败: {message}")
                return False
                
        except Exception as e:
            print(f"\n❌ 支付异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = test_order_payment()
    exit(0 if success else 1)
