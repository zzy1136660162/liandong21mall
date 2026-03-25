# -*- encoding: utf-8 -*-
"""
商品商城模块 - REST API (sp_前缀)
成员1负责：商品、购物车、订单、地址
"""

from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, fields
from apps.sp_mall.sp_services import (
    SpProductService, SpCartService, 
    SpOrderService, SpAddressService
)
from apps import db

api = Namespace('sp_mall', description='商品商城模块API')

sp_product_ns = Namespace('product', description='商品API')
sp_category_ns = Namespace('category', description='商品分类API')
sp_cart_ns = Namespace('cart', description='购物车API')
sp_order_ns = Namespace('order', description='订单API')
sp_address_ns = Namespace('address', description='地址API')


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


# ========== 商品分类相关API ==========

@sp_category_ns.route('/list')
class SpCategoryList(Resource):
    @sp_category_ns.doc('获取商品分类列表')
    def get(self):
        """获取所有商品分类"""
        categories = SpProductService.get_categories()
        return success_response(categories)


@sp_category_ns.route('/<int:category_id>')
class SpCategoryDetail(Resource):
    @sp_category_ns.doc('获取分类详情')
    def get(self, category_id):
        """根据ID获取分类详情"""
        category = SpProductService.get_category_by_id(category_id)
        
        if not category:
            return error_response('分类不存在', 404)
        
        return success_response(category)


# ========== 商品相关API ==========

@sp_product_ns.route('/list')
class SpProductList(Resource):
    @sp_product_ns.doc('获取商品列表')
    def get(self):
        """获取商品列表"""
        category_id = request.args.get('categoryId', type=int)
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        keyword = request.args.get('keyword')
        
        result = SpProductService.get_products(category_id, page, page_size, keyword)
        return success_response(result)


@sp_product_ns.route('/<int:product_id>')
class SpProductDetail(Resource):
    @sp_product_ns.doc('获取商品详情')
    def get(self, product_id):
        """根据ID获取商品详情"""
        product = SpProductService.get_product_by_id(product_id)
        
        if not product:
            return error_response('商品不存在', 404)
        
        return success_response(product)


@sp_product_ns.route('/hot')
class SpHotProducts(Resource):
    @sp_product_ns.doc('获取热销商品')
    def get(self):
        """获取热销商品"""
        limit = request.args.get('limit', 10, type=int)
        products = SpProductService.get_hot_products(limit)
        return success_response(products)


@sp_product_ns.route('/new')
class SpNewProducts(Resource):
    @sp_product_ns.doc('获取新品商品')
    def get(self):
        """获取新品商品"""
        limit = request.args.get('limit', 10, type=int)
        products = SpProductService.get_new_products(limit)
        return success_response(products)


@sp_product_ns.route('/recommend')
class SpRecommendProducts(Resource):
    @sp_product_ns.doc('获取推荐商品')
    def get(self):
        """获取推荐商品"""
        limit = request.args.get('limit', 10, type=int)
        products = SpProductService.get_recommend_products(limit)
        return success_response(products)


@sp_product_ns.route('/search')
class SpSearchProducts(Resource):
    @sp_product_ns.doc('搜索商品')
    def get(self):
        """搜索商品"""
        keyword = request.args.get('keyword')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        if not keyword:
            return error_response('请输入搜索关键词')
        
        result = SpProductService.search_products(keyword, page, page_size)
        return success_response(result)


# ========== 购物车相关API ==========

@sp_cart_ns.route('/list')
class SpCartList(Resource):
    @sp_cart_ns.doc('获取购物车列表')
    def get(self):
        """获取用户购物车列表"""
        user_id = get_current_user_id()
        cart_items = SpCartService.get_cart_list(user_id)
        return success_response(cart_items)


@sp_cart_ns.route('/add')
class SpCartAdd(Resource):
    @sp_cart_ns.doc('添加商品到购物车')
    def post(self):
        """添加商品到购物车"""
        user_id = get_current_user_id()
        data = request.get_json()
        
        product_id = data.get('productId')
        sku_id = data.get('skuId')
        quantity = data.get('quantity', 1)
        
        if not product_id:
            return error_response('请选择商品')
        
        if quantity <= 0:
            return error_response('商品数量必须大于0')
        
        cart_item = SpCartService.add_to_cart(user_id, product_id, sku_id, quantity)
        return success_response(cart_item, '添加成功')


