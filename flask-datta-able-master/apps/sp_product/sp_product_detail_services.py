# -*- encoding: utf-8 -*-
"""
商品详情模块 - 业务逻辑服务
所有函数名以sp_开头，避免与其他模块冲突
"""

from apps import db
from apps.sp_product.sp_product_detail_models import (
    SpProductDetail, SpProductReview, SpProductFavorite,
    SpProductRecommendation, SpProductView
)
from apps.product.models import Product
from datetime import datetime


class SpProductDetailService:
    """商品详情服务类"""
    
    @staticmethod
    def get_product_detail(product_id, user_id=None):
        """
        获取商品详情（包含扩展信息）
        
        Args:
            product_id: 商品ID
            user_id: 用户ID（可选，用于记录浏览和收藏状态）
        
        Returns:
            dict: 商品详情数据
        """
        product = Product.query.filter_by(id=product_id, status=1).first()
        if not product:
            return None
        
        product_dict = product.to_dict(include_detail=True)
        
        detail = SpProductDetail.query.filter_by(product_id=product_id).first()
        if detail:
            product_dict.update({
                'subtitle': detail.subtitle,
                'tags': detail.tags or [],
                'specs': detail.specs or [],
                'description': detail.description,
                'videoUrl': detail.video_url
            })
        
        if detail and detail.original_price:
            product_dict['originalPrice'] = float(detail.original_price)
            product_dict['discount'] = round(float(product.price) / float(detail.original_price) * 10, 1)
            product_dict['saveAmount'] = round(float(detail.original_price) - float(product.price), 2)
        
        if product.member_price:
            product_dict['memberPrice'] = float(product.member_price)
            product_dict['saveAmount'] = round(float(product.price) - float(product.member_price), 2)
        
        if user_id:
            is_favorite = SpProductFavorite.query.filter_by(
                user_id=user_id,
                product_id=product_id
            ).first() is not None
            product_dict['isFavorite'] = is_favorite
            
            SpProductDetailService.record_view(user_id, product_id)
        
        reviews = SpProductReview.query.filter_by(
            product_id=product_id,
            is_show=1
        ).order_by(SpProductReview.created_at.desc()).limit(5).all()
        product_dict['reviewList'] = [review.to_dict() for review in reviews]
        
        recommendations = SpProductDetailService.get_recommendations(product_id, 6)
        product_dict['recommendations'] = recommendations
        
        return product_dict
    
    @staticmethod
    def get_recommendations(product_id, limit=6):
        """
        获取推荐商品
        
        Args:
            product_id: 商品ID
            limit: 返回数量
        
        Returns:
            list: 推荐商品列表
        """
        recommendations = SpProductRecommendation.query.filter_by(
            product_id=product_id
        ).order_by(SpProductRecommendation.sort.asc()).limit(limit).all()
        
        result = []
        for rec in recommendations:
            product = Product.query.filter_by(
                id=rec.recommend_product_id,
                status=1
            ).first()
            if product:
                result.append({
                    'id': product.id,
                    'name': product.product_name,
                    'image': product.main_image,
                    'price': float(product.price)
                })
        
        if len(result) < limit:
            category_id = Product.query.get(product_id).category_id if Product.query.get(product_id) else None
            if category_id:
                additional_products = Product.query.filter(
                    Product.category_id == category_id,
                    Product.id != product_id,
                    Product.status == 1
                ).order_by(Product.sales.desc()).limit(limit - len(result)).all()
                
                for product in additional_products:
                    result.append({
                        'id': product.id,
                        'name': product.product_name,
                        'image': product.main_image,
                        'price': float(product.price)
                    })
        
        return result[:limit]
    
    @staticmethod
    def record_view(user_id, product_id):
        """
        记录商品浏览
        
        Args:
            user_id: 用户ID
            product_id: 商品ID
        """
        view = SpProductView(
            user_id=user_id,
            product_id=product_id,
            view_time=datetime.now()
        )
        db.session.add(view)
        db.session.commit()
    
    @staticmethod
    def add_favorite(user_id, product_id):
        """
        添加商品收藏
        
        Args:
            user_id: 用户ID
            product_id: 商品ID
        
        Returns:
            SpProductFavorite: 收藏记录
        """
        existing = SpProductFavorite.query.filter_by(
            user_id=user_id,
            product_id=product_id
        ).first()
        
        if existing:
            return existing
        
        favorite = SpProductFavorite(
            user_id=user_id,
            product_id=product_id
        )
        db.session.add(favorite)
        db.session.commit()
        
        return favorite
    
    @staticmethod
    def remove_favorite(user_id, product_id):
        """
        取消商品收藏
        
        Args:
            user_id: 用户ID
            product_id: 商品ID
        
        Returns:
            bool: 是否成功
        """
        favorite = SpProductFavorite.query.filter_by(
            user_id=user_id,
            product_id=product_id
        ).first()
        
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def check_favorite(user_id, product_id):
        """
        检查是否已收藏
        
        Args:
            user_id: 用户ID
            product_id: 商品ID
        
        Returns:
            dict: 包含isFavorite字段
        """
        favorite = SpProductFavorite.query.filter_by(
            user_id=user_id,
            product_id=product_id
        ).first()
        
        return {
            'isFavorite': favorite is not None
        }
    
    @staticmethod
    def get_reviews(product_id, page=1, page_size=10):
        """
        获取商品评价列表
        
        Args:
            product_id: 商品ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            dict: 评价列表数据
        """
        pagination = SpProductReview.query.filter_by(
            product_id=product_id,
            is_show=1
        ).order_by(SpProductReview.created_at.desc()).paginate(
            page=page,
            per_page=page_size,
            error_out=False
        )
        
        return {
            'total': pagination.total,
            'page': page,
            'pageSize': page_size,
            'list': [review.to_dict() for review in pagination.items]
        }
    
    @staticmethod
    def add_review(user_id, product_id, order_id, rating, content, images=None, is_anonymous=False):
        """
        添加商品评价
        
        Args:
            user_id: 用户ID
            product_id: 商品ID
            order_id: 订单ID
            rating: 评分（1-5）
            content: 评价内容
            images: 评价图片列表
            is_anonymous: 是否匿名
        
        Returns:
            SpProductReview: 评价记录
        """
        review = SpProductReview(
            user_id=user_id,
            product_id=product_id,
            order_id=order_id,
            rating=rating,
            content=content,
            images=images,
            is_anonymous=1 if is_anonymous else 0
        )
        db.session.add(review)
        db.session.commit()
        
        return review
    
    @staticmethod
    def get_favorite_list(user_id, page=1, page_size=10):
        """
        获取用户收藏列表
        
        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            dict: 收藏列表数据
        """
        pagination = SpProductFavorite.query.filter_by(
            user_id=user_id
        ).order_by(SpProductFavorite.created_at.desc()).paginate(
            page=page,
            per_page=page_size,
            error_out=False
        )
        
        result = []
        for favorite in pagination.items:
            product = Product.query.filter_by(
                id=favorite.product_id,
                status=1
            ).first()
            if product:
                product_dict = product.to_dict()
                product_dict['favoriteId'] = favorite.id
                product_dict['favoriteTime'] = favorite.created_at.strftime('%Y-%m-%d %H:%M:%S')
                result.append(product_dict)
        
        return {
            'total': pagination.total,
            'page': page,
            'pageSize': page_size,
            'list': result
        }
