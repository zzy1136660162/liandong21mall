# -*- encoding: utf-8 -*-
"""
商品商城模块 - 筛选类别管理路由
"""

from flask import render_template
from apps.sp_mall_admin import sp_filter_category_admin_bp
import logging

logger = logging.getLogger(__name__)


@sp_filter_category_admin_bp.route('/filter-category')
def filter_category_list():
    """筛选类别管理页面"""
    return render_template('sp_mall_admin/sp_filter_category_list.html',
                          segment='sp/filter-category')
