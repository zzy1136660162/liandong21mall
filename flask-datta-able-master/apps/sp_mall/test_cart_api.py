# -*- encoding: utf-8 -*-
"""
测试购物车API
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

def test_cart_api():
    """测试购物车API"""
    
    print('=' * 60)
    print('测试购物车API')
    print('=' * 60)
    
    # 1. 测试添加商品到购物车
    print('\n1. 测试添加商品到购物车')
    try:
        response = requests.post(
            f'{BASE_URL}/api/sp/cart/add',
            headers={'Content-Type': 'application/json', 'X-User-Id': '1'},
            json={'productId': 1, 'skuId': None, 'quantity': 1}
        )
        print(f'   状态码: {response.status_code}')
        print(f'   返回数据: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
    except Exception as e:
        print(f'   ✗ 请求失败: {e}')
    
    # 2. 测试获取购物车列表
    print('\n2. 测试获取购物车列表')
    try:
        response = requests.get(
            f'{BASE_URL}/api/sp/cart/list',
            headers={'X-User-Id': '1'}
        )
        print(f'   状态码: {response.status_code}')
        print(f'   返回数据: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
    except Exception as e:
        print(f'   ✗ 请求失败: {e}')
    
    # 3. 检查数据库中的购物车数据
    print('\n3. 检查数据库中的购物车数据')
    try:
        import pymysql
        connection = pymysql.connect(
            host='101.126.90.255',
            port=63306,
            user='root',
            password='Gesoft9919.',
            database='liandong21mall',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM sp_cart")
            carts = cursor.fetchall()
            print(f'   购物车表中有 {len(carts)} 条记录')
            for cart in carts:
                print(f'   - ID: {cart[0]}, 用户ID: {cart[1]}, 商品ID: {cart[2]}, 数量: {cart[4]}')
        
        connection.close()
    except Exception as e:
        print(f'   ✗ 数据库查询失败: {e}')
    
    print('\n' + '=' * 60)
    print('测试完成')
    print('=' * 60)

if __name__ == '__main__':
    test_cart_api()
