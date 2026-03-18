# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from importlib import import_module


db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home', 'member', 'product', 'sample'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def register_api(app):
    """注册REST API"""
    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
    
    api = Api(
        app, 
        version='1.0', 
        title='联动21商城API',
        description='会员达人模块API',
        authorizations=authorizations,
        security='apikey'
    )
    
    from apps.member.api import api as member_user_api, talent_ns
    from apps.product.api import api as product_api
    from apps.sample.api import api as sample_api
    api.add_namespace(member_user_api, path='/api/user')
    api.add_namespace(talent_ns, path='/api/user/talent')
    api.add_namespace(product_api, path='/api/products')
    api.add_namespace(sample_api, path='/api/samples')


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')    
            db.create_all()
        
        from apps.member.models import init_member_levels
        init_member_levels()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

from apps.authentication.oauth import github_blueprint

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    register_api(app)
    app.register_blueprint(github_blueprint, url_prefix="/login")    
    configure_database(app)
    return app
