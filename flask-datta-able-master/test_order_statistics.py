# -*- encoding: utf-8 -*-
"""
测试订单统计API
"""

from apps import create_app, db
from apps.sp_mall.sp_services import SpOrderService
from apps.config import Config

def test_order_statistics():
    """测试订单统计功能"""
    app = create_app(Config)
    
    with app.app_context():
        print("="*70)
        print("测试订单统计功能")
        print("="*70)
        
        # 测试用户ID 1
        user_id = 1
        print(f"\n用户ID: {user_id}")
        
        try:
            statistics = SpOrderService.get_order_statistics(user_id)
            print("\n统计结果:")
            for key, value in statistics.items():
                print(f"  {key}: {value}")
            
            print("\n✅ 订单统计功能正常!")
            return True
            
        except Exception as e:
            print(f"\n❌ 订单统计失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = test_order_statistics()
    exit(0 if success else 1)
