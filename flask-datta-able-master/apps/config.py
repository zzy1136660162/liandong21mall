# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, random, string
from dotenv import load_dotenv

# Load .env file from the parent directory of the apps folder
basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(os.path.dirname(basedir), '.env')
load_dotenv(env_path)

class Config(object):

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

    # Redis Configuration
    REDIS_HOST     = os.getenv('REDIS_HOST'    , 'localhost')
    REDIS_PORT     = int(os.getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    REDIS_DB       = int(os.getenv('REDIS_DB'  , 0))

    DB_ENGINE   = os.getenv('DB_ENGINE'   , None)
    DB_USERNAME = os.getenv('DB_USERNAME' , None)
    DB_PASS     = os.getenv('DB_PASS'     , None)
    DB_HOST     = os.getenv('DB_HOST'     , None)
    DB_PORT     = os.getenv('DB_PORT'     , None)
    DB_NAME     = os.getenv('DB_NAME'     , None)

    USE_SQLITE  = True 

    # try to set up a Relational DBMS
    if DB_ENGINE and DB_NAME and DB_USERNAME:

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

            USE_SQLITE  = False
            print(f'> Using MySQL database: {SQLALCHEMY_DATABASE_URI}')

        except Exception as e:

            print(f'> Error: DBMS Exception: {str(e)} ')
            print(f'> Exception type: {type(e).__name__}')
            print('> Fallback to SQLite ')    

    if USE_SQLITE:

        # This will create a file in <app> FOLDER
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
        print(f'> Using SQLite database: {SQLALCHEMY_DATABASE_URI}')
    
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
