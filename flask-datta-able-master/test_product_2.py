import requests

response = requests.get('http://localhost:5000/api/sp/product/2')
print(f'Status Code: {response.status_code}')
print(f'Response:')
import json
data = response.json()
print(json.dumps(data, indent=2, ensure_ascii=False))

if data.get('code') == 200:
    product = data.get('data', {})
    print(f'\n商品名称: {product.get("name")}')
    print(f'商品图片数量: {len(product.get("images", []))}')
    print(f'推荐商品数量: {len(product.get("recommendations", []))}')
    print(f'商品描述长度: {len(product.get("description", ""))}')
