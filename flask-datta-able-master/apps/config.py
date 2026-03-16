# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, random, string

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')  
    
    # Set up the App SECRET_KEY
    SECRET_KEY  = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))

    # Social AUTH context
    SOCIAL_AUTH_GITHUB  = False

    GITHUB_ID      = os.getenv('GITHUB_ID'    , None)
    GITHUB_SECRET  = os.getenv('GITHUB_SECRET', None)

    # Enable/Disable Github Social Login    
    if GITHUB_ID and GITHUB_SECRET:
         SOCIAL_AUTH_GITHUB  = True        

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =====================================================
    # Redis 本地配置
    # =====================================================
    REDIS_HOST     = 'localhost'  # 本地Redis
    REDIS_PORT     = 6379
    REDIS_PASSWORD = None
    REDIS_DB       = 0

    # =====================================================
    # 服务器Redis配置（暂时注释）
    # =====================================================
    # REDIS_HOST     = os.getenv('REDIS_HOST'    , 'localhost')
    # REDIS_PORT     = int(os.getenv('REDIS_PORT', 6379))
    # REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    # REDIS_DB       = int(os.getenv('REDIS_DB'  , 0))

    # =====================================================
    # MySQL 本地配置
    # =====================================================
    DB_ENGINE   = 'mysql'
    DB_USERNAME = 'root'          # 本地MySQL用户名
    DB_PASS     = '123456'        # 本地MySQL密码
    DB_HOST     = 'localhost'     # 本地MySQL地址
    DB_PORT     = '3306'          # 本地MySQL端口
    DB_NAME     = 'liandong21mall'  # 本地数据库名

    USE_SQLITE  = False  # 不使用SQLite，使用MySQL

    # =====================================================
    # 服务器数据库配置（暂时注释）
    # =====================================================
    # DB_ENGINE   = os.getenv('DB_ENGINE'   , None)
    # DB_USERNAME = os.getenv('DB_USERNAME' , None)
    # DB_PASS     = os.getenv('DB_PASS'     , None)
    # DB_HOST     = os.getenv('DB_HOST'     , None)
    # DB_PORT     = os.getenv('DB_PORT'     , None)
    # DB_NAME     = os.getenv('DB_NAME'     , None)
    # USE_SQLITE  = True

    # 构建数据库连接URI
    try:
        # Relational DBMS: PSQL, MySql
        # Use pymysql for MySQL
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

    except Exception as e:
        print('> Error: DBMS Exception: ' + str(e) )
        print('> Fallback to SQLite ')    
        # This will create a file in <app> FOLDER
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    
class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
