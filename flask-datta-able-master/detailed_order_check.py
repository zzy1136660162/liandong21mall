# -*- encoding: utf-8 -*-
"""
详细检查订单查询问题
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpOrder, SpOrderItem

app = create_app(config_dict['Debug'])

def detailed_order_check():
    """详细检查订单查询问题"""
    
    with app.app_context():
        print("=" * 70)
        print("详细检查订单查询问题")
        print("=" * 70)
        
        # 1. 查询所有订单
        print("\n【1】查询所有订单...")
        all_orders = SpOrder.query.all()
        print(f"    数据库中总订单数: {len(all_orders)}")
        
        if len(all_orders) == 0:
            print("    ⚠️ 数据库中没有订单！")
            return
        
        # 2. 显示所有订单信息
        print("\n【2】所有订单详情:")
        for i, order in enumerate(all_orders, 1):
            print(f"\n    订单 {i}:")
            print(f"      订单ID: {order.id}")
            print(f"      订单编号: {order.order_no}")
            print(f"      用户ID: {order.user_id}")
            print(f"      状态: {order.status}")
            print(f"      总金额: ¥{order.total_amount}")
            print(f"      实付金额: ¥{order.pay_amount}")
            print(f"      收货人: {order.receiver_name}")
            print(f"      创建时间: {order.created_at}")
            
            # 查询订单项
            items = SpOrderItem.query.filter_by(order_id=order.id).all()
            print(f"      订单项数量: {len(items)}")
            for item in items:
                print(f"        - {item.product_name} x {item.quantity}")
        
        # 3. 模拟前端查询（user_id=1）
        print("\n【3】模拟前端查询 (user_id=1):")
        orders_user1 = SpOrder.query.filter_by(user_id=1).all()
        print(f"    用户1的订单数: {len(orders_user1)}")
        
        if len(orders_user1) > 0:
            print(f"    ✓ 找到用户1的订单:")
            for order in orders_user1:
                print(f"      - 订单ID {order.id}: {order.order_no} (¥{order.total_amount})")
        else:
            print(f"    ✗ 未找到用户1的订单")
            print(f"    提示: 订单的用户ID可能是 {all_orders[0].user_id if all_orders else '未知'}")
        
        # 4. 测试订单详情API的查询逻辑
        print("\n【4】测试订单详情查询:")
        
        for order in all_orders:
            print(f"\n    测试订单ID {order.id}:")
            
            # 查询1: 只按ID查
            order_by_id = SpOrder.query.filter_by(id=order.id).first()
            print(f"      只按ID查: {'✓ 找到' if order_by_id else '✗ 未找到'}")
            
            # 查询2: 按ID和user_id=1查
            order_by_id_user1 = SpOrder.query.filter_by(
                id=order.id, 
                user_id=1
            ).first()
            print(f"      按ID+user_id=1查: {'✓ 找到' if order_by_id_user1 else '✗ 未找到'}")
            
            # 查询3: 按实际user_id查
            order_by_id_real_user = SpOrder.query.filter_by(
                id=order.id, 
                user_id=order.user_id
            ).first()
            print(f"      按ID+真实user_id({order.user_id})查: {'✓ 找到' if order_by_id_real_user else '✗ 未找到'}")
            
            # 如果user_id!=1，给出提示
            if order.user_id != 1:
                print(f"\n    ⚠️  问题发现!")
                print(f"      该订单的用户ID是 {order.user_id}")
                print(f"      但前端请求的是 user_id=1")
                print(f"      导致查询时无法匹配!")
        
        # 5. 解决方案
        print("\n【5】解决方案:")
        print("\n    方案A: 更新订单的用户ID为1")
        if len(all_orders) > 0 and all_orders[0].user_id != 1:
            confirm = input(f"    是否将所有订单的用户ID更新为1? (输入 'yes' 确认): ")
            if confirm.lower() == 'yes':
                print("\n    开始更新...")
                for order in all_orders:
                    order.user_id = 1
                db.session.commit()
                print("    ✓ 更新成功!")
                print("    现在可以在小程序中查看订单详情了")
            else:
                print("    取消更新")
        
        print("\n    方案B: 检查前端用户ID")
        print("    确保前端请求的X-User-Id与订单用户ID一致")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    detailed_order_check()