@sp_cart_ns.route('/update/<int:cart_id>')
class SpCartUpdate(Resource):
    @sp_cart_ns.doc('更新购物车商品数量')
    def put(self, cart_id):
        """更新购物车商品数量"""
        user_id = get_current_user_id()
        data = request.get_json()
        quantity = data.get('quantity', 1)
        
        cart_item = SpCartService.update_cart_quantity(cart_id, user_id, quantity)
        
        if not cart_item:
            return error_response('购物车商品不存在')
        
        return success_response(cart_item, '更新成功')


@sp_cart_ns.route('/select/<int:cart_id>')
class SpCartSelect(Resource):
    @sp_cart_ns.doc('更新购物车商品选中状态')
    def put(self, cart_id):
        """更新购物车商品选中状态"""
        user_id = get_current_user_id()
        data = request.get_json()
        selected = data.get('selected', True)
        
        cart_item = SpCartService.update_cart_selected(cart_id, user_id, selected)
        
        if not cart_item:
            return error_response('购物车商品不存在')
        
        return success_response(cart_item, '更新成功')


@sp_cart_ns.route('/delete/<int:cart_id>')
class SpCartDelete(Resource):
    @sp_cart_ns.doc('删除购物车商品')
    def delete(self, cart_id):
        """删除购物车商品"""
        user_id = get_current_user_id()
        
        result = SpCartService.delete_cart_item(cart_id, user_id)
        
        if not result:
            return error_response('购物车商品不存在')
        
        return success_response(None, '删除成功')


@sp_cart_ns.route('/clear')
class SpCartClear(Resource):
    @sp_cart_ns.doc('清空购物车')
    def delete(self):
        """清空购物车"""
        user_id = get_current_user_id()
        SpCartService.clear_cart(user_id)
        return success_response(None, '清空成功')


@sp_cart_ns.route('/total')
class SpCartTotal(Resource):
    @sp_cart_ns.doc('获取购物车总金额')
    def get(self):
        """获取购物车选中商品总金额"""
        user_id = get_current_user_id()
        total = SpCartService.get_cart_total(user_id)
        return success_response({'total': total})


# ========== 订单相关API ==========

@sp_order_ns.route('/create')
class SpOrderCreate(Resource):
    @sp_order_ns.doc('创建订单')
    def post(self):
        """创建订单"""
        user_id = get_current_user_id()
        data = request.get_json()
        
        order, message = SpOrderService.create_order(user_id, data)
        
        if not order:
            return error_response(message)
        
        return success_response(order, message)


@sp_order_ns.route('/list')
class SpOrderList(Resource):
    @sp_order_ns.doc('获取订单列表')
    def get(self):
        """获取用户订单列表"""
        user_id = get_current_user_id()
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        result = SpOrderService.get_order_list(user_id, status, page, page_size)
        return success_response(result)


