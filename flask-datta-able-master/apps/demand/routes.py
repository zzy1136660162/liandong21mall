# -*- encoding: utf-8 -*-
"""
研发需求模块 - API路由
"""

from flask import Blueprint, request, jsonify
from apps import db
from apps.demand.models import RDDemand, RDDemandProgress, STATUS_MAP
from datetime import datetime
import random

blueprint = Blueprint('demand', __name__, url_prefix='/demand')


def generate_demand_no():
    """生成需求编号"""
    now = datetime.now()
    random_num = random.randint(1000, 9999)
    return f"RD{now.strftime('%Y%m%d')}{random_num}"


def success_response(data=None, message='success'):
    """成功响应"""
    return jsonify({
        'code': 200,
        'message': message,
        'data': data
    })


def error_response(message='error', code=500):
    """错误响应"""
    return jsonify({
        'code': code,
        'message': message,
        'data': None
    })


@blueprint.route('/submit', methods=['POST'])
def submit_demand():
    """提交研发需求"""
    try:
        data = request.get_json()
        
        # 必填字段验证
        required_fields = ['title', 'functionalAppeal', 'targetAudience', 'budgetRange', 'expectedDeliveryTime']
        for field in required_fields:
            if not data.get(field):
                return error_response(f'缺少必填字段: {field}')
        
        # 生成需求编号
        demand_no = generate_demand_no()
        
        # 创建需求
        now = datetime.now()
        demand = RDDemand(
            demand_no=demand_no,
            title=data.get('title'),
            functional_appeal=data.get('functionalAppeal'),
            target_audience=data.get('targetAudience'),
            dosage_form_preference=data.get('dosageFormPreference'),
            budget_range=data.get('budgetRange'),
            expected_delivery_time=datetime.strptime(data.get('expectedDeliveryTime'), '%Y-%m-%d'),
            remark=data.get('remark'),
            submitter_id=data.get('submitterId', 'USER_DEFAULT'),
            submitter_name=data.get('submitterName'),
            submitter_phone=data.get('submitterPhone'),
            status=0,
            status_text=STATUS_MAP[0],
            submit_time=now,
            update_time=now
        )
        db.session.add(demand)
        db.session.flush()
        
        # 添加进度记录
        progress = RDDemandProgress(
            demand_id=demand.id,
            status=0,
            status_text=STATUS_MAP[0],
            remark='需求已提交',
            operator_name='系统'
        )
        db.session.add(progress)
        
        db.session.commit()
        
        return success_response({
            'id': demand.id,
            'demandNo': demand.demand_no
        }, '提交成功')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'提交失败: {str(e)}')


@blueprint.route('/list', methods=['GET'])
def get_demand_list():
    """查询需求列表"""
    try:
        submitter_id = request.args.get('submitterId')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', 10))
        status = request.args.get('status')
        
        # 构建查询
        query = RDDemand.query
        
        if submitter_id:
            query = query.filter(RDDemand.submitter_id == submitter_id)
        
        if status is not None and status != '':
            query = query.filter(RDDemand.status == int(status))
        
        # 排序
        query = query.order_by(RDDemand.submit_time.desc())
        
        # 分页
        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        
        # 转换为列表
        demand_list = []
        for item in pagination.items:
            demand_list.append({
                'id': item.id,
                'demandNo': item.demand_no,
                'title': item.title,
                'targetAudience': item.target_audience,
                'budgetRange': item.budget_range,
                'expectedDeliveryTime': item.expected_delivery_time.strftime('%Y-%m-%d') if item.expected_delivery_time else None,
                'status': item.status,
                'statusText': item.status_text,
                'submitTime': item.submit_time.strftime('%Y-%m-%d %H:%M:%S') if item.submit_time else None,
                'statusClass': get_status_class(item.status),
                'submitterId': item.submitter_id
            })
        
        return success_response({
            'list': demand_list,
            'total': pagination.total,
            'page': page,
            'pageSize': page_size
        })
        
    except Exception as e:
        return error_response(f'查询失败: {str(e)}')


@blueprint.route('/detail/<int:demand_id>', methods=['GET'])
def get_demand_detail(demand_id):
    """查询需求详情"""
    try:
        submitter_id = request.args.get('submitterId')
        
        demand = RDDemand.query.get(demand_id)
        if not demand:
            return error_response('需求不存在', 404)
        
        # 权限验证（可选）
        # if submitter_id and demand.submitter_id != submitter_id:
        #     return error_response('无权限查看', 403)
        
        return success_response(demand.to_dict())
        
    except Exception as e:
        return error_response(f'查询失败: {str(e)}')


@blueprint.route('/progress/<int:demand_id>', methods=['GET'])
def get_demand_progress(demand_id):
    """查询需求进度"""
    try:
        progress_list = RDDemandProgress.query.filter_by(demand_id=demand_id).order_by(RDDemandProgress.create_time.asc()).all()
        
        return success_response([p.to_dict() for p in progress_list])
        
    except Exception as e:
        return error_response(f'查询失败: {str(e)}')


