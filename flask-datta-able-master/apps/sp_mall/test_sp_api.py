# -*- encoding: utf-8 -*-
"""
测试 sp_mall 模块 API 连通性
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

def test_api():
    """测试 API 连通性"""
    
    print('=' * 60)
    print('测试 sp_mall 模块 API 连通性')
    print('=' * 60)
    
    # 测试商品分类列表
    print('\n1. 测试商品分类列表 API')
    try:
        response = requests.get(f'{BASE_URL}/api/sp/category/list')
        print(f'   状态码: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'   返回数据: {json.dumps(data, ensure_ascii=False, indent=2)}')
        else:
            print(f'   错误: {response.text}')
    except Exception as e:
        print(f'   ✗ 连接失败: {e}')
    
    # 测试商品列表
    print('\n2. 测试商品列表 API')
    try:
        response = requests.get(f'{BASE_URL}/api/sp/product/list')
        print(f'   状态码: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'   返回数据: {json.dumps(data, ensure_ascii=False, indent=2)[:200]}...')
        else:
            print(f'   错误: {response.text}')
    except Exception as e:
        print(f'   ✗ 连接失败: {e}')
    
    # 测试购物车列表
    print('\n3. 测试购物车列表 API')
    try:
        response = requests.get(
            f'{BASE_URL}/api/sp/cart/list',
            headers={'X-User-Id': '1'}
        )
        print(f'   状态码: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'   返回数据: {json.dumps(data, ensure_ascii=False, indent=2)}')
        else:
            print(f'   错误: {response.text}')
    except Exception as e:
        print(f'   ✗ 连接失败: {e}')
    
    # 测试地址列表
    print('\n4. 测试地址列表 API')
    try:
        response = requests.get(
            f'{BASE_URL}/api/sp/address/list',
            headers={'X-User-Id': '1'}
        )
        print(f'   状态码: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'   返回数据: {json.dumps(data, ensure_ascii=False, indent=2)}')
        else:
            print(f'   错误: {response.text}')
    except Exception as e:
        print(f'   ✗ 连接失败: {e}')
    
    print('\n' + '=' * 60)
    print('API 测试完成')
    print('=' * 60)

if __name__ == '__main__':
    test_api()
