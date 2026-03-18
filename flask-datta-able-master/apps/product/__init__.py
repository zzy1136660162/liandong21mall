# -*- encoding: utf-8 -*-
"""
商品商城模块 - 初始化文件
"""

from flask import Blueprint
from apps.product.models import (
    ProductCategory, Product, ProductSku,
    Cart, Order, OrderItem,
    init_product_categories
)

product_bp = Blueprint('product', __name__)

__all__ = [
    'product_bp',
    'ProductCategory',
    'Product',
    'ProductSku',
    'Cart',
    'Order',
    'OrderItem',
    'init_product_categories'
]
