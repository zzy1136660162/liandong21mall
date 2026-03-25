import requests

response = requests.get('http://localhost:5000/api/sp/product/1')
print(f'Status Code: {response.status_code}')
print(f'Response:')
import json
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
