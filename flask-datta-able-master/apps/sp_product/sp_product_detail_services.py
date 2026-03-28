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
from apps.xp_product.models import Product
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

        product_dict = product.to_dict()

        product_dict['title'] = product_dict['name']
        product_dict['productName'] = product_dict['name']

        product_dict['subtitle'] = product_dict.get('subtitle', '')

        original_price = float(product.original_price) if product.original_price else 0
        current_price = float(product.price)
        if original_price > 0:
            discount = round(current_price / original_price * 10, 1)
        else:
            discount = 10.0
        product_dict['discount'] = str(discount)

        product_dict['saveAmount'] = round(original_price - current_price, 2) if original_price > 0 else 0

        product_dict['stock'] = product.stock if product.stock else 0
        product_dict['sales'] = product.sales if product.sales else 0

        review_count = SpProductReview.query.filter_by(
            product_id=product_id,
            is_show=1
        ).count()
        product_dict['reviews'] = review_count

        tags = []
        if product.is_hot:
            tags.append('热销')
        if product.is_new:
            tags.append('新品')
        if product.is_recommend:
            tags.append('推荐')
        if product.is_brand:
            tags.append('品牌')
        if product.is_cashback:
            tags.append('单单返现')
        if product.is_trust:
            tags.append('信任购')
        product_dict['tags'] = tags

        specs_list = []
        if product.specifications:
            specs_list = product.specifications
        if not specs_list:
            specs_list = [
                {
                    'name': '规格',
                    'values': ['默认']
                }
            ]

        product_dict['specs'] = specs_list

        product_dict['shopName'] = '立白Liby旗舰店'
        product_dict['shopLogo'] = 'https://picsum.photos/80/80?random=10'
        product_dict['shopSales'] = '6860'
        product_dict['shopScore'] = '4.84'
        product_dict['productScore'] = '4.96'
        product_dict['logisticsScore'] = '4.74'
        product_dict['serviceScore'] = '4.79'

        product_dict['darenCount'] = '4'
        product_dict['location'] = '贵州省黔南布依族苗族自治州'

        product_dict['monthSales'] = str(product.sales if product.sales else 0)
        product_dict['monthViews'] = '3166'
        product_dict['monthDaren'] = '1万'
        
        product_dict['reviewCount'] = str(review_count)
        product_dict['goodRate'] = '98'
        product_dict['reviewTags'] = ['有图/视频', '很好用', '味道好', '香味很香']
        
        product_dict['tuanzhangName'] = '飞鸽传媒团长精选'
        product_dict['tuanzhangAvatar'] = 'https://picsum.photos/80/80?random=20'
        product_dict['tuanzhangDesc'] = '聊高佣·帮申样·响应快'
        
        if user_id:
            is_favorite = SpProductFavorite.query.filter_by(
                user_id=user_id,
                product_id=product_id
            ).first() is not None
            product_dict['isFavorite'] = is_favorite
            
            # 暂时注释掉浏览记录功能，避免外键约束错误
            # SpProductDetailService.record_view(user_id, product_id)
        
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
                    'name': product.name,
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
                        'name': product.name,
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
