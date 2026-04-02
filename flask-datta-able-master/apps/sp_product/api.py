# -*- encoding: utf-8 -*-
"""
<<<<<<< HEAD
商品商城模块 - REST API
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from apps.product.services import ProductService, CartService, OrderService
from apps import db

api = Namespace('product', description='商品相关API')

category_ns = Namespace('product/category', description='商品分类API')
cart_ns = Namespace('product/cart', description='购物车API')
order_ns = Namespace('product/order', description='订单API')


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

@category_ns.route('/list')
class CategoryList(Resource):
    @category_ns.doc('获取商品分类列表')
    def get(self):
        """获取所有商品分类"""
        categories = ProductService.get_categories()
        return success_response(categories)


@category_ns.route('/<int:category_id>')
class CategoryDetail(Resource):
    @category_ns.doc('获取分类详情')
    def get(self, category_id):
        """根据ID获取分类详情"""
        category = ProductService.get_category_by_id(category_id)
        
        if not category:
            return error_response('分类不存在', 404)
        
        return success_response(category)


# ========== 商品相关API ==========

@api.route('/list')
class ProductList(Resource):
    @api.doc('获取商品列表')
    def get(self):
        """获取商品列表"""
        category_id = request.args.get('categoryId', type=int)
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        keyword = request.args.get('keyword')
        
        result = ProductService.get_products(category_id, page, page_size, keyword)
        return success_response(result)


@api.route('/<int:product_id>')
class ProductDetail(Resource):
    @api.doc('获取商品详情')
    def get(self, product_id):
        """根据ID获取商品详情"""
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            return error_response('商品不存在', 404)
        
        return success_response(product)


@api.route('/hot')
class HotProducts(Resource):
    @api.doc('获取热销商品')
    def get(self):
        """获取热销商品"""
        limit = request.args.get('limit', 10, type=int)
        products = ProductService.get_hot_products(limit)
        return success_response(products)


@api.route('/new')
class NewProducts(Resource):
    @api.doc('获取新品商品')
    def get(self):
        """获取新品商品"""
        limit = request.args.get('limit', 10, type=int)
        products = ProductService.get_new_products(limit)
        return success_response(products)


@api.route('/recommend')
class RecommendProducts(Resource):
    @api.doc('获取推荐商品')
    def get(self):
        """获取推荐商品"""
        limit = request.args.get('limit', 10, type=int)
        products = ProductService.get_recommend_products(limit)
        return success_response(products)


@api.route('/search')
class SearchProducts(Resource):
    @api.doc('搜索商品')
    def get(self):
        """搜索商品"""
        keyword = request.args.get('keyword')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        if not keyword:
            return error_response('请输入搜索关键词')
        
        result = ProductService.search_products(keyword, page, page_size)
        return success_response(result)


# ========== 购物车相关API ==========

@cart_ns.route('/list')
class CartList(Resource):
    @cart_ns.doc('获取购物车列表')
    def get(self):
        """获取用户购物车列表"""
        user_id = get_current_user_id()
        cart_items = CartService.get_cart_list(user_id)
        return success_response(cart_items)


@cart_ns.route('/add')
class CartAdd(Resource):
    @cart_ns.doc('添加商品到购物车')
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
        
        cart_item = CartService.add_to_cart(user_id, product_id, sku_id, quantity)
        return success_response(cart_item, '添加成功')


@cart_ns.route('/update/<int:cart_id>')
class CartUpdate(Resource):
    @cart_ns.doc('更新购物车商品数量')
    def put(self, cart_id):
        """更新购物车商品数量"""
        user_id = get_current_user_id()
        data = request.get_json()
        quantity = data.get('quantity', 1)
        
        cart_item = CartService.update_cart_quantity(cart_id, user_id, quantity)
        
        if not cart_item:
            return error_response('购物车商品不存在')
        
        return success_response(cart_item, '更新成功')


@cart_ns.route('/select/<int:cart_id>')
class CartSelect(Resource):
    @cart_ns.doc('更新购物车商品选中状态')
    def put(self, cart_id):
        """更新购物车商品选中状态"""
        user_id = get_current_user_id()
        data = request.get_json()
        selected = data.get('selected', True)
        
        cart_item = CartService.update_cart_selected(cart_id, user_id, selected)
        
        if not cart_item:
            return error_response('购物车商品不存在')
        
        return success_response(cart_item, '更新成功')


@cart_ns.route('/delete/<int:cart_id>')
class CartDelete(Resource):
    @cart_ns.doc('删除购物车商品')
    def delete(self, cart_id):
        """删除购物车商品"""
        user_id = get_current_user_id()
        
        result = CartService.delete_cart_item(cart_id, user_id)
        
        if not result:
            return error_response('购物车商品不存在')
        
        return success_response(None, '删除成功')


@cart_ns.route('/clear')
class CartClear(Resource):
    @cart_ns.doc('清空购物车')
    def delete(self):
        """清空购物车"""
        user_id = get_current_user_id()
        CartService.clear_cart(user_id)
        return success_response(None, '清空成功')


@cart_ns.route('/total')
class CartTotal(Resource):
    @cart_ns.doc('获取购物车总金额')
    def get(self):
        """获取购物车选中商品总金额"""
        user_id = get_current_user_id()
        total = CartService.get_cart_total(user_id)
        return success_response({'total': total})


# ========== 订单相关API ==========

@order_ns.route('/submit')
class OrderSubmit(Resource):
    @order_ns.doc('提交订单')
    def post(self):
        """提交订单"""
        user_id = get_current_user_id()
        data = request.get_json()
        
        cart_items = data.get('cartItems', [])
        address_info = data.get('addressInfo')
        remark = data.get('remark')
        
        if not cart_items:
            return error_response('请选择商品')
        
        if not address_info:
            return error_response('请填写收货地址')
        
        order, message = OrderService.submit_order(user_id, cart_items, address_info, remark)
        
        if not order:
            return error_response(message)
        
        return success_response(order, message)


@order_ns.route('/list')
class OrderList(Resource):
    @order_ns.doc('获取订单列表')
    def get(self):
        """获取用户订单列表"""
        user_id = get_current_user_id()
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        result = OrderService.get_order_list(user_id, status, page, page_size)
        return success_response(result)


@order_ns.route('/detail/<int:order_id>')
class OrderDetail(Resource):
    @order_ns.doc('获取订单详情')
    def get(self, order_id):
        """根据ID获取订单详情"""
        user_id = get_current_user_id()
        order = OrderService.get_order_by_id(order_id, user_id)
        
        if not order:
            return error_response('订单不存在', 404)
        
        return success_response(order)


@order_ns.route('/cancel/<int:order_id>')
class OrderCancel(Resource):
    @order_ns.doc('取消订单')
    def post(self, order_id):
        """取消订单"""
        user_id = get_current_user_id()
        data = request.get_json()
        reason = data.get('reason')
        
        order, message = OrderService.cancel_order(order_id, user_id, reason)
        
        if not order:
            return error_response(message)
        
        return success_response(order, message)


@order_ns.route('/detail/<order_no>')
class OrderDetailByNo(Resource):
    @order_ns.doc('根据订单编号获取订单详情')
    def get(self, order_no):
        """根据订单编号获取订单详情"""
        order = OrderService.get_order_by_no(order_no)
        
        if not order:
            return error_response('订单不存在', 404)
        
        return success_response(order)
