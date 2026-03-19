import re

file_path = r'd:\develop\小程序文件\实战项目\电商小程序\liandong21mall\flask-datta-able-master\apps\product\routes.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('product_bp', 'blueprint')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('替换完成')
