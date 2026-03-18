import os
from dotenv import load_dotenv

load_dotenv()

print('当前工作目录:', os.getcwd())
print('.env文件路径:', os.path.join(os.getcwd(), '.env'))
print('.env文件是否存在:', os.path.exists('.env'))

if os.path.exists('.env'):
    print('\n.env文件内容:')
    with open('.env', 'r', encoding='utf-8') as f:
        print(f.read())
else:
    print('\n.env文件不存在！')
