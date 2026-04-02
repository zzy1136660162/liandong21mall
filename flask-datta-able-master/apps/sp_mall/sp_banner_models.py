# -*- encoding: utf-8 -*-
"""
商品商城模块 - 轮播图模型
"""

from apps import db
from datetime import datetime


class SpBanner(db.Model):
    """轮播图表"""
    __tablename__ = 'sp_banner'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='轮播图ID')
    title = db.Column(db.String(100), nullable=False, comment='轮播图标题')
    image_url = db.Column(db.String(500), nullable=False, comment='轮播图URL')
    link_type = db.Column(db.String(20), nullable=False, default='none', comment='链接类型: none/product/category/url')
    link_value = db.Column(db.String(500), nullable=True, comment='链接值: 商品ID/分类ID/URL地址')
    sort = db.Column(db.Integer, nullable=False, default=0, comment='排序')
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='状态: 1启用 0禁用')
    position = db.Column(db.String(20), nullable=False, default='home', comment='位置: home首页/mall商品页')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'imageUrl': self.image_url,
            'linkType': self.link_type,
            'linkValue': self.link_value,
            'sort': self.sort,
            'status': self.status,
            'position': self.position,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
