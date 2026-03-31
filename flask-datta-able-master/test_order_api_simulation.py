# -*- encoding: utf-8 -*-
"""
模拟前端API调用测试
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpOrder

app = create_app(config_dict['Debug'])

def test_api_call():
    """测试API调用"""
    
    with app.app_context():
        print("=" * 70)
        print("模拟前端API调用测试")
        print("=" * 70)
        
        # 1. 查询所有订单
        all_orders = SpOrder.query.all()
        
        if len(all_orders) == 0:
            print("\n⚠️ 没有订单，无法测试")
            return
        
        test_order = all_orders[0]
        
        print(f"\n【1】测试订单信息:")
        print(f"    订单ID: {test_order.id}")
        print(f"    订单编号: {test_order.order_no}")
        print(f"    用户ID: {test_order.user_id}")
        
        # 2. 模拟不同的API调用场景
        print(f"\n【2】模拟API调用场景:")
        
        print(f"\n    场景A: 前端调用 GET /api/sp/order/detail/{test_order.id}")
        print(f"    期望: 返回订单详情")
        print(f"    实际: 模拟查询...")
        
        # 查询订单
        order = SpOrder.query.filter_by(id=test_order.id).first()
        
        if order:
            print(f"    结果: ✓ 找到订单")
            print(f"    订单详情:")
            print(f"      - 订单ID: {order.id}")
            print(f"      - 订单编号: {order.order_no}")
            print(f"      - 状态: {order.status}")
            print(f"      - 总金额: ¥{order.total_amount}")
        else:
            print(f"    结果: ✗ 未找到订单")
        
        print(f"\n    场景B: 前端调用 GET /api/sp/order/detail/999")
        print(f"    期望: 返回404错误")
        print(f"    实际: 模拟查询...")
        
        # 查询不存在的订单
        order_not_exist = SpOrder.query.filter_by(id=999).first()
        
        if order_not_exist:
            print(f"    结果: ✗ 应该找不到但找到了（数据异常）")
        else:
            print(f"    结果: ✓ 正确返回未找到")
        
        print(f"\n    场景C: 检查订单ID是否为字符串'undefined'")
        print(f"    如果前端传递的orderId='undefined'，会导致查询失败")
        print(f"    解决方案: 检查前端onLoad中的options参数")
        
        # 3. 创建测试脚本
        print(f"\n【3】创建API测试脚本...")
        
        with open('test_order_api.py', 'w', encoding='utf-8') as f:
            f.write('''# -*- encoding: utf-8 -*-
"""测试订单详情API"""

import requests
import json

def test_order_detail_api():
    """测试订单详情API"""
    
    BASE_URL = "http://localhost:5000"
    
    print("=" * 70)
    print("测试订单详情API")
    print("=" * 70)
    
    # 1. 测试订单列表API
    print("\\n【1】测试订单列表API...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/sp/order/list",
            headers={"X-User-Id": "1"}
        )
        print(f"    状态码: {response.status_code}")
        print(f"    响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"    错误: {e}")
    
    # 2. 测试订单详情API
    print("\\n【2】测试订单详情API...")
    order_id = input("请输入要查询的订单ID: ").strip()
    
    if not order_id:
        print("    取消测试")
        return
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/sp/order/detail/{order_id}",
            headers={"X-User-Id": "1"}
        )
        print(f"    状态码: {response.status_code}")
        print(f"    响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"    错误: {e}")
    
    print("\\n" + "=" * 70)

if __name__ == "__main__":
    test_order_detail_api()
''')
        
        print(f"    ✓ 已创建测试脚本: test_order_api.py")
        print(f"    运行命令: python test_order_api.py")
        
        print(f"\n【4】前端调试建议:")
        print(f"    1. 打开微信开发者工具")
        print(f"    2. 进入订单详情页面")
        print(f"    3. 查看Console控制台输出")
        print(f"    4. 查看Network网络请求")
        print(f"    5. 检查请求URL和参数")
        
        print(f"\n【5】需要检查的项:")
        print(f"    1. Network中是否有 /api/sp/order/detail/ 请求")
        print(f"    2. 请求的orderId参数是什么")
        print(f"    3. 请求头中是否有 X-User-Id: 1")
        print(f"    4. 响应状态码是什么")
        print(f"    5. 响应数据内容")
        
        print(f"\n【6】可能的问题:")
        print(f"    ❌ 问题1: orderId为undefined或空")
        print(f"       解决: 检查onLoad中的options参数")
        print(f"    ❌ 问题2: 用户ID不匹配")
        print(f"       解决: 检查X-User-Id请求头")
        print(f"    ❌ 问题3: API路径错误")
        print(f"       解决: 检查前端调用的API路径")
        print(f"    ❌ 问题4: 后端服务未启动")
        print(f"       解决: 重启Flask后端服务")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    test_api_call()
