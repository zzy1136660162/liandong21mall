import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f'.env文件路径: {env_path}')
print(f'.env文件是否存在: {os.path.exists(env_path)}')

if os.path.exists(env_path):
    load_dotenv(env_path)
    print('✓ .env文件加载成功')
else:
    print('✗ .env文件不存在')

print('\n环境变量检查：')
print(f'DB_ENGINE: {os.getenv("DB_ENGINE")}')
print(f'DB_NAME: {os.getenv("DB_NAME")}')
print(f'DB_USERNAME: {os.getenv("DB_USERNAME")}')
