# -*- encoding: utf-8 -*-
"""
样品申请模块 - 数据模型
"""

from apps import db
from datetime import datetime


class SampleApply(db.Model):
    """样品申请"""
    __tablename__ = 'xp_sample_apply'

    id = db.Column(db.BigInteger, primary_key=True)
    apply_no = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.BigInteger, nullable=False)
    user_name = db.Column(db.String(50))
    user_phone = db.Column(db.String(20))
    product_id = db.Column(db.BigInteger, nullable=False)
    product_name = db.Column(db.String(200))
    product_image = db.Column(db.String(500))
    quantity = db.Column(db.Integer, default=1)
    address = db.Column(db.String(500))
    remark = db.Column(db.String(500))
    status = db.Column(db.SmallInteger, default=0)
    review_remark = db.Column(db.String(500))
    review_time = db.Column(db.DateTime)
    review_by = db.Column(db.String(50))
    ship_status = db.Column(db.SmallInteger, default=0)
    ship_company = db.Column(db.String(50))
    ship_no = db.Column(db.String(50))
    ship_time = db.Column(db.DateTime)
    receive_status = db.Column(db.SmallInteger, default=0)
    receive_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'apply_no': self.apply_no,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_phone': self.user_phone,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_image': self.product_image,
            'quantity': self.quantity,
            'address': self.address,
            'remark': self.remark,
            'status': self.status,
            'status_text': self.get_status_text(),
            'review_remark': self.review_remark,
            'review_time': self.review_time.strftime('%Y-%m-%d %H:%M:%S') if self.review_time else None,
            'review_by': self.review_by,
            'ship_status': self.ship_status,
            'ship_status_text': self.get_ship_status_text(),
            'ship_company': self.ship_company,
            'ship_no': self.ship_no,
            'ship_time': self.ship_time.strftime('%Y-%m-%d %H:%M:%S') if self.ship_time else None,
            'receive_status': self.receive_status,
            'receive_time': self.receive_time.strftime('%Y-%m-%d %H:%M:%S') if self.receive_time else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

    def get_status_text(self):
        status_map = {
            0: '待审核',
            1: '审核通过',
            2: '审核拒绝',
            3: '已取消'
        }
        return status_map.get(self.status, '待审核')

    def get_ship_status_text(self):
        status_map = {
            0: '待发货',
            1: '已发货',
            2: '已签收'
        }
        return status_map.get(self.ship_status, '待发货')

    def to_api_list_dict(self):
        status_map = {0: 'pending', 1: 'approved', 2: 'rejected', 3: 'cancelled'}
        ship_status_map = {0: 'not_shipped', 1: 'shipped', 2: 'received'}
        status_text_map = {0: '待审核', 1: '审核通过', 2: '审核拒绝', 3: '已取消'}
        ship_status_text_map = {0: '未寄出', 1: '已寄出', 2: '已签收'}
        
        return {
            'id': self.apply_no,
            'applyTime': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else '',
            'status': status_map.get(self.status, 'pending'),
            'statusText': status_text_map.get(self.status, '待审核'),
            'shipStatus': ship_status_map.get(self.ship_status, 'not_shipped'),
            'shipStatusText': ship_status_text_map.get(self.ship_status, '未寄出'),
            'products': [{
                'id': str(self.product_id),
                'name': self.product_name,
                'image': self.product_image,
                'price': str(float(self.quantity) * 10) if self.product_id else '0',
                'commission': '10%'
            }] if self.product_id else []
        }

    def to_api_detail_dict(self):
        status_map = {0: 'pending', 1: 'approved', 2: 'rejected', 3: 'cancelled'}
        ship_status_map = {0: 'not_shipped', 1: 'shipped', 2: 'received'}
        status_text_map = {0: '待审核', 1: '审核通过', 2: '审核拒绝', 3: '已取消'}
        ship_status_text_map = {0: '未寄出', 1: '已寄出', 2: '已签收'}
        
        address_parts = self.address.split(',') if self.address else ['', '', '', '']
        
        return {
            'id': self.apply_no,
            'applyTime': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else '',
            'status': status_map.get(self.status, 'pending'),
            'statusText': status_text_map.get(self.status, '待审核'),
            'reviewTime': self.review_time.strftime('%Y-%m-%d %H:%M:%S') if self.review_time else None,
            'reviewRemark': self.review_remark or '',
            'shipStatus': ship_status_map.get(self.ship_status, 'not_shipped'),
            'shipStatusText': ship_status_text_map.get(self.ship_status, '未寄出'),
            'logisticsCompany': self.ship_company or '',
            'trackingNo': self.ship_no or '',
            'shipTime': self.ship_time.strftime('%Y-%m-%d %H:%M:%S') if self.ship_time else None,
            'receiveTime': self.receive_time.strftime('%Y-%m-%d %H:%M:%S') if self.receive_time else None,
            'recipient': {
                'name': self.user_name or '',
                'phone': self.user_phone or '',
                'address': self.address or ''
            },
            'products': [{
                'id': str(self.product_id),
                'name': self.product_name,
                'image': self.product_image,
                'price': str(float(self.quantity) * 10) if self.product_id else '0',
                'commission': '10%'
            }] if self.product_id else []
        }
