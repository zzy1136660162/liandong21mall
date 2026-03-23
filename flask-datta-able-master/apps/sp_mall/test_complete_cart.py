# -*- encoding: utf-8 -*-
"""
完整测试购物车功能
"""

import requests
import json
import pymysql

BASE_URL = 'http://localhost:5000'

def test_complete_cart_flow():
    """完整测试购物车流程"""
    
    print('=' * 80)
    print('完整测试购物车功能')
    print('=' * 80)
    
    # 1. 检查数据库中的商品数据
    print('\n【步骤1】检查数据库中的商品数据')
    try:
        connection = pymysql.connect(
            host='101.126.90.255',
            port=63306,
            user='root',
            password='Gesoft9919.',
            database='liandong21mall',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM sp_product WHERE status = 1")
            product_count = cursor.fetchone()[0]
            print(f'   ✓ 有效商品数量: {product_count}')
            
            if product_count > 0:
                cursor.execute("SELECT id, product_name, price FROM sp_product WHERE status = 1 LIMIT 3")
                products = cursor.fetchall()
                print('   商品示例:')
                for p in products:
                    print(f'     - ID: {p[0]}, 名称: {p[1]}, 价格: ¥{p[2]}')
        
        connection.close()
    except Exception as e:
        print(f'   ✗ 数据库查询失败: {e}')
        return
    
    # 2. 测试添加商品到购物车
    print('\n【步骤2】测试添加商品到购物车')
    try:
        response = requests.post(
            f'{BASE_URL}/api/sp/cart/add',
            headers={
                'Content-Type': 'application/json',
                'X-User-Id': '1'
            },
            json={
                'productId': 1,
                'skuId': None,
                'quantity': 2
            }
        )
        print(f'   状态码: {response.status_code}')
        result = response.json()
        print(f'   返回数据: {json.dumps(result, ensure_ascii=False, indent=2)}')
        
        if result['code'] == 200:
            print('   ✓ 添加成功')
        else:
            print(f'   ✗ 添加失败: {result["message"]}')
    except Exception as e:
        print(f'   ✗ 请求失败: {e}')
    
    # 3. 检查数据库中的购物车数据
    print('\n【步骤3】检查数据库中的购物车数据')
    try:
        connection = pymysql.connect(
            host='101.126.90.255',
            port=63306,
            user='root',
            password='Gesoft9919.',
            database='liandong21mall',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM sp_cart WHERE user_id = 1")
            cart_count = cursor.fetchone()[0]
            print(f'   ✓ 用户1的购物车商品数量: {cart_count}')
            
            if cart_count > 0:
                cursor.execute("""
                    SELECT c.id, c.product_id, p.product_name, c.quantity, c.selected
                    FROM sp_cart c
                    LEFT JOIN sp_product p ON c.product_id = p.id
                    WHERE c.user_id = 1
                """)
                carts = cursor.fetchall()
                print('   购物车商品:')
                for cart in carts:
                    print(f'     - 购物车ID: {cart[0]}, 商品ID: {cart[1]}, 商品名: {cart[2]}, 数量: {cart[3]}, 选中: {cart[4]}')
        
        connection.close()
    except Exception as e:
        print(f'   ✗ 数据库查询失败: {e}')
    
    # 4. 测试获取购物车列表
    print('\n【步骤4】测试获取购物车列表')
    try:
        response = requests.get(
            f'{BASE_URL}/api/sp/cart/list',
            headers={'X-User-Id': '1'}
        )
        print(f'   状态码: {response.status_code}')
        result = response.json()
        print(f'   返回数据: {json.dumps(result, ensure_ascii=False, indent=2)}')
        
        if result['code'] == 200:
            cart_list = result['data']
            if cart_list and len(cart_list) > 0:
                print(f'   ✓ 获取成功，购物车中有 {len(cart_list)} 个商品')
            else:
                print('   ⚠ 购物车为空')
        else:
            print(f'   ✗ 获取失败: {result["message"]}')
    except Exception as e:
        print(f'   ✗ 请求失败: {e}')
    
    print('\n' + '=' * 80)
    print('测试完成')
    print('=' * 80)

if __name__ == '__main__':
    test_complete_cart_flow()
