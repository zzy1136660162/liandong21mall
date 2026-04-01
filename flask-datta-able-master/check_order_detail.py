# -*- encoding: utf-8 -*-
"""
检查订单详情问题
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpOrder, SpOrderItem

app = create_app(config_dict['Debug'])

def check_order_issue():
    """检查订单详情问题"""
    
    with app.app_context():
        print("=" * 60)
        print("检查订单详情问题")
        print("=" * 60)
        
        # 1. 查询所有订单
        print("\n1. 查询所有订单...")
        all_orders = SpOrder.query.all()
        print(f"   总共有 {len(all_orders)} 个订单")
        
        if len(all_orders) == 0:
            print("\n   ⚠️ 没有订单，无法测试订单详情功能")
            return
        
        # 2. 测试获取订单详情
        print("\n2. 测试获取订单详情...")
        
        test_order = all_orders[0]
        print(f"\n   测试订单:")
        print(f"      订单ID: {test_order.id}")
        print(f"      订单编号: {test_order.order_no}")
        print(f"      用户ID: {test_order.user_id}")
        print(f"      订单状态: {test_order.status}")
        
        # 模拟前端请求（user_id=1）
        print(f"\n   模拟前端请求 (user_id=1):")
        order_with_user1 = SpOrder.query.filter_by(id=test_order.id, user_id=1).first()
        
        if order_with_user1:
            print(f"   ✓ 找到订单（user_id=1）")
        else:
            print(f"   ✗ 未找到订单（user_id=1）")
            print(f"   提示: 该订单的用户ID是 {test_order.user_id}，不是 1")
        
        # 不限制用户ID
        print(f"\n   不限制用户ID查询:")
        order_no_user = SpOrder.query.filter_by(id=test_order.id).first()
        
        if order_no_user:
            print(f"   ✓ 找到订单")
            print(f"   订单用户ID: {order_no_user.user_id}")
        else:
            print(f"   ✗ 未找到订单")
        
        # 3. 测试不同的用户ID
        print(f"\n3. 测试不同用户ID的订单...")
        
        user_ids = set([order.user_id for order in all_orders])
        print(f"   数据库中的用户ID: {user_ids}")
        
        for uid in user_ids:
            orders = SpOrder.query.filter_by(user_id=uid).all()
            print(f"   用户 {uid} 的订单数: {len(orders)}")
        
        # 4. 检查订单详情数据
        print(f"\n4. 检查订单详情数据...")
        
        for order in all_orders:
            print(f"\n   订单 {order.id} ({order.order_no}):")
            print(f"      用户ID: {order.user_id}")
            print(f"      状态: {order.status}")
            print(f"      总金额: ¥{order.total_amount}")
            print(f"      实付金额: ¥{order.pay_amount}")
            print(f"      最终金额: ¥{order.final_amount}")
            
            # 查询订单项
            items = SpOrderItem.query.filter_by(order_id=order.id).all()
            print(f"      订单项数量: {len(items)}")
            
            for item in items:
                print(f"         - {item.product_name} x {item.quantity} = ¥{item.total_amount}")
        
        # 5. 建议
        print("\n" + "=" * 60)
        print("5. 问题分析与建议:")
        print("=" * 60)
        
        if 1 not in user_ids:
            print("\n   ⚠️ 数据库中没有用户ID为1的订单！")
            print("   可能原因:")
            print("   1. 创建订单时使用了不同的用户ID")
            print("   2. 前端请求的用户ID与订单用户ID不匹配")
            print("   3. 订单被删除或转移到了其他用户")
        
        print("\n   建议:")
        print("   1. 检查订单创建时的用户ID")
        print("   2. 确认前端请求头中的X-User-Id")
        print("   3. 查看后端日志获取更多信息")
        print("   4. 检查订单详情API的返回数据")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    check_order_issue()
