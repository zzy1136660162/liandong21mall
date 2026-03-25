# -*- encoding: utf-8 -*-
"""
商品详情模块 - 数据模型
所有表名以sp_开头，避免与其他模块冲突
"""

from apps import db
from datetime import datetime


class SpProductDetail(db.Model):
    """商品详情扩展表"""
    __tablename__ = 'sp_product_detail'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='详情ID')
    product_id = db.Column(db.BigInteger, db.ForeignKey('xp_products.id'), nullable=False, comment='商品ID')
    subtitle = db.Column(db.String(500), nullable=True, comment='商品副标题')
    tags = db.Column(db.JSON, nullable=True, comment='商品标签JSON数组')
    specs = db.Column(db.JSON, nullable=True, comment='商品规格JSON')
    description = db.Column(db.Text, nullable=True, comment='商品详情HTML')
    video_url = db.Column(db.String(500), nullable=True, comment='商品视频URL')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 移除直接的relationship引用，避免循环导入问题
    
    def __repr__(self):
        return f'<SpProductDetail {self.product_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'productId': self.product_id,
            'subtitle': self.subtitle,
            'tags': self.tags or [],
            'specs': self.specs or [],
            'description': self.description,
            'videoUrl': self.video_url,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }


class SpProductReview(db.Model):
    """商品评价表"""
    __tablename__ = 'sp_product_review'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='评价ID')
    product_id = db.Column(db.BigInteger, db.ForeignKey('xp_products.id'), nullable=False, comment='商品ID')
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False, comment='用户ID')
    order_id = db.Column(db.BigInteger, db.ForeignKey('order.id'), nullable=True, comment='订单ID')
    rating = db.Column(db.SmallInteger, nullable=False, default=5, comment='评分：1-5星')
    content = db.Column(db.Text, nullable=True, comment='评价内容')
    images = db.Column(db.JSON, nullable=True, comment='评价图片JSON数组')
    is_anonymous = db.Column(db.SmallInteger, nullable=False, default=0, comment='是否匿名：1是 0否')
    reply_content = db.Column(db.Text, nullable=True, comment='商家回复内容')
    reply_time = db.Column(db.DateTime, nullable=True, comment='商家回复时间')
    is_show = db.Column(db.SmallInteger, nullable=False, default=1, comment='是否显示：1是 0否')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 移除直接的relationship引用，避免循环导入问题
    
    def __repr__(self):
        return f'<SpProductReview {self.id}:{self.product_id}>'
    
    def to_dict(self):
        user_name = '匿名用户' if self.is_anonymous == 1 else (self.user.username if self.user else '用户')
        user_avatar = self.user.avatar if self.user and self.is_anonymous == 0 else '/static/images/user/default-avatar.png'
        
        return {
            'id': self.id,
            'productId': self.product_id,
            'userId': self.user_id,
            'orderId': self.order_id,
            'name': user_name,
            'avatar': user_avatar,
            'rating': self.rating,
            'content': self.content,
            'images': self.images or [],
            'isAnonymous': self.is_anonymous == 1,
            'replyContent': self.reply_content,
            'replyTime': self.reply_time.strftime('%Y-%m-%d %H:%M:%S') if self.reply_time else None,
            'date': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class SpProductFavorite(db.Model):
    """商品收藏表"""
    __tablename__ = 'sp_product_favorite'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='收藏ID')
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False, comment='用户ID')
    product_id = db.Column(db.BigInteger, db.ForeignKey('xp_products.id'), nullable=False, comment='商品ID')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    
    user = db.relationship('User', backref='sp_product_favorites')
    # 移除直接的product relationship引用，避免循环导入问题
    
    def __repr__(self):
        return f'<SpProductFavorite {self.user_id}:{self.product_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'productId': self.product_id,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class SpProductRecommendation(db.Model):
    """商品推荐表"""
    __tablename__ = 'sp_product_recommendation'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='推荐ID')
    product_id = db.Column(db.BigInteger, db.ForeignKey('xp_products.id'), nullable=False, comment='商品ID')
    recommend_product_id = db.Column(db.BigInteger, db.ForeignKey('xp_products.id'), nullable=False, comment='推荐商品ID')
    sort = db.Column(db.Integer, nullable=False, default=0, comment='排序')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    
    # 移除直接的relationship引用，避免循环导入问题
    
    def __repr__(self):
        return f'<SpProductRecommendation {self.product_id}:{self.recommend_product_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'productId': self.product_id,
            'recommendProductId': self.recommend_product_id,
            'sort': self.sort,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class SpProductView(db.Model):
    """商品浏览记录表"""
    __tablename__ = 'sp_product_view'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='浏览ID')
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False, comment='用户ID')
    product_id = db.Column(db.BigInteger, db.ForeignKey('xp_products.id'), nullable=False, comment='商品ID')
    view_time = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='浏览时间')
    
    user = db.relationship('User', backref='sp_product_views')
    # 移除直接的product relationship引用，避免循环导入问题
    
    def __repr__(self):
        return f'<SpProductView {self.user_id}:{self.product_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'productId': self.product_id,
            'viewTime': self.view_time.strftime('%Y-%m-%d %H:%M:%S') if self.view_time else None
        }
