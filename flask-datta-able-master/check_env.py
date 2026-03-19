import os
from dotenv import load_dotenv

load_dotenv()

print('环境变量检查：')
print(f'DB_ENGINE: {os.getenv("DB_ENGINE")}')
print(f'DB_NAME: {os.getenv("DB_NAME")}')
print(f'DB_USERNAME: {os.getenv("DB_USERNAME")}')
print(f'DB_HOST: {os.getenv("DB_HOST")}')
print(f'DB_PORT: {os.getenv("DB_PORT")}')
print(f'DB_PASS: {os.getenv("DB_PASS")}')

print('\n数据库连接字符串构建：')
DB_ENGINE = os.getenv('DB_ENGINE', None)
DB_USERNAME = os.getenv('DB_USERNAME', None)
DB_PASS = os.getenv('DB_PASS', None)
DB_HOST = os.getenv('DB_HOST', None)
DB_PORT = os.getenv('DB_PORT', None)
DB_NAME = os.getenv('DB_NAME', None)

if DB_ENGINE and DB_NAME and DB_USERNAME:
    try:
        engine = DB_ENGINE
        if engine == 'mysql':
            engine = 'mysql+pymysql'
        
        SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
            engine,
            DB_USERNAME,
            DB_PASS,
            DB_HOST,
            DB_PORT,
            DB_NAME
        )
        
        print(f'SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}')
        print(f'USE_SQLITE: False')
    except Exception as e:
        print(f'构建连接字符串失败：{e}')
        print(f'USE_SQLITE: True')
else:
    print('缺少必要的数据库配置，将使用 SQLite')
    print(f'USE_SQLITE: True')
