# -*- encoding: utf-8 -*-
"""
商品详情模块 - REST API
所有接口路径以sp_开头，避免与其他模块冲突
"""

from flask import request
from flask_restx import Namespace, Resource
from apps.sp_product.sp_product_detail_services import SpProductDetailService


sp_product_detail_ns = Namespace('sp_product_detail', description='商品详情API')


def success_response(data=None, message='success'):
    return {'code': 200, 'message': message, 'data': data}


def error_response(message, code=500):
    return {'code': code, 'message': message, 'data': None}


def get_current_user_id():
    """获取当前用户ID"""
    user_id = request.headers.get('X-User-Id')
    if user_id:
        try:
            return int(user_id)
        except:
            pass
    return 1


@sp_product_detail_ns.route('/detail')
class SpProductDetailAPI(Resource):
    @sp_product_detail_ns.doc('获取商品详情')
    def get(self):
        """获取商品详情"""
        product_id = request.args.get('productId', type=int)
        user_id = get_current_user_id()
        
        if not product_id:
            return error_response('商品ID不能为空')
        
        product = SpProductDetailService.get_product_detail(product_id, user_id)
        
        if not product:
            return error_response('商品不存在', 404)
        
        return success_response(product)


@sp_product_detail_ns.route('/favorite/add')
class SpFavoriteAddAPI(Resource):
    @sp_product_detail_ns.doc('添加商品收藏')
    def post(self):
        """添加商品收藏"""
        user_id = get_current_user_id()
        data = request.get_json()
        
        product_id = data.get('productId')
        
        if not product_id:
            return error_response('商品ID不能为空')
        
        favorite = SpProductDetailService.add_favorite(user_id, product_id)
        return success_response(favorite.to_dict(), '添加成功')


@sp_product_detail_ns.route('/favorite/remove')
class SpFavoriteRemoveAPI(Resource):
    @sp_product_detail_ns.doc('取消商品收藏')
    def post(self):
        """取消商品收藏"""
        user_id = get_current_user_id()
        data = request.get_json()
        
        product_id = data.get('productId')
        
        if not product_id:
            return error_response('商品ID不能为空')
        
        result = SpProductDetailService.remove_favorite(user_id, product_id)
        
        if not result:
            return error_response('收藏不存在')
        
        return success_response(None, '取消成功')


@sp_product_detail_ns.route('/favorite/check')
class SpFavoriteCheckAPI(Resource):
    @sp_product_detail_ns.doc('检查商品收藏状态')
    def get(self):
        """检查商品收藏状态"""
        user_id = get_current_user_id()
        product_id = request.args.get('productId', type=int)
        
        if not product_id:
            return error_response('商品ID不能为空')
        
        result = SpProductDetailService.check_favorite(user_id, product_id)
        return success_response(result)


@sp_product_detail_ns.route('/reviews')
class SpProductReviewsAPI(Resource):
    @sp_product_detail_ns.doc('获取商品评价列表')
    def get(self):
        """获取商品评价列表"""
        product_id = request.args.get('productId', type=int)
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        if not product_id:
            return error_response('商品ID不能为空')
        
        result = SpProductDetailService.get_reviews(product_id, page, page_size)
        return success_response(result)


@sp_product_detail_ns.route('/review/add')
class SpReviewAddAPI(Resource):
    @sp_product_detail_ns.doc('添加商品评价')
    def post(self):
        """添加商品评价"""
        user_id = get_current_user_id()
        data = request.get_json()
        
        product_id = data.get('productId')
        order_id = data.get('orderId')
        rating = data.get('rating')
        content = data.get('content')
        images = data.get('images')
        is_anonymous = data.get('isAnonymous', False)
        
        if not product_id:
            return error_response('商品ID不能为空')
        
        if not rating or rating < 1 or rating > 5:
            return error_response('评分必须在1-5之间')
        
        if not content:
            return error_response('评价内容不能为空')
        
        review = SpProductDetailService.add_review(
            user_id=user_id,
            product_id=product_id,
            order_id=order_id,
            rating=rating,
            content=content,
            images=images,
            is_anonymous=is_anonymous
        )
        
        return success_response(review.to_dict(), '评价成功')


@sp_product_detail_ns.route('/favorite/list')
class SpFavoriteListAPI(Resource):
    @sp_product_detail_ns.doc('获取用户收藏列表')
    def get(self):
        """获取用户收藏列表"""
        user_id = get_current_user_id()
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        result = SpProductDetailService.get_favorite_list(user_id, page, page_size)
        return success_response(result)
