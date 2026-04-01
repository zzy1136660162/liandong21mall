# -*- encoding: utf-8 -*-
"""
直接测试订单详情API
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_order_detail_api():
    """测试订单详情API"""
    
    print("=" * 70)
    print("订单详情API测试")
    print("=" * 70)
    
    # 1. 测试订单列表API
    print("\n【1】测试订单列表API...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/sp/order/list",
            headers={"X-User-Id": "1"},
            timeout=5
        )
        print(f"    状态码: {response.status_code}")
        print(f"    响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                orders = data.get('data', {}).get('list', [])
                print(f"\n    找到 {len(orders)} 个订单:")
                for order in orders:
                    print(f"      - 订单ID: {order.get('orderId')}, 编号: {order.get('orderNo')}")
            else:
                print(f"    API返回错误: {data.get('message')}")
        else:
            print(f"    HTTP错误: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"    ✗ 连接失败! 后端服务是否启动?")
        print(f"    请先启动Flask服务:")
        print(f"    cd d:\\develop\\小程序文件\\实战项目\\电商小程序\\liandong21mall\\flask-datta-able-master")
        print(f"    python run.py")
        return
    except Exception as e:
        print(f"    错误: {e}")
        return
    
    # 2. 测试订单详情API
    print("\n" + "=" * 70)
    order_id_input = input("\n【2】请输入要查询的订单ID (直接回车查询第1个订单): ").strip()
    
    if not order_id_input:
        if orders:
            order_id = orders[0].get('orderId', 11)
        else:
            print("    没有订单可查询")
            return
    else:
        try:
            order_id = int(order_id_input)
        except ValueError:
            print(f"    ✗ 无效的订单ID: {order_id_input}")
            return
    
    print(f"\n    测试订单ID: {order_id}")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/sp/order/detail/{order_id}",
            headers={"X-User-Id": "1"},
            timeout=5
        )
        print(f"    状态码: {response.status_code}")
        print(f"    响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 200:
                order_detail = data.get('data', {})
                print(f"\n    ✓ 订单详情:")
                print(f"      订单ID: {order_detail.get('orderId')}")
                print(f"      订单编号: {order_detail.get('orderNo')}")
                print(f"      订单状态: {order_detail.get('status')} ({order_detail.get('statusText')})")
                print(f"      总金额: ¥{order_detail.get('totalAmount')}")
                print(f"      实付金额: ¥{order_detail.get('payAmount')}")
                print(f"      收货人: {order_detail.get('receiverName')}")
                print(f"      收货地址: {order_detail.get('receiverAddress')}")
                
                items = order_detail.get('items', [])
                print(f"\n      商品列表 ({len(items)} 个):")
                for item in items:
                    print(f"        - {item.get('productName')} x {item.get('quantity')} = ¥{item.get('totalAmount')}")
            else:
                print(f"    ✗ API返回错误: {data.get('message')}")
                print(f"\n    可能的原因:")
                print(f"    1. 订单不存在")
                print(f"    2. 用户ID不匹配")
                print(f"    3. 数据库查询错误")
        else:
            print(f"    ✗ HTTP错误: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"    ✗ 连接失败! 后端服务可能已停止")
    except Exception as e:
        print(f"    错误: {e}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_order_detail_api()
