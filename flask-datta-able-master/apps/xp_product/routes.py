# -*- encoding: utf-8 -*-
"""
商品选品模块 - 路由
"""

from flask import Blueprint, render_template

blueprint = Blueprint('product', __name__, url_prefix='/admin/product')


@blueprint.route('/')
def index():
    return render_template('product/index.html')


@blueprint.route('/list')
def list():
    return render_template('product/list.html')


@blueprint.route('/category')
def category():
    return render_template('product/category.html')


@blueprint.route('/commission')
def commission():
    return render_template('product/commission.html')
