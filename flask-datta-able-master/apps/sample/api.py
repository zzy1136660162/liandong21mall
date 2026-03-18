# -*- encoding: utf-8 -*-
"""
样品申请模块 - API
"""

from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from apps import db
from apps.sample.models import SampleApply
from apps.product.models import Product
from datetime import datetime

api = Namespace('sample', description='样品申请模块')

SampleApplyModel = api.model('SampleApply', {
    'id': fields.Integer,
    'apply_no': fields.String,
    'user_name': fields.String,
    'product_name': fields.String,
    'status': fields.Integer,
})


@api.route('')
class SampleListAPI(Resource):
    """获取样品申请列表 - GET /api/sample/samples"""
    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        status = request.args.get('status', '')
        
        query = SampleApply.query

        if status and status != 'all':
            status_map = {'pending': 0, 'approved': 1, 'rejected': 2, 'shipped': 1, 'received': 2}
            if status in status_map:
                if status == 'shipped':
                    query = query.filter(SampleApply.status == 1, SampleApply.ship_status == 1)
                elif status == 'received':
                    query = query.filter(SampleApply.ship_status == 2)
                else:
                    query = query.filter(SampleApply.status == status_map[status])

        pagination = query.order_by(SampleApply.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )

        return {
            'code': 200,
            'message': 'success',
            'data': {
                'total': pagination.total,
                'page': page,
                'pageSize': page_size,
                'list': [p.to_api_list_dict() for p in pagination.items]
            }
        }


