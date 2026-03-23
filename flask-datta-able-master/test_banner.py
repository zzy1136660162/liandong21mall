import requests
import json

r = requests.get('http://localhost:5000/api/product/recommend?limit=3')
data = json.loads(r.text)

print('Banner products:')
for p in data['data']:
    print(f'  {p["productName"]}: {p["mainImage"]}')
