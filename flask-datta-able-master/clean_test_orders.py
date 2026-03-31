# -*- encoding: utf-8 -*-
"""
删除订单测试数据
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpOrder, SpOrderItem

app = create_app(config_dict['Debug'])

def clean_test_orders():
    """删除订单测试数据"""
    
    with app.app_context():
        print("=" * 60)
        print("删除订单测试数据")
        print("=" * 60)
        
        # 1. 查询所有订单
        print("\n1. 查询所有订单...")
        all_orders = SpOrder.query.all()
        print(f"   总共有 {len(all_orders)} 个订单")
        
        if len(all_orders) == 0:
            print("\n   ✓ 订单表已经是空的，无需清理")
            return
        
        # 2. 显示订单详情
        print("\n2. 订单列表:")
        for i, order in enumerate(all_orders, 1):
            print(f"\n   订单 {i}:")
            print(f"      订单ID: {order.id}")
            print(f"      订单编号: {order.order_no}")
            print(f"      用户ID: {order.user_id}")
            print(f"      订单金额: ¥{order.total_amount}")
            print(f"      订单状态: {order.status}")
            print(f"      创建时间: {order.created_at}")
            
            # 查询订单项
            items = SpOrderItem.query.filter_by(order_id=order.id).all()
            print(f"      订单项数量: {len(items)}")
            for item in items:
                print(f"         - {item.product_name} x {item.quantity}")
        
        # 3. 确认删除
        print("\n" + "=" * 60)
        confirm = input("确认删除所有订单测试数据？(输入 'yes' 确认): ")
        
        if confirm.lower() != 'yes':
            print("\n   ✗ 取消删除操作")
            return
        
        # 4. 删除订单项
        print("\n3. 删除订单项...")
        order_ids = [order.id for order in all_orders]
        items_deleted = 0
        
        for order_id in order_ids:
            items = SpOrderItem.query.filter_by(order_id=order_id).all()
            for item in items:
                db.session.delete(item)
                items_deleted += 1
        
        print(f"   删除了 {items_deleted} 条订单项")
        
        # 5. 删除订单
        print("\n4. 删除订单...")
        orders_deleted = 0
        
        for order in all_orders:
            db.session.delete(order)
            orders_deleted += 1
        
        print(f"   删除了 {orders_deleted} 个订单")
        
        # 6. 提交更改
        try:
            db.session.commit()
            print("\n5. ✓ 删除成功！")
            print(f"   共删除 {orders_deleted} 个订单")
            print(f"   共删除 {items_deleted} 条订单项")
        except Exception as e:
            db.session.rollback()
            print(f"\n5. ✗ 删除失败: {e}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    clean_test_orders()
