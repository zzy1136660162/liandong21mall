# -*- encoding: utf-8 -*-
"""
商品商城模块 - 后台管理 (sp_前缀)
成员1负责：商品分类、商品管理、订单管理
"""

from flask import Blueprint

sp_mall_admin_bp = Blueprint('sp_mall_admin', __name__, url_prefix='/admin/sp')

from . import routes

__all__ = ['sp_mall_admin_bp']
