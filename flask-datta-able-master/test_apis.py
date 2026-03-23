import requests

base_url = 'http://127.0.0.1:5000'

print('测试API接口...\n')

try:
    print('1. 测试分类列表接口')
    response = requests.get(f'{base_url}/api/product/category/list')
    print(f'   状态码: {response.status_code}')
    if response.status_code == 200:
        print(f'   响应: {response.json()}')
    else:
        print(f'   错误: {response.text}')
except Exception as e:
    print(f'   请求失败: {e}')

print('\n')

try:
    print('2. 测试商品列表接口')
    response = requests.get(f'{base_url}/api/product/list?page=1&pageSize=10')
    print(f'   状态码: {response.status_code}')
    if response.status_code == 200:
        print(f'   响应: {response.json()}')
    else:
        print(f'   错误: {response.text}')
except Exception as e:
    print(f'   请求失败: {e}')

print('\n')

try:
    print('3. 测试购物车总数接口')
    response = requests.get(f'{base_url}/api/product/cart/total')
    print(f'   状态码: {response.status_code}')
    if response.status_code == 200:
        print(f'   响应: {response.json()}')
    else:
        print(f'   错误: {response.text}')
except Exception as e:
    print(f'   请求失败: {e}')

print('\nAPI测试完成！')