@blueprint.route('/update', methods=['POST'])
def update_demand_status():
    """更新需求状态（后台）"""
    try:
        data = request.get_json()
        demand_id = data.get('demandId')
        status = data.get('status')
        status_text = data.get('statusText')
        admin_remark = data.get('adminRemark')
        handler_name = data.get('handlerName')
        
        if not demand_id or status is None:
            return error_response('缺少必填参数')
        
        demand = RDDemand.query.get(demand_id)
        if not demand:
            return error_response('需求不存在', 404)
        
        # 更新需求状态
        demand.status = status
        demand.status_text = status_text or STATUS_MAP.get(status, '未知')
        demand.admin_remark = admin_remark
        demand.handler_name = handler_name
        demand.update_time = datetime.now()
        
        # 添加进度记录
        progress = RDDemandProgress(
            demand_id=demand_id,
            status=status,
            status_text=demand.status_text,
            remark=admin_remark or f'状态变更为{demand.status_text}',
            operator_name=handler_name or '管理员'
        )
        db.session.add(progress)
        
        db.session.commit()
        
        return success_response(None, '更新成功')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'更新失败: {str(e)}')


@blueprint.route('/withdraw', methods=['POST'])
def withdraw_demand():
    """撤回需求"""
    try:
        data = request.get_json()
        demand_id = data.get('demandId')
        submitter_id = data.get('submitterId')
        
        if not demand_id:
            return error_response('缺少必填参数')
        
        demand = RDDemand.query.get(demand_id)
        if not demand:
            return error_response('需求不存在', 404)
        
        # 验证状态（只有待处理状态可以撤回）
        if demand.status != 0:
            return error_response('该需求状态不允许撤回')
        
        # 验证提交人
        if submitter_id and demand.submitter_id != submitter_id:
            return error_response('无权限操作')
        
        # 更新状态为已取消
        demand.status = 5
        demand.status_text = STATUS_MAP[5]
        demand.update_time = datetime.now()
        
        # 添加进度记录
        progress = RDDemandProgress(
            demand_id=demand_id,
            status=5,
            status_text=STATUS_MAP[5],
            remark='用户撤回需求',
            operator_name='系统'
        )
        db.session.add(progress)
        
        db.session.commit()
        
        return success_response(None, '撤回成功')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'撤回失败: {str(e)}')


@blueprint.route('/reapply', methods=['POST'])
def reapply_demand():
    """重新申请"""
    try:
        data = request.get_json()
        demand_id = data.get('demandId')
        submitter_id = data.get('submitterId')
        
        if not demand_id:
            return error_response('缺少必填参数')
        
        demand = RDDemand.query.get(demand_id)
        if not demand:
            return error_response('需求不存在', 404)
        
        # 验证状态（只有已取消状态可以重新申请）
        if demand.status != 5:
            return error_response('该需求状态不允许重新申请')
        
        # 验证提交人
        if submitter_id and demand.submitter_id != submitter_id:
            return error_response('无权限操作')
        
        # 生成新的需求编号
        new_demand_no = generate_demand_no()
        
        # 更新需求
        demand.demand_no = new_demand_no
        demand.status = 0
        demand.status_text = STATUS_MAP[0]
        demand.admin_remark = None
        demand.handler_name = None
        demand.update_time = datetime.now()
        
        # 添加进度记录
        progress = RDDemandProgress(
            demand_id=demand_id,
            status=0,
            status_text=STATUS_MAP[0],
            remark='用户重新申请',
            operator_name='系统'
        )
        db.session.add(progress)
        
        db.session.commit()
        
        return success_response({
            'demandNo': new_demand_no
        }, '重新申请成功')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'重新申请失败: {str(e)}')


@blueprint.route('/delete', methods=['POST'])
def delete_demand():
    """删除需求"""
    try:
        data = request.get_json()
        demand_id = data.get('demandId')
        submitter_id = data.get('submitterId')
        
        if not demand_id:
            return error_response('缺少必填参数')
        
        demand = RDDemand.query.get(demand_id)
        if not demand:
            return error_response('需求不存在', 404)
        
        # 验证状态（只有已取消状态可以删除）
        if demand.status != 5:
            return error_response('该需求状态不允许删除')
        
        # 验证提交人
        if submitter_id and demand.submitter_id != submitter_id:
            return error_response('无权限操作')
        
        # 删除需求（级联删除进度记录）
        db.session.delete(demand)
        db.session.commit()
        
        return success_response(None, '删除成功')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'删除失败: {str(e)}')


@blueprint.route('/statistics', methods=['GET'])
def get_statistics():
    """获取统计数据（后台）"""
    try:
        total = RDDemand.query.count()
        pending = RDDemand.query.filter_by(status=0).count()
        confirming = RDDemand.query.filter_by(status=1).count()
        developing = RDDemand.query.filter_by(status=2).count()
        sampling = RDDemand.query.filter_by(status=3).count()
        completed = RDDemand.query.filter_by(status=4).count()
        cancelled = RDDemand.query.filter_by(status=5).count()
        
        return success_response({
            'total': total,
            'pending': pending,
            'confirming': confirming,
            'developing': developing,
            'sampling': sampling,
            'completed': completed,
            'cancelled': cancelled
        })
        
    except Exception as e:
        return error_response(f'查询失败: {str(e)}')


def get_status_class(status):
    """获取状态样式类名"""
    class_map = {
        0: 'pending',
        1: 'confirming',
        2: 'developing',
        3: 'sampling',
        4: 'completed',
        5: 'cancelled'
    }
    return class_map.get(status, 'pending')


@blueprint.route('/test', methods=['GET'])
def test_connection():
    """测试连接"""
    try:
        from apps import db
        from apps.demand.models import RDDemand
        count = RDDemand.query.count()
        return success_response({
            'status': 'ok',
            'demand_count': count,
            'message': '后端连接正常'
        })
    except Exception as e:
        return error_response(f'连接测试失败: {str(e)}')
