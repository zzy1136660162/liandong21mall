# -*- encoding: utf-8 -*-
"""
测试订单详情API
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.config import config_dict
from apps import create_app, db
from apps.sp_mall.sp_models import SpOrder

app = create_app(config_dict['Debug'])

with app.app_context():
    try:
        # 测试查询订单7
        order_id = 7
        print(f"正在查询订单ID: {order_id}")
        
        order = SpOrder.query.get(order_id)
        if order:
            print(f"找到订单: {order.order_no}")
            print(f"订单状态: {order.status}")
            
            # 测试转换为字典
            try:
                order_dict = order.to_dict(include_items=True)
                print("订单转换为字典成功")
                print(f"订单数据: {order_dict}")
            except Exception as e:
                print(f"转换为字典失败: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"订单 {order_id} 不存在")
            
    except Exception as e:
        print(f"查询失败: {e}")
        import traceback
        traceback.print_exc()
