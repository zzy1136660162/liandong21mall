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
=======
商品选品模块 - API
按接口文档实现
"""

from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from apps import db
from apps.product.models import Product, Category
from datetime import datetime

api = Namespace('product', description='商品选品模块')

ProductModel = api.model('Product', {
    'id': fields.Integer,
    'name': fields.String,
    'category_id': fields.Integer,
    'status': fields.Integer,
})


@api.route('')
class ProductListAPI(Resource):
    """获取商品列表 - GET /products"""
    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        category = request.args.get('category', '')
        keyword = request.args.get('keyword', '')
        sort_by = request.args.get('sortBy', '')
        sort_order = request.args.get('sortOrder', 'desc')
        min_commission = request.args.get('minCommission', type=float)
        max_price = request.args.get('maxPrice', type=float)

        query = Product.query.filter_by(status=1)

        if category:
            query = query.filter(Product.category_id == category)
        if keyword:
            query = query.filter(Product.name.like(f'%{keyword}%'))
        if min_commission:
            query = query.filter(Product.commission_rate >= min_commission)
        if max_price:
            query = query.filter(Product.price <= max_price)

        if sort_by:
            sort_field = Product.commission_rate if sort_by == 'commission' else \
                        Product.sales if sort_by == 'sales' else Product.price
            if sort_order == 'asc':
                query = query.order_by(sort_field.asc())
            else:
                query = query.order_by(sort_field.desc())
        else:
            query = query.order_by(Product.created_at.desc())

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)

        return {
            'code': 200,
            'message': 'success',
            'data': {
                'total': pagination.total,
                'page': page,
                'pageSize': page_size,
                'list': [p.to_api_dict() for p in pagination.items]
            }
        }


@api.route('/<int:id>')
class ProductDetailAPI(Resource):
    """获取商品详情 - GET /products/{id}"""
    def get(self, id):
        product = Product.query.get_or_404(id)
        
        return {
            'code': 200,
            'message': 'success',
            'data': product.to_api_detail_dict()
        }


@api.route('/<int:id>/commission')
class ProductCommissionAPI(Resource):
    """获取商品佣金信息 - GET /products/{id}/commission"""
    def get(self, id):
        product = Product.query.get_or_404(id)
        
        commission_amount = float(product.price) * float(product.commission_rate) / 100
        
        settlement_map = {1: '月结', 2: '周结', 3: '实时'}
        
        return {
            'code': 200,
            'message': 'success',
            'data': {
                'productId': product.id,
                'baseRate': float(product.commission_rate),
                'levelRates': {
                    'normal': {'rate': float(product.normal_rate), 'description': '普通达人'},
                    'premium': {'rate': float(product.premium_rate), 'description': '优质达人'},
                    'top': {'rate': float(product.top_rate), 'description': '头部达人'}
                },
                'currentRate': float(product.commission_rate),
                'estimatedCommission': round(commission_amount, 2),
                'settlementType': settlement_map.get(product.settlement_type, '月结'),
                'settlementDesc': '订单确认收货后结算，每月15日打款'
            }
        }


@api.route('/category/list')
class CategoryListAPI(Resource):
    """获取分类列表 - GET /categories"""
    def get(self):
        categories = Category.query.filter_by(status=1).order_by(Category.sort.asc()).all()
        
        result = []
        for cat in categories:
            if cat.parent_id == 0:
                sub_cats = [sub for sub in categories if sub.parent_id == cat.id]
                result.append({
                    'id': str(cat.id),
                    'name': cat.name,
                    'icon': cat.icon or '',
                    'subCategories': [{'id': str(sub.id), 'name': sub.name} for sub in sub_cats]
                })
        
        return {
            'code': 200,
            'message': 'success',
            'data': result
        }


@api.route('/categories')
class CategoriesAPI(Resource):
    """获取分类列表 - GET /api/product/categories (小程序端)"""
    def get(self):
        categories = Category.query.filter_by(status=1).order_by(Category.sort.asc()).all()
        
        result = []
        for cat in categories:
            if cat.parent_id == 0:
                sub_cats = [sub for sub in categories if sub.parent_id == cat.id]
                result.append({
                    'id': str(cat.id),
                    'name': cat.name,
                    'icon': cat.icon or '',
                    'subCategories': [{'id': str(sub.id), 'name': sub.name} for sub in sub_cats]
                })
        
        return {
            'code': 200,
            'message': 'success',
            'data': result
        }


@api.route('/list/admin')
class ProductListAdminAPI(Resource):
    """管理后台商品列表"""
    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        category_id = request.args.get('category_id', type=int)
        status = request.args.get('status', type=int)
        keyword = request.args.get('keyword', '')

        query = Product.query

        if category_id:
            query = query.filter(Product.category_id == category_id)
        if status is not None:
            query = query.filter(Product.status == status)
        if keyword:
            query = query.filter(Product.name.like(f'%{keyword}%'))

        pagination = query.order_by(Product.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )

        return {
            'code': 200,
            'message': 'success',
            'data': {
                'list': [p.to_dict() for p in pagination.items],
                'total': pagination.total,
                'page': page,
                'page_size': page_size
            }
        }

    def post(self):
        data = request.get_json()
        
        if not data.get('name') or not data.get('price'):
            return {'code': 400, 'message': '商品名和价格不能为空'}, 400
        
        import time
        product = Product(
            product_no=f'P{time.strftime("%Y%m%d%H%M%S")}{str(time.time())[-6:]}',
            name=data['name'],
            subtitle=data.get('subtitle', ''),
            category_id=data.get('category_id', 0),
            main_image=data.get('main_image', ''),
            images=data.get('images', []),
            price=data['price'],
            original_price=data.get('original_price'),
            supply_price=data.get('supply_price', 0),
            stock=data.get('stock', 0),
            status=data.get('status', 1),
            commission_rate=data.get('commission_rate', 10),
            normal_rate=data.get('normal_rate', 10),
            premium_rate=data.get('premium_rate', 15),
            top_rate=data.get('top_rate', 20),
            settlement_type=data.get('settlement_type', 1)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return {'code': 200, 'message': '添加成功', 'data': product.to_dict()}


@api.route('/<int:id>/admin')
class ProductDetailAdminAPI(Resource):
    def get(self, id):
        product = Product.query.get_or_404(id)
        return {'code': 200, 'message': 'success', 'data': product.to_dict()}

    def put(self, id):
        product = Product.query.get_or_404(id)
        data = request.get_json()
        
        product.name = data.get('name', product.name)
        product.subtitle = data.get('subtitle', product.subtitle)
        product.category_id = data.get('category_id', product.category_id)
        product.main_image = data.get('main_image', product.main_image)
        product.images = data.get('images', product.images)
        product.price = data.get('price', product.price)
        product.original_price = data.get('original_price', product.original_price)
        product.supply_price = data.get('supply_price', product.supply_price)
        product.stock = data.get('stock', product.stock)
        product.status = data.get('status', product.status)
        product.commission_rate = data.get('commission_rate', product.commission_rate)
        product.normal_rate = data.get('normal_rate', product.normal_rate)
        product.premium_rate = data.get('premium_rate', product.premium_rate)
        product.top_rate = data.get('top_rate', product.top_rate)
        product.settlement_type = data.get('settlement_type', product.settlement_type)
        
        db.session.commit()
        return {'code': 200, 'message': '更新成功', 'data': product.to_dict()}

    def delete(self, id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return {'code': 200, 'message': '删除成功'}


@api.route('/batch-delete')
class ProductBatchDelete(Resource):
    def post(self):
        data = request.get_json()
        ids = data.get('ids', [])
        
        if not ids:
            return {'code': 400, 'message': '请选择要删除的商品'}, 400
        
        Product.query.filter(Product.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        
        return {'code': 200, 'message': '批量删除成功'}


@api.route('/batch-update-status')
class ProductBatchUpdateStatus(Resource):
    def post(self):
        data = request.get_json()
        ids = data.get('ids', [])
        status = data.get('status', 1)
        
        if not ids:
            return {'code': 400, 'message': '请选择要操作的商品'}, 400
        
        Product.query.filter(Product.id.in_(ids)).update({Product.status: status}, synchronize_session=False)
        db.session.commit()
        
        return {'code': 200, 'message': '批量更新成功'}


@api.route('/category/admin/list')
class CategoryListAdminAPI(Resource):
    def get(self):
        parent_id = request.args.get('parent_id', 0, type=int)
        
        query = Category.query
        if parent_id is not None:
            query = query.filter_by(parent_id=parent_id)
        
        categories = query.order_by(Category.sort.asc(), Category.id.asc()).all()
        
        return {
            'code': 200,
            'message': 'success',
            'data': [c.to_dict() for c in categories]
        }

    def post(self):
        data = request.get_json()
        
        if not data.get('name'):
            return {'code': 400, 'message': '分类名称不能为空'}, 400
        
        category = Category(
            name=data['name'],
            parent_id=data.get('parent_id', 0),
            level=data.get('level', 1),
            icon=data.get('icon', ''),
            sort=data.get('sort', 0),
            status=data.get('status', 1)
        )
        
        db.session.add(category)
        db.session.commit()
        
        return {'code': 200, 'message': '添加成功', 'data': category.to_dict()}


@api.route('/category/<int:id>/admin')
class CategoryDetailAdminAPI(Resource):
    def get(self, id):
        category = Category.query.get_or_404(id)
        return {'code': 200, 'message': 'success', 'data': category.to_dict()}

    def put(self, id):
        category = Category.query.get_or_404(id)
        data = request.get_json()
        
        category.name = data.get('name', category.name)
        category.parent_id = data.get('parent_id', category.parent_id)
        category.level = data.get('level', category.level)
        category.icon = data.get('icon', category.icon)
        category.sort = data.get('sort', category.sort)
        category.status = data.get('status', category.status)
        
        db.session.commit()
        return {'code': 200, 'message': '更新成功', 'data': category.to_dict()}

    def delete(self, id):
        category = Category.query.get_or_404(id)
        
        child_count = Category.query.filter_by(parent_id=id).count()
        if child_count > 0:
            return {'code': 400, 'message': '请先删除子分类'}, 400
        
        db.session.delete(category)
        db.session.commit()
        return {'code': 200, 'message': '删除成功'}


@api.route('/commission/list')
class CommissionListAPI(Resource):
    """佣金管理列表"""
    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 20, type=int)
        keyword = request.args.get('keyword', '')
        
        query = Product.query
        
        if keyword:
            query = query.filter(Product.name.like(f'%{keyword}%'))
        
        pagination = query.order_by(Product.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        return {
            'code': 200,
            'message': 'success',
            'data': {
                'list': [p.to_dict() for p in pagination.items],
                'total': pagination.total,
                'page': page,
                'page_size': page_size
            }
        }


@api.route('/commission/update/<int:id>')
class CommissionUpdateAPI(Resource):
    def put(self, id):
        product = Product.query.get_or_404(id)
        data = request.get_json()
        
        product.commission_rate = data.get('commission_rate', product.commission_rate)
        product.normal_rate = data.get('normal_rate', product.normal_rate)
        product.premium_rate = data.get('premium_rate', product.premium_rate)
        product.top_rate = data.get('top_rate', product.top_rate)
        product.settlement_type = data.get('settlement_type', product.settlement_type)
        
        db.session.commit()
        return {'code': 200, 'message': '更新成功', 'data': product.to_dict()}


@api.route('/commission/batch-update')
class CommissionBatchUpdateAPI(Resource):
    def post(self):
        data = request.get_json()
        ids = data.get('ids', [])
        
        if not ids:
            return {'code': 400, 'message': '请选择要更新的商品'}, 400
        
        update_data = {}
        if 'commission_rate' in data:
            update_data[Product.commission_rate] = data['commission_rate']
        if 'normal_rate' in data:
            update_data[Product.normal_rate] = data['normal_rate']
        if 'premium_rate' in data:
            update_data[Product.premium_rate] = data['premium_rate']
        if 'top_rate' in data:
            update_data[Product.top_rate] = data['top_rate']
        if 'settlement_type' in data:
            update_data[Product.settlement_type] = data['settlement_type']
        
        if update_data:
            Product.query.filter(Product.id.in_(ids)).update(update_data, synchronize_session=False)
            db.session.commit()
        
        return {'code': 200, 'message': '批量更新成功'}


@api.route('/activities')
class ActivityListAPI(Resource):
    """获取活动列表 - GET /activities"""
    def get(self):
        activities = [
            {
                'id': 'ACT001',
                'type': 'hot',
                'name': '超级爆品',
                'title': '超级爆品',
                'subtitle': '精选全网热销爆款，佣金高转化好',
                'banner': '/static/assets/images/slider/img-slide-1.jpg',
                'stats': {
                    'productCount': Product.query.filter_by(status=1, is_hot=1).count(),
                    'avgCommission': 25,
                    'totalSales': '1.2亿'
                }
            },
            {
                'id': 'ACT002',
                'type': 'follow',
                'name': '同行跟选',
                'title': '同行跟选',
                'subtitle': '看看同行都在卖什么，紧跟市场趋势',
                'banner': '/static/assets/images/slider/img-slide-2.jpg',
                'stats': {
                    'followerCount': 12580,
                    'successRate': 85,
                    'avgIncome': '¥3,200'
                }
            },
            {
                'id': 'ACT003',
                'type': 'new',
                'name': '新品推荐',
                'title': '新品推荐',
                'subtitle': '最新上线商品，抢占先机',
                'banner': '/static/assets/images/slider/img-slide-3.jpg',
                'stats': {
                    'productCount': Product.query.filter_by(status=1, is_new=1).count(),
                    'avgCommission': 20,
                    'totalSales': '500万'
                }
            },
            {
                'id': 'ACT004',
                'type': 'brand',
                'name': '品牌专区',
                'title': '品牌专区',
                'subtitle': '知名品牌，品质保障',
                'banner': '/static/assets/images/slider/img-slide-4.jpg',
                'stats': {
                    'productCount': Product.query.filter_by(status=1, is_brand=1).count(),
                    'avgCommission': 18,
                    'totalSales': '8000万'
                }
            }
        ]
        
        return {
            'code': 200,
            'message': 'success',
            'data': activities
        }


@api.route('/activities/<string:activity_type>/products')
class ActivityProductListAPI(Resource):
    """获取活动商品列表 - GET /activities/{type}/products"""
    def get(self, activity_type):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        query = Product.query.filter_by(status=1)
        
        if activity_type == 'hot':
            query = query.filter_by(is_hot=1)
            title = '超级爆品'
        elif activity_type == 'follow':
            query = query.order_by(Product.sales.desc())
            title = '同行跟选'
        elif activity_type == 'new':
            query = query.filter_by(is_new=1)
            title = '新品推荐'
        elif activity_type == 'brand':
            query = query.filter_by(is_brand=1)
            title = '品牌专区'
        else:
            title = '活动商品'
        
        pagination = query.order_by(Product.sales.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        products = []
        for idx, p in enumerate(pagination.items, start=1):
            commission = float(p.price) * float(p.commission_rate) / 100 if p.commission_rate else 0
            products.append({
                'id': str(p.id),
                'rank': idx,
                'name': p.name,
                'image': p.main_image,
                'price': float(p.price) if p.price else 0,
                'commission': round(commission, 2),
                'commissionRate': float(p.commission_rate) if p.commission_rate else 0,
                'sales': f'月销{p.sales}件' if p.sales else '月销0件',
                'dailySales': f'{p.sales // 30}万' if p.sales else '0',
                'tag': '爆款' if p.is_hot else ('新品' if p.is_new else ('品牌' if p.is_brand else '')),
                'rankTag': f'入选{title}第{idx}名'
            })
        
        return {
            'code': 200,
            'message': 'success',
            'data': {
                'activityType': activity_type,
                'products': products
            }
        }


@api.route('/search')
class SearchAPI(Resource):
    """搜索商品 - GET /search"""
    def get(self):
        keyword = request.args.get('keyword', '')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        sort = request.args.get('sort', 'default')
        
        if not keyword:
            return {'code': 400, 'message': '请输入搜索关键词'}, 400
        
        query = Product.query.filter_by(status=1).filter(
            Product.name.like(f'%{keyword}%')
        )
        
        if sort == 'sales':
            query = query.order_by(Product.sales.desc())
        elif sort == 'commission':
            query = query.order_by(Product.commission_rate.desc())
        elif sort == 'new':
            query = query.order_by(Product.create_time.desc())
        elif sort == 'price':
            query = query.order_by(Product.price.asc())
        else:
            query = query.order_by(Product.sales.desc())
        
        pagination = query.paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        return {
            'code': 200,
            'message': 'success',
            'data': {
                'keyword': keyword,
                'total': pagination.total,
                'page': page,
                'pageSize': page_size,
                'list': [p.to_api_dict() for p in pagination.items]
            }
        }


@api.route('/search/hot')
class HotSearchAPI(Resource):
    """获取热门搜索词 - GET /search/hot"""
    def get(self):
        keywords = ['洗衣液', '抽纸', '零食', '饮料', '面膜', '卫生巾', '洗发水', '牙膏', '牙刷', '杯子']
        
        return {
            'code': 200,
            'message': 'success',
            'data': {
                'keywords': keywords
            }
        }


@api.route('/search/suggestions')
class SearchSuggestionsAPI(Resource):
    """获取搜索联想 - GET /search/suggestions"""
    def get(self):
        keyword = request.args.get('keyword', '')
        
        if not keyword or len(keyword) < 1:
            return {'code': 200, 'data': []}
        
        products = Product.query.filter(
            Product.status == 1,
            Product.name.like(f'%{keyword}%')
        ).limit(10).all()
        
        suggestions = []
        seen = set()
        for p in products:
            if p.name not in seen:
                suggestions.append(p.name)
                seen.add(p.name)
        
        common_suffixes = ['', '1', '2', '3', '套装', '正品', '新款', '爆款']
        for suffix in common_suffixes:
            if len(suggestions) >= 5:
                break
            suggestion = keyword + suffix
            if suggestion not in seen:
                suggestions.append(suggestion)
                seen.add(suggestion)
        
        return {
            'code': 200,
            'message': 'success',
            'data': suggestions[:5]
        }


@api.route('/search/history')
class SearchHistoryAPI(Resource):
    """获取搜索历史 - GET /search/history"""
    def get(self):
        return {
            'code': 200,
            'message': 'success',
            'data': {
                'history': []
            }
        }
    
    def delete(self):
        return {
            'code': 200,
            'message': '清空成功',
            'data': None
        }


@api.route('/rankings')
class RankingListAPI(Resource):
    """获取榜单列表 - GET /rankings"""
    def get(self):
        ranking_type = request.args.get('type', 'hot')
        category = request.args.get('category', '')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        
        query = Product.query.filter_by(status=1)
        
        if category:
            try:
                category_id = int(category)
                query = query.filter(Product.category_id == category_id)
            except:
                pass
        
        if ranking_type == 'hot':
            query = query.order_by(Product.sales.desc())
            title = '热销榜单'
        elif ranking_type == 'commission':
            query = query.order_by(Product.commission_rate.desc())
            title = '高佣榜单'
        elif ranking_type == 'new':
            query = query.order_by(Product.created_at.desc())
            title = '新品榜单'
        elif ranking_type == 'rising':
            query = query.order_by(Product.sales.desc())
            title = '飙升榜单'
        else:
            title = '榜单'
        
        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        
        products = []
        for idx, p in enumerate(pagination.items, start=1):
            commission = float(p.price) * float(p.commission_rate) / 100 if p.commission_rate else 0
            trend = 'up' if p.sales > 1000 else ('down' if p.sales < 100 else 'stable')
            products.append({
                'id': str(p.id),
                'rank': idx,
                'name': p.name,
                'image': p.main_image,
                'price': float(p.price) if p.price else 0,
                'commission': round(commission, 2),
                'commissionRate': float(p.commission_rate) if p.commission_rate else 0,
                'sales': f'月销{p.sales}件' if p.sales else '月销0件',
                'trend': trend
            })
        
        return {
            'code': 200,
            'message': 'success',
            'data': {
                'type': ranking_type,
                'title': title,
                'updateTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'list': products
            }
        }


@api.route('/logistics/query')
class LogisticsQueryAPI(Resource):
    """查询物流信息 - GET /logistics/query"""
    def get(self):
        company = request.args.get('company', '')
        tracking_no = request.args.get('trackingNo', '')
        
        if not company or not tracking_no:
            return {'code': 400, 'message': '物流公司和单号不能为空'}, 400
        
        company_map = {
            'sf': '顺丰速运',
            'yto': '圆通速递',
            'zto': '中通快递',
            'sto': '申通快递',
            'ems': 'EMS',
            'jd': '京东物流'
        }
        
        company_name = company_map.get(company, company)
        
        traces = [
            {
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'desc': f'【目的地】快件已发出',
                'location': '目的地城市'
            },
            {
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'desc': f'【中转中心】快件到达转运中心',
                'location': '中转城市'
            },
            {
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'desc': f'【寄件地】快件已发货',
                'location': '寄件城市'
            }
        ]
        
        return {
            'code': 200,
            'message': 'success',
            'data': {
                'company': company_name,
                'trackingNo': tracking_no,
                'status': 'shipped',
                'statusText': '运输中',
                'traces': traces
            }
        }
>>>>>>> origin/master
