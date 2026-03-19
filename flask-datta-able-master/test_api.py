import requests

base_url = 'http://127.0.0.1:5000/api'

print('测试API接口...\n')

print('1. 测试商品分类列表：')
try:
    response = requests.get(f'{base_url}/product/category/list')
    print(f'   状态码: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'   响应数据: {data}')
    else:
        print(f'   错误: {response.text}')
except Exception as e:
    print(f'   异常: {e}')

print('\n2. 测试商品列表：')
try:
    response = requests.get(f'{base_url}/product/list?page=1&pageSize=10')
    print(f'   状态码: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'   响应数据: {data}')
    else:
        print(f'   错误: {response.text}')
except Exception as e:
    print(f'   异常: {e}')

print('\n3. 测试购物车总数：')
try:
    response = requests.get(f'{base_url}/product/cart/total')
    print(f'   状态码: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'   响应数据: {data}')
    else:
        print(f'   错误: {response.text}')
except Exception as e:
    print(f'   异常: {e}')

print('\nAPI测试完成！')
