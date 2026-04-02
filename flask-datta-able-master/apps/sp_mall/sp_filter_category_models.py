# -*- encoding: utf-8 -*-
"""
商品商城模块 - 筛选类别模型 (用于前端分类按钮)
"""

from apps import db
from datetime import datetime


class SpFilterCategory(db.Model):
    """筛选类别表 - 用于前端商品页分类按钮"""
    __tablename__ = 'sp_filter_category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='类别ID')
    name = db.Column(db.String(50), nullable=False, comment='类别名称')
    code = db.Column(db.String(50), nullable=False, unique=True, comment='类别编码')
    sort = db.Column(db.Integer, nullable=False, default=0, comment='排序权重')
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='状态: 1启用 0禁用')
    icon = db.Column(db.String(500), nullable=True, comment='类别图标')
    color = db.Column(db.String(20), nullable=True, comment='主题颜色')
    description = db.Column(db.String(200), nullable=True, comment='类别描述')
    product_count = db.Column(db.Integer, nullable=False, default=0, comment='商品数量')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'sort': self.sort,
            'status': self.status,
            'icon': self.icon,
            'color': self.color,
            'description': self.description,
            'productCount': self.product_count,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class SpCategoryOperationLog(db.Model):
    """类别操作日志表"""
    __tablename__ = 'sp_category_operation_log'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='日志ID')
    category_id = db.Column(db.Integer, nullable=True, comment='操作的类别ID')
    operation_type = db.Column(db.String(20), nullable=False, comment='操作类型: CREATE/UPDATE/DELETE/BATCH_UPDATE/IMPORT/EXPORT')
    operator_id = db.Column(db.BigInteger, nullable=True, comment='操作人ID')
    operator_name = db.Column(db.String(100), nullable=True, comment='操作人名称')
    operator_ip = db.Column(db.String(50), nullable=True, comment='操作人IP')
    old_data = db.Column(db.Text, nullable=True, comment='操作前数据')
    new_data = db.Column(db.Text, nullable=True, comment='操作后数据')
    description = db.Column(db.String(500), nullable=True, comment='操作描述')
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='状态: 1成功 0失败')
    error_message = db.Column(db.Text, nullable=True, comment='错误信息')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='操作时间')

    __table_args__ = (
        db.Index('idx_category_id', 'category_id'),
        db.Index('idx_operation_type', 'operation_type'),
        db.Index('idx_operator_id', 'operator_id'),
        db.Index('idx_created_at', 'created_at'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'categoryId': self.category_id,
            'operationType': self.operation_type,
            'operatorId': self.operator_id,
            'operatorName': self.operator_name,
            'operatorIp': self.operator_ip,
            'oldData': self.old_data,
            'newData': self.new_data,
            'description': self.description,
            'status': self.status,
            'errorMessage': self.error_message,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
