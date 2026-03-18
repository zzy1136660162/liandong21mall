# -*- encoding: utf-8 -*-
"""
样品申请模块 - 路由
"""

from flask import Blueprint, render_template

blueprint = Blueprint('sample', __name__, url_prefix='/admin/sample')


@blueprint.route('/apply/list')
def apply_list():
    return render_template('sample/apply_list.html')


@blueprint.route('/review')
def review():
    return render_template('sample/review.html')


@blueprint.route('/ship')
def ship():
    return render_template('sample/ship.html')


@blueprint.route('/status')
def status():
    return render_template('sample/status.html')
