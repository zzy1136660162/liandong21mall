# -*- encoding: utf-8 -*-
"""
测试订单列表API
"""

from apps import create_app, db
from apps.sp_mall.sp_services import SpOrderService
from apps.sp_mall.sp_models import SpOrder
from apps.config import Config

def test_order_list():
    """测试订单列表功能"""
    app = create_app(Config)
    
    with app.app_context():
        print("="*70)
        print("测试订单列表功能")
        print("="*70)
        
        user_id = 1
        
        # 测试1：获取所有订单（status=None）
        print("\n【测试1】获取所有订单（status=None）")
        print("-"*70)
        result = SpOrderService.get_order_list(user_id, status=None, page=1, page_size=10)
        print(f"返回结果:")
        print(f"  订单数量: {result['total']}")
        print(f"  当前页: {result['page']}")
        print(f"  每页大小: {result['pageSize']}")
        print(f"  总页数: {result['totalPages']}")
        print(f"  订单列表长度: {len(result['list'])}")
        
        if result['list']:
            print(f"\n订单列表:")
            for i, order in enumerate(result['list'], 1):
                print(f"  {i}. 订单号: {order['orderNo']}, 状态: {order['status']}, 金额: {order['finalAmount']}")
        
        # 测试2：获取待付款订单
        print("\n【测试2】获取待付款订单（status='PENDING_PAY'）")
        print("-"*70)
        result = SpOrderService.get_order_list(user_id, status='PENDING_PAY', page=1, page_size=10)
        print(f"返回结果:")
        print(f"  订单数量: {result['total']}")
        print(f"  订单列表长度: {len(result['list'])}")
        
        if result['list']:
            print(f"\n订单列表:")
            for i, order in enumerate(result['list'], 1):
                print(f"  {i}. 订单号: {order['orderNo']}, 状态: {order['status']}")
        
        # 测试3：获取已支付订单
        print("\n【测试3】获取已支付订单（status='PAID'）")
        print("-"*70)
        result = SpOrderService.get_order_list(user_id, status='PAID', page=1, page_size=10)
        print(f"返回结果:")
        print(f"  订单数量: {result['total']}")
        print(f"  订单列表长度: {len(result['list'])}")
        
        if result['list']:
            print(f"\n订单列表:")
            for i, order in enumerate(result['list'], 1):
                print(f"  {i}. 订单号: {order['orderNo']}, 状态: {order['status']}")
        
        # 测试4：搜索订单
        print("\n【测试4】搜索订单（keyword='精华'）")
        print("-"*70)
        result = SpOrderService.get_order_list(user_id, status=None, page=1, page_size=10, keyword='精华')
        print(f"返回结果:")
        print(f"  订单数量: {result['total']}")
        print(f"  订单列表长度: {len(result['list'])}")
        
        if result['list']:
            print(f"\n订单列表:")
            for i, order in enumerate(result['list'], 1):
                print(f"  {i}. 订单号: {order['orderNo']}, 状态: {order['status']}")
        
        # 验证数据库中的订单总数
        print("\n【验证】数据库中的订单统计")
        print("-"*70)
        total_orders = SpOrder.query.filter_by(user_id=user_id).count()
        print(f"数据库中用户{user_id}的订单总数: {total_orders}")
        
        # 按状态统计
        status_count = {}
        for status in ['PENDING_PAY', 'PAID', 'SHIPPED', 'FINISHED', 'CANCELLED']:
            count = SpOrder.query.filter_by(user_id=user_id, status=status).count()
            status_count[status] = count
            print(f"  {status}: {count}个")
        
        print("\n" + "="*70)
        print("测试完成!")
        print("="*70)
        
        return True

if __name__ == '__main__':
    success = test_order_list()
    exit(0 if success else 1)
