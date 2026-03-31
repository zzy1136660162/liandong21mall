# -*- encoding: utf-8 -*-
"""
测试订单创建API
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

def test_create_order():
    """测试创建订单"""
    
    # 1. 首先获取一个商品详情
    print("1. 获取商品列表...")
    response = requests.get(f'{BASE_URL}/api/sp/product/list', params={'page': 1, 'pageSize': 1})
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.json()['code'] != 200:
        print("获取商品列表失败")
        return False
    
    products = response.json()['data']['list']
    if not products:
        print("没有商品数据")
        return False
    
    product = products[0]
    print(f"商品信息: ID={product['productId']}, 名称={product['productName']}, 价格={product['price']}")
    
    # 2. 获取默认地址
    print("\n2. 获取默认地址...")
    headers = {'X-User-Id': '1'}
    response = requests.get(f'{BASE_URL}/api/sp/address/default', headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.json()['code'] != 200 or not response.json()['data']:
        print("没有默认地址，创建一个...")
        # 创建地址
        address_data = {
            'name': '张三',
            'phone': '13800138000',
            'province': '北京市',
            'city': '北京市',
            'district': '朝阳区',
            'detail': 'XX街道XX号',
            'isDefault': True
        }
        response = requests.post(f'{BASE_URL}/api/sp/address/add', 
                                json=address_data, 
                                headers=headers)
        print(f"创建地址响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.json()['code'] != 200:
            print("创建地址失败")
            return False
        
        address = response.json()['data']
    else:
        address = response.json()['data']
    
    print(f"地址信息: {address['name']}, {address['phone']}")
    
    # 3. 创建订单
    print("\n3. 创建订单...")
    order_data = {
        'items': [
            {
                'productId': product['productId'],
                'quantity': 1
            }
        ],
        'address': {
            'name': address['name'],
            'phone': address['phone'],
            'province': address['province'],
            'city': address['city'],
            'district': address['district'],
            'detail': address['detail']
        },
        'remark': '测试订单'
    }
    
    print(f"订单数据: {json.dumps(order_data, indent=2, ensure_ascii=False)}")
    
    response = requests.post(f'{BASE_URL}/api/sp/order/create',
                           json=order_data,
                           headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code != 200:
        print(f"创建订单失败: HTTP {response.status_code}")
        return False
    
    result = response.json()
    if result['code'] != 200:
        print(f"创建订单失败: {result.get('message', '未知错误')}")
        return False
    
    order = result['data']
    print(f"\n✅ 订单创建成功!")
    print(f"订单ID: {order['orderId']}")
    print(f"订单编号: {order['orderNo']}")
    print(f"订单金额: {order['finalAmount']}")
    print(f"订单状态: {order['statusText']}")
    
    # 4. 查询订单列表
    print("\n4. 查询订单列表...")
    response = requests.get(f'{BASE_URL}/api/sp/order/list',
                          headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.json()['code'] == 200:
        orders = response.json()['data']['list']
        print(f"订单数量: {len(orders)}")
        for order in orders[:3]:
            print(f"  - 订单{order['orderId']}: {order['orderNo']}, 金额={order['finalAmount']}, 状态={order['statusText']}")
    
    # 5. 查询订单详情
    print("\n5. 查询订单详情...")
    response = requests.get(f'{BASE_URL}/api/sp/order/detail/{order["orderId"]}',
                          headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return True

if __name__ == '__main__':
    try:
        success = test_create_order()
        if success:
            print("\n" + "="*50)
            print("✅ 所有测试通过!")
            print("="*50)
        else:
            print("\n" + "="*50)
            print("❌ 测试失败!")
            print("="*50)
            exit(1)
    except Exception as e:
        print(f"\n❌ 测试异常: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