@sp_order_ns.route('/detail/<int:order_id>')
class SpOrderDetail(Resource):
    @sp_order_ns.doc('获取订单详情')
    def get(self, order_id):
        """根据ID获取订单详情"""
        user_id = get_current_user_id()
        order = SpOrderService.get_order_by_id(order_id, user_id)
        
        if not order:
            return error_response('订单不存在', 404)
        
        # 添加剩余支付时间
        if order.get('status') == 'PENDING_PAY':
            remaining_seconds = SpOrderService.get_order_expire_time(order_id)
            order['remainingSeconds'] = remaining_seconds
            order['expireTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if remaining_seconds > 0 else None
        
        return success_response(order)


@sp_order_ns.route('/expire-time/<int:order_id>')
class SpOrderExpireTime(Resource):
    @sp_order_ns.doc('获取订单剩余支付时间')
    def get(self, order_id):
        """获取订单剩余支付时间"""
        user_id = get_current_user_id()
        order = SpOrderService.get_order_by_id(order_id, user_id)
        
        if not order:
            return error_response('订单不存在', 404)
        
        remaining_seconds = SpOrderService.get_order_expire_time(order_id)
        
        return success_response({
            'remainingSeconds': remaining_seconds,
            'expired': remaining_seconds <= 0
        })


@sp_order_ns.route('/count')
class SpOrderCount(Resource):
    @sp_order_ns.doc('获取订单数量统计')
    def get(self):
        """获取用户各状态订单数量"""
        user_id = get_current_user_id()
        
        from apps.sp_mall.sp_models import SpOrder
        
        # 统计各状态订单数量
        counts = {
            'pending': SpOrder.query.filter_by(user_id=user_id, status='PENDING_PAY').count(),
            'shipped': SpOrder.query.filter_by(user_id=user_id, status='PAID').count(),
            'received': SpOrder.query.filter_by(user_id=user_id, status='SHIPPED').count(),
            'refund': SpOrder.query.filter_by(user_id=user_id, status='CANCELLED').count()
        }
        
        return success_response(counts)


@sp_order_ns.route('/cancel/<int:order_id>')
class SpOrderCancel(Resource):
    @sp_order_ns.doc('取消订单')
    def post(self, order_id):
        """取消订单"""
        user_id = get_current_user_id()
        data = request.get_json()
        reason = data.get('reason')
        
        order, message = SpOrderService.cancel_order(order_id, user_id, reason)
        
        if not order:
            return error_response(message)
        
        return success_response(order, message)


@sp_order_ns.route('/confirm/<int:order_id>')
class SpOrderConfirm(Resource):
    @sp_order_ns.doc('确认收货')
    def post(self, order_id):
        """确认收货"""
        user_id = get_current_user_id()
        
        order, message = SpOrderService.confirm_receipt(order_id, user_id)
        
        if not order:
            return error_response(message)
        
        return success_response(order, message)


# ========== 地址相关API ==========

@sp_address_ns.route('/list')
class SpAddressList(Resource):
    @sp_address_ns.doc('获取地址列表')
    def get(self):
        """获取用户地址列表"""
        user_id = get_current_user_id()
        addresses = SpAddressService.get_address_list(user_id)
        return success_response(addresses)


@sp_address_ns.route('/default')
class SpAddressDefault(Resource):
    @sp_address_ns.doc('获取默认地址')
    def get(self):
        """获取用户默认地址"""
        user_id = get_current_user_id()
        address = SpAddressService.get_default_address(user_id)
        return success_response(address)


@sp_address_ns.route('/detail/<int:address_id>')
class SpAddressDetail(Resource):
    @sp_address_ns.doc('获取地址详情')
    def get(self, address_id):
        """根据ID获取地址详情"""
        user_id = get_current_user_id()
        address = SpAddressService.get_address_by_id(address_id, user_id)
        
        if not address:
            return error_response('地址不存在', 404)
        
        return success_response(address)


@sp_address_ns.route('/add')
class SpAddressAdd(Resource):
    @sp_address_ns.doc('添加地址')
    def post(self):
        """添加地址"""
        user_id = get_current_user_id()
        data = request.get_json()
        
        if not data.get('name'):
            return error_response('请输入收货人姓名')
        
        if not data.get('phone'):
            return error_response('请输入手机号码')
        
        if not data.get('province') or not data.get('city') or not data.get('district'):
            return error_response('请选择所在地区')
        
        if not data.get('detail'):
            return error_response('请输入详细地址')
        
        address = SpAddressService.add_address(user_id, data)
        return success_response(address, '添加成功')


@sp_address_ns.route('/update/<int:address_id>')
class SpAddressUpdate(Resource):
    @sp_address_ns.doc('更新地址')
    def put(self, address_id):
        """更新地址"""
        user_id = get_current_user_id()
        data = request.get_json()
        
        address = SpAddressService.update_address(address_id, user_id, data)
        
        if not address:
            return error_response('地址不存在')
        
        return success_response(address, '更新成功')


@sp_address_ns.route('/delete/<int:address_id>')
class SpAddressDelete(Resource):
    @sp_address_ns.doc('删除地址')
    def delete(self, address_id):
        """删除地址"""
        user_id = get_current_user_id()
        
        result = SpAddressService.delete_address(address_id, user_id)
        
        if not result:
            return error_response('地址不存在')
        
        return success_response(None, '删除成功')


@sp_address_ns.route('/default/<int:address_id>')
class SpAddressSetDefault(Resource):
    @sp_address_ns.doc('设置默认地址')
    def put(self, address_id):
        """设置默认地址"""
        user_id = get_current_user_id()
        
        address = SpAddressService.set_default_address(address_id, user_id)
        
        if not address:
            return error_response('地址不存在')
        
        return success_response(address, '设置成功')
