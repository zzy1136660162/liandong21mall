# -*- encoding: utf-8 -*-
"""
研发需求模块 - 数据模型
"""

from apps import db
from datetime import datetime


class RDDemand(db.Model):
    """研发需求主表"""
    __tablename__ = 'rd_demand'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键ID')
    demand_no = db.Column(db.String(50), unique=True, nullable=False, comment='需求编号')
    title = db.Column(db.String(200), nullable=False, comment='需求标题')
    functional_appeal = db.Column(db.Text, nullable=False, comment='功能诉求')
    target_audience = db.Column(db.String(200), nullable=False, comment='目标人群')
    dosage_form_preference = db.Column(db.String(100), nullable=True, comment='剂型偏好')
    budget_range = db.Column(db.String(50), nullable=False, comment='预算范围')
    expected_delivery_time = db.Column(db.Date, nullable=False, comment='期望交付时间')
    remark = db.Column(db.Text, nullable=True, comment='备注')
    submitter_id = db.Column(db.String(50), nullable=False, comment='提交人ID')
    submitter_name = db.Column(db.String(50), nullable=True, comment='提交人姓名')
    submitter_phone = db.Column(db.String(20), nullable=True, comment='提交人电话')
    status = db.Column(db.Integer, nullable=False, default=0, comment='状态: 0-待处理 1-确认中 2-研发中 3-样品制作 4-已完成 5-已取消')
    status_text = db.Column(db.String(20), nullable=False, comment='状态文本')
    admin_remark = db.Column(db.Text, nullable=True, comment='处理备注')
    handler_name = db.Column(db.String(50), nullable=True, comment='处理人')
    submit_time = db.Column(db.DateTime, nullable=False, comment='提交时间')
    update_time = db.Column(db.DateTime, nullable=False, comment='更新时间')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')

    # 关联
    progress_records = db.relationship('RDDemandProgress', backref='demand', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'demandNo': self.demand_no,
            'title': self.title,
            'functionalAppeal': self.functional_appeal,
            'targetAudience': self.target_audience,
            'dosageFormPreference': self.dosage_form_preference,
            'budgetRange': self.budget_range,
            'expectedDeliveryTime': self.expected_delivery_time.strftime('%Y-%m-%d') if self.expected_delivery_time else None,
            'remark': self.remark,
            'submitterId': self.submitter_id,
            'submitterName': self.submitter_name,
            'submitterPhone': self.submitter_phone,
            'status': self.status,
            'statusText': self.status_text,
            'adminRemark': self.admin_remark,
            'handlerName': self.handler_name,
            'submitTime': self.submit_time.strftime('%Y-%m-%d %H:%M:%S') if self.submit_time else None,
            'updateTime': self.update_time.strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None,
        }


class RDDemandProgress(db.Model):
    """研发需求进度记录表"""
    __tablename__ = 'rd_demand_progress'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键ID')
    demand_id = db.Column(db.Integer, db.ForeignKey('rd_demand.id'), nullable=False, comment='需求ID')
    status = db.Column(db.Integer, nullable=False, comment='状态值')
    status_text = db.Column(db.String(20), nullable=False, comment='状态文本')
    remark = db.Column(db.Text, nullable=True, comment='进度备注')
    operator_name = db.Column(db.String(50), nullable=True, comment='操作人')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='创建时间')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'demandId': self.demand_id,
            'status': self.status,
            'statusText': self.status_text,
            'remark': self.remark,
            'operatorName': self.operator_name,
            'createTime': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
        }


# 状态映射
STATUS_MAP = {
    0: '待处理',
    1: '确认中',
    2: '研发中',
    3: '样品制作',
    4: '已完成',
    5: '已取消'
}
