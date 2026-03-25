# -*- encoding: utf-8 -*-
"""
样品申请模块 - 路由
"""

from flask import Blueprint, render_template, request, jsonify
from apps.sample.models import SampleApply
from apps import db

blueprint = Blueprint('sample', __name__, url_prefix='/admin/sample')


@blueprint.route('/apply/list')
def apply_list():
    page = request.args.get('page', 1, type=int)
    page_size = 20
    status = request.args.get('status', type=int)
    keyword = request.args.get('keyword')
    
    query = SampleApply.query
    
    if status is not None:
        query = query.filter_by(status=status)
    
    if keyword:
        query = query.filter(SampleApply.apply_no.like(f'%{keyword}%') | SampleApply.product_name.like(f'%{keyword}%'))
    
    pagination = query.order_by(SampleApply.created_at.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )
    
    return render_template('sample/apply_list.html', 
                          applies=pagination.items,
                          pagination=pagination,
                          page=page,
                          page_size=page_size)


@blueprint.route('/review')
def review():
    page = request.args.get('page', 1, type=int)
    page_size = 20
    
    pagination = SampleApply.query.filter_by(status=0).order_by(SampleApply.created_at.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )
    
    return render_template('sample/review.html',
                          applies=pagination.items,
                          pagination=pagination)


@blueprint.route('/ship')
def ship():
    page = request.args.get('page', 1, type=int)
    page_size = 20
    
    pagination = SampleApply.query.filter(
        SampleApply.status == 1,
        SampleApply.ship_status == 0
    ).order_by(SampleApply.created_at.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )
    
    return render_template('sample/ship.html',
                          applies=pagination.items,
                          pagination=pagination)


@blueprint.route('/status')
def status():
    page = request.args.get('page', 1, type=int)
    page_size = 20
    
    pagination = SampleApply.query.order_by(SampleApply.created_at.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )
    
    return render_template('sample/status.html',
                          applies=pagination.items,
                          pagination=pagination)


@blueprint.route('/apply/review/<int:apply_id>', methods=['POST'])
def review_apply(apply_id):
    data = request.get_json()
    action = data.get('action')
    remark = data.get('remark', '')
    
    apply = SampleApply.query.get(apply_id)
    if not apply:
        return jsonify({'code': 404, 'message': '申请不存在'})
    
    if action == 'approve':
        apply.status = 1
    elif action == 'reject':
        apply.status = 2
    
    apply.review_remark = remark
    
    try:
        db.session.commit()
        return jsonify({'code': 200, 'message': '审核成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)})


@blueprint.route('/apply/ship/<int:apply_id>', methods=['POST'])
def ship_apply(apply_id):
    data = request.get_json()
    company = data.get('company')
    ship_no = data.get('ship_no')
    
    apply = SampleApply.query.get(apply_id)
    if not apply:
        return jsonify({'code': 404, 'message': '申请不存在'})
    
    apply.ship_status = 1
    apply.ship_company = company
    apply.ship_no = ship_no
    
    try:
        db.session.commit()
        return jsonify({'code': 200, 'message': '发货成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e)})
