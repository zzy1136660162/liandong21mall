# -*- encoding: utf-8 -*-
"""
检查订单ID=12的问题
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpOrder, SpOrderItem

app = create_app(config_dict['Debug'])

def check_order_12():
    """检查订单ID=12"""
    
    with app.app_context():
        print("=" * 70)
        print("检查订单ID=12的问题")
        print("=" * 70)
        
        # 1. 查询订单ID=12
        print("\n【1】查询订单ID=12...")
        order = SpOrder.query.get(12)
        
        if order:
            print(f"   ✓ 找到订单ID=12:")
            print(f"      订单编号: {order.order_no}")
            print(f"      用户ID: {order.user_id}")
            print(f"      状态: {order.status}")
            print(f"      总金额: ¥{order.total_amount}")
            print(f"      创建时间: {order.created_at}")
        else:
            print(f"   ✗ 未找到订单ID=12")
        
        # 2. 查询所有订单
        print("\n【2】查询所有订单...")
        all_orders = SpOrder.query.all()
        print(f"   数据库中共有 {len(all_orders)} 个订单:")
        
        for order in all_orders:
            print(f"   - ID: {order.id}, 编号: {order.order_no}, 用户: {order.user_id}, 状态: {order.status}")
        
        # 3. 测试查询（不限制用户ID）
        print("\n【3】测试不同的查询方式...")
        
        # 不限制用户ID
        order_no_user = SpOrder.query.get(12)
        print(f"   查询1 (不限制用户ID): {'✓ 找到' if order_no_user else '✗ 未找到'}")
        
        # 限制用户ID=1
        order_user1 = SpOrder.query.filter_by(id=12, user_id=1).first()
        print(f"   查询2 (限制用户ID=1): {'✓ 找到' if order_user1 else '✗ 未找到'}")
        
        # 4. 分析问题
        print("\n【4】问题分析:")
        
        if not order:
            print("   ⚠️ 订单ID=12根本不存在于数据库中!")
            print("   可能原因:")
            print("   1. 订单创建后被删除了")
            print("   2. 订单ID不正确")
            print("   3. 数据库数据不一致")
        elif order and not order_user1:
            print("   ⚠️ 订单存在，但用户ID不匹配!")
            print(f"   订单的用户ID: {order.user_id}")
            print(f"   请求的用户ID: 1")
            print("   解决方案: 更新订单的用户ID为1")
            
            # 自动修复
            confirm = input("\n   是否将订单的用户ID更新为1? (输入 'yes' 确认): ")
            if confirm.lower() == 'yes':
                print("\n   正在更新...")
                order.user_id = 1
                db.session.commit()
                print("   ✓ 更新成功!")
            else:
                print("   取消更新")
        else:
            print("   ✓ 订单查询应该正常")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    check_order_12()
