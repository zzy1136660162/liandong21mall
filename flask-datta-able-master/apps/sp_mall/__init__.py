# -*- encoding: utf-8 -*-
"""
商品商城模块 - 成员1负责
包含：商品、购物车、订单、地址等功能
"""

from flask import Blueprint

sp_mall_bp = Blueprint('sp_mall', __name__)

from .sp_api import api as sp_mall_api
from .sp_api import (
    sp_product_ns,
    sp_category_ns,
    sp_cart_ns,
    sp_order_ns,
    sp_address_ns
)

__all__ = [
    'sp_mall_bp',
    'sp_mall_api',
    'sp_product_ns',
    'sp_category_ns',
    'sp_cart_ns',
    'sp_order_ns',
    'sp_address_ns'
]
