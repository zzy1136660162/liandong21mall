import os
from dotenv import load_dotenv

load_dotenv()

DB_ENGINE = os.getenv('DB_ENGINE', None)
DB_USERNAME = os.getenv('DB_USERNAME', None)
DB_PASS = os.getenv('DB_PASS', None)
DB_HOST = os.getenv('DB_HOST', None)
DB_PORT = os.getenv('DB_PORT', None)
DB_NAME = os.getenv('DB_NAME', None)

print('环境变量检查：')
print(f'DB_ENGINE: {DB_ENGINE}')
print(f'DB_USERNAME: {DB_USERNAME}')
print(f'DB_PASS: {DB_PASS}')
print(f'DB_HOST: {DB_HOST}')
print(f'DB_PORT: {DB_PORT}')
print(f'DB_NAME: {DB_NAME}')

print('\n条件检查：')
print(f'DB_ENGINE and DB_NAME and DB_USERNAME: {bool(DB_ENGINE and DB_NAME and DB_USERNAME)}')
print(f'DB_ENGINE: {bool(DB_ENGINE)}')
print(f'DB_NAME: {bool(DB_NAME)}')
print(f'DB_USERNAME: {bool(DB_USERNAME)}')

if DB_ENGINE and DB_NAME and DB_USERNAME:
    print('\n✓ 所有条件满足，应该使用MySQL')
else:
    print('\n✗ 条件不满足，将使用SQLite')