@api.route('/apply')
class SampleApplyAPI(Resource):
    """提交样品申请 - POST /api/sample/samples/apply"""
    def post(self):
        data = request.get_json()
        
        product_ids = data.get('productIds', [])
        recipient_name = data.get('recipientName')
        phone = data.get('phone')
        province = data.get('province', '')
        city = data.get('city', '')
        district = data.get('district', '')
        address = data.get('address')
        remark = data.get('remark', '')
        
        if not product_ids:
            return {'code': 400, 'message': '请选择申请的商品'}, 400
        if not recipient_name or not phone or not address:
            return {'code': 400, 'message': '请填写完整的收货信息'}, 400
        
        full_address = f'{province}{city}{district}{address}'
        
        apply_list = []
        for product_id in product_ids[:3]:
            product = Product.query.get(product_id)
            if not product:
                continue
            
            import time
            apply_no = f'SA{int(time.time() * 1000)}'
            
            apply = SampleApply(
                apply_no=apply_no,
                user_id=1,
                user_name=recipient_name,
                user_phone=phone,
                product_id=product.id,
                product_name=product.name,
                product_image=product.main_image,
                quantity=1,
                address=full_address,
                remark=remark,
                status=0,
                ship_status=0
            )
            db.session.add(apply)
            apply_list.append(apply_no)
        
        db.session.commit()
        
        return {
            'code': 200,
            'message': '申请提交成功',
            'data': {
                'applicationId': apply_list[0] if apply_list else '',
                'status': 'pending',
                'applyTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }


@api.route('/<string:apply_no>')
class SampleDetailAPI(Resource):
    """获取样品申请详情 - GET /api/sample/samples/{id}"""
    def get(self, apply_no):
        apply = SampleApply.query.filter_by(apply_no=apply_no).first()
        if not apply:
            return {'code': 404, 'message': '申请不存在'}, 404
        
        return {
            'code': 200,
            'message': 'success',
            'data': apply.to_api_detail_dict()
        }


@api.route('/<string:apply_no>/receive')
class SampleReceiveAPI(Resource):
    """确认收货 - POST /api/sample/samples/{id}/receive"""
    def post(self, apply_no):
        apply = SampleApply.query.filter_by(apply_no=apply_no).first()
        if not apply:
            return {'code': 404, 'message': '申请不存在'}, 404
        
        if apply.ship_status != 1:
            return {'code': 400, 'message': '该申请尚未发货'}, 400
        
        apply.ship_status = 2
        apply.receive_time = datetime.now()
        db.session.commit()
        
        return {
            'code': 200,
            'message': '确认收货成功',
            'data': {
                'id': apply_no,
                'shipStatus': 'received',
                'receiveTime': apply.receive_time.strftime('%Y-%m-%d %H:%M:%S')
            }
        }


@api.route('/apply/list')
class SampleApplyDetail(Resource):
    def get(self, id):
        apply = SampleApply.query.get_or_404(id)
        return {'code': 200, 'message': 'success', 'data': apply.to_dict()}


@api.route('/review')
class SampleReview(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)

        query = SampleApply.query.filter_by(status=0)

        pagination = query.order_by(SampleApply.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )

        return {
            'code': 200,
            'message': 'success',
            'data': {
                'list': [p.to_dict() for p in pagination.items],
                'total': pagination.total,
                'page': page,
                'page_size': page_size
            }
        }

    def post(self):
        data = request.get_json()
        apply_id = data.get('id')
        action = data.get('action')
        remark = data.get('remark', '')

        if not apply_id:
            return {'code': 400, 'message': '申请ID不能为空'}, 400

        apply = SampleApply.query.get_or_404(apply_id)

        if action == 'pass':
            apply.status = 1
            apply.review_remark = remark
        elif action == 'reject':
            apply.status = 2
            apply.review_remark = remark
        else:
            return {'code': 400, 'message': '无效的操作'}, 400

        apply.review_time = db.func.now()
        db.session.commit()

        return {'code': 200, 'message': '审核成功', 'data': apply.to_dict()}


@api.route('/ship')
class SampleShip(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)

        query = SampleApply.query.filter_by(status=1, ship_status=0)

        pagination = query.order_by(SampleApply.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )

        return {
            'code': 200,
            'message': 'success',
            'data': {
                'list': [p.to_dict() for p in pagination.items],
                'total': pagination.total,
                'page': page,
                'page_size': page_size
            }
        }

    def post(self):
        data = request.get_json()
        apply_id = data.get('id')
        ship_company = data.get('ship_company', '')
        ship_no = data.get('ship_no', '')

        if not apply_id:
            return {'code': 400, 'message': '申请ID不能为空'}, 400

        apply = SampleApply.query.get_or_404(apply_id)

        if apply.status != 1:
            return {'code': 400, 'message': '只有审核通过的申请才能发货'}, 400

        apply.ship_status = 1
        apply.ship_company = ship_company
        apply.ship_no = ship_no
        apply.ship_time = db.func.now()

        db.session.commit()

        return {'code': 200, 'message': '发货成功', 'data': apply.to_dict()}


@api.route('/status')
class SampleStatus(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        status = request.args.get('status', None, type=int)
        ship_status = request.args.get('ship_status', None, type=int)

        query = SampleApply.query

        if status is not None and status != '':
            query = query.filter(SampleApply.status == status)
        if ship_status is not None and ship_status != '':
            query = query.filter(SampleApply.ship_status == ship_status)

        pagination = query.order_by(SampleApply.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )

        return {
            'code': 200,
            'message': 'success',
            'data': {
                'list': [p.to_dict() for p in pagination.items],
                'total': pagination.total,
                'page': page,
                'page_size': page_size
            }
        }

    def put(self):
        data = request.get_json()
        apply_id = data.get('id')

        if not apply_id:
            return {'code': 400, 'message': '申请ID不能为空'}, 400

        apply = SampleApply.query.get_or_404(apply_id)

        if 'status' in data:
            apply.status = data['status']
        if 'review_remark' in data:
            apply.review_remark = data['review_remark']
        if 'ship_status' in data:
            apply.ship_status = data['ship_status']
            if data['ship_status'] == 2:
                apply.receive_time = db.func.now()
        if 'ship_company' in data:
            apply.ship_company = data['ship_company']
        if 'ship_no' in data:
            apply.ship_no = data['ship_no']

        db.session.commit()

        return {'code': 200, 'message': '更新成功', 'data': apply.to_dict()}


@api.route('/batch-review')
class SampleBatchReview(Resource):
    def post(self):
        data = request.get_json()
        ids = data.get('ids', [])
        action = data.get('action')
        remark = data.get('remark', '')

        if not ids:
            return {'code': 400, 'message': '请选择要审核的申请'}, 400

        status_value = 1 if action == 'pass' else 2

        SampleApply.query.filter(SampleApply.id.in_(ids)).update({
            SampleApply.status: status_value,
            SampleApply.review_remark: remark,
            SampleApply.review_time: db.func.now()
        }, synchronize_session=False)

        db.session.commit()

        return {'code': 200, 'message': '批量审核成功'}


@api.route('/batch-ship')
class SampleBatchShip(Resource):
    def post(self):
        data = request.get_json()
        ids = data.get('ids', [])
        ship_company = data.get('ship_company', '')
        ship_no = data.get('ship_no', '')

        if not ids:
            return {'code': 400, 'message': '请选择要发货的申请'}, 400

        SampleApply.query.filter(SampleApply.id.in_(ids), SampleApply.status == 1).update({
            SampleApply.ship_status: 1,
            SampleApply.ship_company: ship_company,
            SampleApply.ship_no: ship_no,
            SampleApply.ship_time: db.func.now()
        }, synchronize_session=False)

        db.session.commit()

        return {'code': 200, 'message': '批量发货成功'}


@api.route('/export')
class SampleExport(Resource):
    def get(self):
        query = SampleApply.query.order_by(SampleApply.created_at.desc()).all()

        data = []
        for apply in query:
            data.append({
                '申请单号': apply.apply_no,
                '申请人': apply.user_name,
                '联系电话': apply.user_phone,
                '商品名称': apply.product_name,
                '申请数量': apply.quantity,
                '收货地址': apply.address,
                '审核状态': apply.get_status_text(),
                '发货状态': apply.get_ship_status_text(),
                '物流公司': apply.ship_company,
                '物流单号': apply.ship_no,
                '申请时间': apply.created_at.strftime('%Y-%m-%d %H:%M:%S') if apply.created_at else ''
            })

        return {
            'code': 200,
            'message': 'success',
            'data': data
        }
