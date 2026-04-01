# -*- encoding: utf-8 -*-
"""
商品商城模块 - 后台管理路由
"""

from flask import Blueprint, render_template, request, jsonify
from apps.product.services import ProductService, CartService, OrderService
from apps.product.models import Order
from apps.xp_product.models import Category as XPCategory, Product as XPProduct
from apps import db

blueprint = Blueprint('product', __name__, url_prefix='/admin/product')


@blueprint.route('/category')
def category_list():
    """商品分类列表页"""
    categories = XPCategory.query.order_by(XPCategory.sort).all()
    return render_template('product/category_list.html', categories=categories)


@blueprint.route('/category/add', methods=['POST'])
def category_add():
    """添加商品分类"""
    data = request.get_json()
    
    category = XPCategory(
        name=data.get('categoryName'),
        parent_id=data.get('parentId', 0),
        level=data.get('level', 1),
        icon=data.get('icon'),
        sort=data.get('sort', 0),
        status=data.get('status', 1)
    )
    
    try:
        db.session.add(category)
        db.session.commit()
        return jsonify({'code': 200, 'message': '添加成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/category/<int:category_id>')
def category_detail(category_id):
    """获取单个分类详情"""
    category = XPCategory.query.get(category_id)
    
    if not category:
        return jsonify({'code': 404, 'message': '分类不存在', 'data': None})
    
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'id': category.id,
            'categoryName': category.name,
            'categoryCode': '',
            'parentId': category.parent_id,
            'icon': category.icon,
            'sort': category.sort,
            'status': category.status
        }
    })


@blueprint.route('/category/delete/<int:category_id>', methods=['DELETE'])
def category_delete(category_id):
    """删除商品分类"""
    category = XPCategory.query.get(category_id)
    
    if not category:
        return jsonify({'code': 404, 'message': '分类不存在', 'data': None})
    
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'code': 200, 'message': '删除成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/product')
@blueprint.route('/list')
def product_list():
    """商品列表页"""
    page = request.args.get('page', 1, type=int)
    page_size = 20
    category_id = request.args.get('categoryId', type=int)
    status = request.args.get('status', type=int)
    keyword = request.args.get('keyword')
    
    query = XPProduct.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if status is not None:
        query = query.filter_by(status=status)
    
    if keyword:
        query = query.filter(XPProduct.name.like(f'%{keyword}%'))
    
    pagination = query.order_by(XPProduct.id.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )
    
    categories = XPCategory.query.filter_by(status=1).order_by(XPCategory.sort).all()
    
    return render_template('product/product_list.html', 
                          products=pagination.items,
                          categories=categories,
                          pagination=pagination)


@blueprint.route('/product/add', methods=['POST'])
def product_add():
    """添加商品"""
    data = request.get_json()
    
    product = Product(
        category_id=data.get('categoryId'),
        product_name=data.get('productName'),
        product_code=data.get('productCode'),
        main_image=data.get('mainImage'),
        price=data.get('price'),
        original_price=data.get('originalPrice'),
        member_price=data.get('memberPrice'),
        stock=data.get('stock', 0),
        sales=data.get('sales', 0),
        brief=data.get('brief'),
        status=data.get('status', 1),
        is_hot=data.get('isHot', 0),
        is_new=data.get('isNew', 0),
        is_recommend=data.get('isRecommend', 0),
        sort=data.get('sort', 0)
    )
    
    try:
        db.session.add(product)
        db.session.commit()
        return jsonify({'code': 200, 'message': '添加成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/product/toggle-status/<int:product_id>', methods=['PUT'])
def product_toggle_status(product_id):
    """切换商品状态"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'code': 404, 'message': '商品不存在', 'data': None})
    
    try:
        product.status = 0 if product.status == 1 else 1
        db.session.commit()
        return jsonify({'code': 200, 'message': '状态更新成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/product/delete/<int:product_id>', methods=['DELETE'])
def product_delete(product_id):
    """删除商品"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'code': 404, 'message': '商品不存在', 'data': None})
    
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'code': 200, 'message': '删除成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/order')
def order_list():
    """订单列表页"""
    page = request.args.get('page', 1, type=int)
    page_size = 20
    status = request.args.get('status')
    order_no = request.args.get('orderNo')
    phone = request.args.get('phone')
    
    query = Order.query
    
    if status:
        query = query.filter_by(status=status)
    
    if order_no:
        query = query.filter(Order.order_no.like(f'%{order_no}%'))
    
    if phone:
        query = query.filter(Order.receiver_phone.like(f'%{phone}%'))
    
    pagination = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )
    
    return render_template('product/order_list.html', 
                          orders=pagination.items,
                          pagination=pagination)


@blueprint.route('/order/detail/<int:order_id>')
def order_detail(order_id):
    """订单详情"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'code': 404, 'message': '订单不存在', 'data': None})
    
    return jsonify({'code': 200, 'message': 'success', 'data': order.to_dict(include_items=True)})


@blueprint.route('/order/ship/<int:order_id>', methods=['PUT'])
def order_ship(order_id):
    """订单发货"""
    order, message = OrderService.update_order_status(order_id, 'SHIPPED')
    
    if order:
        return jsonify({'code': 200, 'message': '发货成功', 'data': order})
    else:
        return jsonify({'code': 500, 'message': message, 'data': None})


@blueprint.route('/order/cancel/<int:order_id>', methods=['POST'])
def order_cancel(order_id):
    """取消订单"""
    data = request.get_json()
    reason = data.get('reason')
    
    order, message = OrderService.cancel_order(order_id, order.user_id, reason)
    
    if order:
        return jsonify({'code': 200, 'message': '订单已取消', 'data': order})
    else:
        return jsonify({'code': 500, 'message': message, 'data': None})


@blueprint.route('/commission')
def commission_list():
    """佣金管理页面"""
    # 强制刷新模板缓存
    return render_template('product/commission.html', cache_timeout=0)
