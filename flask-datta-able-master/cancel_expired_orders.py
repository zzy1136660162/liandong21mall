# -*- encoding: utf-8 -*-
"""
订单超时自动取消脚本
可以配合APScheduler定时执行，或者手动运行
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.config import config_dict
from apps import create_app, db
from apps.sp_mall.sp_services import SpOrderService
from datetime import datetime

def cancel_expired_orders_task():
    """执行超时订单取消任务"""
    app = create_app(config_dict['Debug'])
    
    with app.app_context():
        try:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始检查超时订单...")
            
            cancelled_count = SpOrderService.cancel_expired_orders(timeout_minutes=30)
            
            if cancelled_count > 0:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 已自动取消 {cancelled_count} 个超时订单")
            else:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 没有超时订单")
                
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 执行失败: {e}")

if __name__ == '__main__':
    import time
    
    print("=" * 60)
    print("订单超时自动取消服务")
    print("=" * 60)
    print("每分钟检查一次超时订单")
    print("按 Ctrl+C 停止服务")
    print("=" * 60)
    
    try:
        while True:
            cancel_expired_orders_task()
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 下次检查将在 60 秒后...")
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n服务已停止")
