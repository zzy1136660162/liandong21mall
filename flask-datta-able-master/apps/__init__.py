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
    for module_name in ('authentication', 'home', 'member', 'demand', 'demand_admin', 'product', 'sample'):
        module = import_module('apps.{}.routes'.format(module_name))
        if hasattr(module, 'blueprint'):
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
    from apps.member.auth import auth_ns
    api.add_namespace(member_user_api, path='/api/user')
    api.add_namespace(talent_ns, path='/api/user/talent')
    api.add_namespace(auth_ns, path='/api/auth')

    from apps.product.api import api as product_api, category_ns, cart_ns, order_ns, favorite_ns
    api.add_namespace(product_api, path='/api/product')
    api.add_namespace(category_ns, path='/api/product/category')
    api.add_namespace(cart_ns, path='/api/product/cart')
    api.add_namespace(order_ns, path='/api/product/order')
    api.add_namespace(favorite_ns, path='/api/product/favorite')

    from apps.sp_product.sp_product_detail_api import sp_product_detail_ns
    api.add_namespace(sp_product_detail_ns, path='/api/sp_product_detail')

    from apps.sp_mall.sp_api import (
        sp_product_ns, sp_category_ns, sp_cart_ns, sp_order_ns, sp_address_ns
    )
    api.add_namespace(sp_product_ns, path='/api/sp/product')
    api.add_namespace(sp_category_ns, path='/api/sp/category')
    api.add_namespace(sp_cart_ns, path='/api/sp/cart')
    api.add_namespace(sp_order_ns, path='/api/sp/order')
    api.add_namespace(sp_address_ns, path='/api/sp/address')

    from apps.sample.api import api as sample_api
    api.add_namespace(sample_api, path='/api/samples')


def configure_database(app):
    initialized = False

    @app.before_request
    def initialize_database():
        nonlocal initialized
        if not initialized:
            try:
                db.create_all()
            except Exception as e:
                print('> Warning: DBMS Exception: ' + str(e) )
                print('> Tables may already exist, skipping auto-creation')

            from apps.member.models import init_member_levels
            from apps.product.models import init_product_categories
            try:
                init_member_levels()
                init_product_categories()
            except Exception as e:
                print('> Warning: Initialization failed: ' + str(e) )

            initialized = True

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
