# -*- encoding: utf-8 -*-
"""
注册 sp_mall 模块到 Flask 应用
使用独立文件，避免修改 __init__.py 造成冲突
"""

from apps.sp_mall.sp_api import (
    api as sp_mall_api,
    sp_product_ns,
    sp_category_ns,
    sp_cart_ns,
    sp_order_ns,
    sp_address_ns
)


def register_sp_mall_api(api):
    """注册 sp_mall 模块的 API"""
    api.add_namespace(sp_product_ns, path='/api/sp/product')
    api.add_namespace(sp_category_ns, path='/api/sp/category')
    api.add_namespace(sp_cart_ns, path='/api/sp/cart')
    api.add_namespace(sp_order_ns, path='/api/sp/order')
    api.add_namespace(sp_address_ns, path='/api/sp/address')
    
    print('> sp_mall API registered successfully')
    return api
