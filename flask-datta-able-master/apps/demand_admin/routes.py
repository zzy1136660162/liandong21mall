# -*- encoding: utf-8 -*-
"""
研发需求模块 - 后台管理页面
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required
from apps import db
from apps.demand.models import RDDemand, RDDemandProgress, STATUS_MAP
from datetime import datetime

blueprint = Blueprint('demand_admin', __name__, url_prefix='/demand_admin')


@blueprint.route('/list')
@login_required
def list_demands():
    """需求列表页面"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    status = request.args.get('status', type=int)
    keyword = request.args.get('keyword', '')

    query = RDDemand.query

    if status is not None:
        query = query.filter(RDDemand.status == status)

    if keyword:
        query = query.filter(
            db.or_(
                RDDemand.title.ilike(f'%{keyword}%'),
                RDDemand.demand_no.ilike(f'%{keyword}%'),
                RDDemand.submitter_name.ilike(f'%{keyword}%')
            )
        )

    pagination = query.order_by(RDDemand.submit_time.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )

    demands = pagination.items

    status_options = [
        {'value': 0, 'label': '待处理'},
        {'value': 1, 'label': '确认中'},
        {'value': 2, 'label': '研发中'},
        {'value': 3, 'label': '样品制作'},
        {'value': 4, 'label': '已完成'},
        {'value': 5, 'label': '已取消'},
    ]

    return render_template(
        'demand_admin/list.html',
        segment='demand_list',
        demands=demands,
        pagination=pagination,
        status_options=status_options,
        current_status=status,
        keyword=keyword
    )


@blueprint.route('/detail/<int:demand_id>')
@login_required
def detail(demand_id):
    """需求详情页面"""
    demand = RDDemand.query.get_or_404(demand_id)
    progress_list = RDDemandProgress.query.filter_by(demand_id=demand_id).order_by(RDDemandProgress.create_time.asc()).all()

    status_options = [
        {'value': 0, 'label': '待处理'},
        {'value': 1, 'label': '确认中'},
        {'value': 2, 'label': '研发中'},
        {'value': 3, 'label': '样品制作'},
        {'value': 4, 'label': '已完成'},
        {'value': 5, 'label': '已取消'},
    ]

    return render_template(
        'demand_admin/detail.html',
        segment='demand_list',
        demand=demand,
        progress_list=progress_list,
        status_options=status_options
    )


@blueprint.route('/update_status', methods=['POST'])
@login_required
def update_status():
    """更新需求状态"""
    demand_id = request.form.get('demand_id', type=int)
    new_status = request.form.get('status', type=int)
    remark = request.form.get('remark', '')
    operator_name = request.form.get('operator_name', '管理员')

    demand = RDDemand.query.get_or_404(demand_id)

    old_status = demand.status
    demand.status = new_status
    demand.status_text = STATUS_MAP[new_status]
    demand.update_time = datetime.now()

    if remark:
        demand.admin_remark = remark
    demand.handler_name = operator_name

    progress = RDDemandProgress(
        demand_id=demand_id,
        status=new_status,
        status_text=STATUS_MAP[new_status],
        remark=remark,
        operator_name=operator_name
    )
    db.session.add(progress)
    db.session.commit()

    return jsonify({'code': 200, 'message': '状态更新成功'})


@blueprint.route('/statistics')
@login_required
def statistics():
    """统计看板页面"""
    from sqlalchemy import func
    
    total_count = RDDemand.query.count()
    
    status_counts = db.session.query(
        RDDemand.status,
        func.count(RDDemand.id)
    ).group_by(RDDemand.status).all()
    
    status_data = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for status, count in status_counts:
        status_data[status] = count
    
    recent_demands = RDDemand.query.order_by(RDDemand.submit_time.desc()).limit(10).all()
    
    status_options = [
        {'value': 0, 'label': '待处理', 'count': status_data.get(0, 0)},
        {'value': 1, 'label': '确认中', 'count': status_data.get(1, 0)},
        {'value': 2, 'label': '研发中', 'count': status_data.get(2, 0)},
        {'value': 3, 'label': '样品制作', 'count': status_data.get(3, 0)},
        {'value': 4, 'label': '已完成', 'count': status_data.get(4, 0)},
        {'value': 5, 'label': '已取消', 'count': status_data.get(5, 0)},
    ]
    
    return render_template(
        'demand_admin/statistics.html',
        segment='demand_statistics',
        total_count=total_count,
        status_data=status_data,
        recent_demands=recent_demands,
        status_options=status_options
    )


@blueprint.route('/api/statistics')
@login_required
def get_statistics():
    """获取统计数据API"""
    from sqlalchemy import func
    
    try:
        total_count = RDDemand.query.count()
        
        status_counts = db.session.query(
            RDDemand.status,
            func.count(RDDemand.id)
        ).group_by(RDDemand.status).all()
        
        status_data = {}
        for status, count in status_counts:
            status_data[status] = count
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'totalCount': total_count,
                'statusData': status_data,
                'statusText': STATUS_MAP
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e), 'data': None})
