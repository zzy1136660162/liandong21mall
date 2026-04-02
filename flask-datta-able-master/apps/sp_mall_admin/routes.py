# -*- encoding: utf-8 -*-
"""
商品商城模块 - 后台管理路由
"""

import os
import uuid
from flask import Blueprint, render_template, request, jsonify, current_app, send_from_directory
from apps import db
from apps.sp_mall.sp_models import (
    SpProductCategory,
    SpProduct,
    SpProductSku,
    SpOrder,
    SpOrderItem
)
from datetime import datetime
import time
import logging

blueprint = Blueprint('sp_mall_admin', __name__, url_prefix='/admin/sp')

logger = logging.getLogger(__name__)


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})


@blueprint.route('/upload/image', methods=['POST'])
def upload_image():
    """上传商品图片"""
    try:
        if 'file' not in request.files:
            return jsonify({'code': 400, 'message': '没有文件', 'data': None})
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'code': 400, 'message': '没有选择文件', 'data': None})
        
        if not allowed_file(file.filename):
            return jsonify({'code': 400, 'message': '不支持的文件类型，请上传 JPG、PNG、GIF、WebP 格式的图片', 'data': None})
        
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'products')
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        file_size = os.path.getsize(filepath)
        logger.info(f'图片上传成功: {filename}, 大小: {file_size} bytes')
        
        image_url = f'/static/uploads/products/{filename}'
        
        return jsonify({
            'code': 200,
            'message': '上传成功',
            'data': {
                'url': image_url,
                'filename': filename,
                'size': file_size
            }
        })
    
    except Exception as e:
        logger.error(f'图片上传失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'上传失败: {str(e)}', 'data': None})


@blueprint.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """访问上传的文件"""
    return send_from_directory(os.path.join(current_app.root_path, 'static', 'uploads'), filename)


@blueprint.route('/category')
def category_list():
    """商品分类列表"""
    categories = SpProductCategory.query.order_by(SpProductCategory.sort).all()
    
    # 构建树形结构
    category_tree = {}
    for cat in categories:
        if cat.parent_id == 0:
            category_tree[cat.id] = {
                'id': cat.id,
                'category_name': cat.category_name,
                'category_code': cat.category_code,
                'icon': cat.icon,
                'sort': cat.sort,
                'status': cat.status,
                'children': []
            }
    
    for cat in categories:
        if cat.parent_id in category_tree:
            category_tree[cat.parent_id]['children'].append({
                'id': cat.id,
                'category_name': cat.category_name,
                'category_code': cat.category_code,
                'icon': cat.icon,
                'sort': cat.sort,
                'status': cat.status
            })
    
    return render_template('sp_mall_admin/sp_category_list.html', 
                          category_tree=category_tree,
                          categories=categories,
                          segment='sp/category')


@blueprint.route('/category/add', methods=['POST'])
def category_add():
    """添加商品分类"""
    data = request.get_json()
    
    if SpProductCategory.query.filter_by(category_code=data.get('categoryCode')).first():
        return jsonify({'code': 400, 'message': '分类编码已存在', 'data': None})
    
    parent_id = data.get('parentId', 0)
    
    # 验证父分类是否存在（如果不是一级分类）
    if parent_id and parent_id != 0:
        parent = SpProductCategory.query.get(parent_id)
        if not parent:
            return jsonify({'code': 400, 'message': '父分类不存在', 'data': None})
        if parent.parent_id != 0:
            return jsonify({'code': 400, 'message': '最多只支持二级分类', 'data': None})
    
    category = SpProductCategory(
        category_name=data.get('categoryName'),
        category_code=data.get('categoryCode'),
        parent_id=parent_id,
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


@blueprint.route('/category/<int:category_id>', methods=['GET'])
def category_detail(category_id):
    """获取分类详情"""
    category = SpProductCategory.query.get(category_id)
    
    if not category:
        return jsonify({'code': 404, 'message': '分类不存在', 'data': None})
    
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'id': category.id,
            'categoryName': category.category_name,
            'categoryCode': category.category_code,
            'parentId': category.parent_id,
            'icon': category.icon,
            'sort': category.sort,
            'status': category.status
        }
    })


@blueprint.route('/category/<int:category_id>', methods=['PUT'])
def category_update(category_id):
    """更新分类"""
    category = SpProductCategory.query.get(category_id)
    
    if not category:
        return jsonify({'code': 404, 'message': '分类不存在', 'data': None})
    
    data = request.get_json()
    
    existing = SpProductCategory.query.filter(
        SpProductCategory.category_code == data.get('categoryCode'),
        SpProductCategory.id != category_id
    ).first()
    
    if existing:
        return jsonify({'code': 400, 'message': '分类编码已存在', 'data': None})
    
    try:
        category.category_name = data.get('categoryName')
        category.category_code = data.get('categoryCode')
        category.icon = data.get('icon')
        category.sort = data.get('sort', 0)
        category.status = data.get('status', 1)
        
        db.session.commit()
        return jsonify({'code': 200, 'message': '更新成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/category/<int:category_id>', methods=['DELETE'])
def category_delete(category_id):
    """删除分类"""
    category = SpProductCategory.query.get(category_id)
    
    if not category:
        return jsonify({'code': 404, 'message': '分类不存在', 'data': None})
    
    if SpProduct.query.filter_by(category_id=category_id).first():
        return jsonify({'code': 400, 'message': '该分类下存在商品，无法删除', 'data': None})
    
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'code': 200, 'message': '删除成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/product')
def product_list():
    """商品列表"""
    page = request.args.get('page', 1, type=int)
    page_size = 20
    category_id = request.args.get('categoryId', type=int)
    status = request.args.get('status', type=int)
    keyword = request.args.get('keyword')
    
    query = SpProduct.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if status is not None:
        query = query.filter_by(status=status)
    
    if keyword:
        query = query.filter(SpProduct.product_name.like(f'%{keyword}%'))
    
    pagination = query.order_by(SpProduct.sort.desc(), SpProduct.created_at.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )
    
    categories = SpProductCategory.query.filter_by(status=1).order_by(SpProductCategory.sort).all()
    
    return render_template('sp_mall_admin/sp_product_list.html',
                          products=pagination.items,
                          categories=categories,
                          pagination=pagination,
                          current_page=page)


@blueprint.route('/product/add', methods=['POST'])
def product_add():
    """添加商品"""
    data = request.get_json()
    
    # 验证必填字段
    required_fields = ['productName', 'productCode', 'categoryId', 'price', 'mainImage']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'code': 400, 'message': f'缺少必填字段: {field}', 'data': None})
    
    if SpProduct.query.filter_by(product_code=data.get('productCode')).first():
        return jsonify({'code': 400, 'message': '商品编码已存在', 'data': None})
    
    product = SpProduct(
        category_id=data.get('categoryId'),
        product_name=data.get('productName'),
        product_code=data.get('productCode'),
        main_image=data.get('mainImage'),
        images=data.get('images'),
        price=data.get('price'),
        original_price=data.get('originalPrice'),
        member_price=data.get('memberPrice'),
        stock=data.get('stock', 0),
        sales=data.get('sales', 0),
        brief=data.get('brief'),
        description=data.get('description'),
        status=data.get('status', 1),
        is_hot=data.get('isHot', 0),
        is_new=data.get('isNew', 0),
        is_recommend=data.get('isRecommend', 0),
        sort=data.get('sort', 0)
    )
    
    try:
        db.session.add(product)
        db.session.commit()
        logger.info(f'商品添加成功: {product.product_name}, ID: {product.id}, 图片: {product.main_image}')
        return jsonify({'code': 200, 'message': '添加成功', 'data': {'productId': product.id}})
    except Exception as e:
        db.session.rollback()
        logger.error(f'商品添加失败: {str(e)}')
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/product/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    """获取商品详情"""
    product = SpProduct.query.get(product_id)
    
    if not product:
        return jsonify({'code': 404, 'message': '商品不存在', 'data': None})
    
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': product.to_dict(include_detail=True)
    })


@blueprint.route('/product/<int:product_id>', methods=['PUT'])
def product_update(product_id):
    """更新商品"""
    product = SpProduct.query.get(product_id)
    
    if not product:
        return jsonify({'code': 404, 'message': '商品不存在', 'data': None})
    
    data = request.get_json()
    
    # 验证必填字段
    required_fields = ['productName', 'productCode', 'categoryId', 'price', 'mainImage']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'code': 400, 'message': f'缺少必填字段: {field}', 'data': None})
    
    if data.get('productCode') != product.product_code:
        if SpProduct.query.filter(
            SpProduct.product_code == data.get('productCode'),
            SpProduct.id != product_id
        ).first():
            return jsonify({'code': 400, 'message': '商品编码已存在', 'data': None})
    
    try:
        product.category_id = data.get('categoryId')
        product.product_name = data.get('productName')
        product.product_code = data.get('productCode')
        product.main_image = data.get('mainImage')
        product.images = data.get('images')
        product.price = data.get('price')
        product.original_price = data.get('originalPrice')
        product.member_price = data.get('memberPrice')
        product.stock = data.get('stock', 0)
        product.brief = data.get('brief')
        product.description = data.get('description')
        product.status = data.get('status', 1)
        product.is_hot = data.get('isHot', 0)
        product.is_new = data.get('isNew', 0)
        product.is_recommend = data.get('isRecommend', 0)
        product.sort = data.get('sort', 0)
        
        db.session.commit()
        logger.info(f'商品更新成功: {product.product_name}, ID: {product.id}, 图片: {product.main_image}')
        return jsonify({'code': 200, 'message': '更新成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/product/<int:product_id>', methods=['DELETE'])
def product_delete(product_id):
    """删除商品"""
    product = SpProduct.query.get(product_id)
    
    if not product:
        return jsonify({'code': 404, 'message': '商品不存在', 'data': None})
    
    # 检查是否有订单明细关联
    order_items = SpOrderItem.query.filter_by(product_id=product_id).first()
    if order_items:
        return jsonify({
            'code': 400, 
            'message': '该商品已被订单使用，无法删除。如需删除，请先删除关联的订单。', 
            'data': None
        })
    
    try:
        # 先删除关联的SKU
        SpProductSku.query.filter_by(product_id=product_id).delete()
        
        # 删除商品
        db.session.delete(product)
        db.session.commit()
        return jsonify({'code': 200, 'message': '删除成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/product/toggle-status/<int:product_id>', methods=['POST'])
def product_toggle_status(product_id):
    """切换商品上下架状态"""
    product = SpProduct.query.get(product_id)
    
    if not product:
        return jsonify({'code': 404, 'message': '商品不存在', 'data': None})
    
    try:
        product.status = 1 if product.status == 0 else 0
        db.session.commit()
        return jsonify({
            'code': 200,
            'message': '状态更新成功',
            'data': {'status': product.status}
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/order')
def order_list():
    """订单列表"""
    page = request.args.get('page', 1, type=int)
    page_size = 20
    status = request.args.get('status')
    keyword = request.args.get('keyword')
    
    query = SpOrder.query
    
    if status:
        query = query.filter_by(status=status)
    
    if keyword:
        query = query.filter(
            db.or_(
                SpOrder.order_no.like(f'%{keyword}%'),
                SpOrder.receiver_phone.like(f'%{keyword}%'),
                SpOrder.receiver_name.like(f'%{keyword}%')
            )
        )
    
    pagination = query.order_by(SpOrder.created_at.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )
    
    return render_template('sp_mall_admin/sp_order_list.html',
                          orders=pagination.items,
                          pagination=pagination,
                          current_page=page,
                          status=status,
                          keyword=keyword,
                          segment='sp/order')


@blueprint.route('/order/<int:order_id>', methods=['GET'])
def order_detail(order_id):
    """订单详情"""
    order = SpOrder.query.get(order_id)
    
    if not order:
        return jsonify({'code': 404, 'message': '订单不存在', 'data': None})
    
    items = SpOrderItem.query.filter_by(order_id=order_id).all()
    
    return render_template('sp_mall_admin/sp_order_detail.html',
                          order=order,
                          items=items,
                          segment='sp/order')


@blueprint.route('/order/<int:order_id>/ship', methods=['POST'])
def order_ship(order_id):
    """发货"""
    order = SpOrder.query.get(order_id)
    
    if not order:
        return jsonify({'code': 404, 'message': '订单不存在', 'data': None})
    
    if order.status != 'PAID':
        return jsonify({'code': 400, 'message': '只有已支付的订单才能发货', 'data': None})
    
    data = request.get_json()
    
    try:
        order.status = 'SHIPPED'
        order.ship_time = datetime.now()
        order.logistics_company = data.get('logisticsCompany')
        order.logistics_no = data.get('logisticsNo')
        
        db.session.commit()
        return jsonify({'code': 200, 'message': '发货成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/order/<int:order_id>/finish', methods=['POST'])
def order_finish(order_id):
    """完成订单"""
    order = SpOrder.query.get(order_id)
    
    if not order:
        return jsonify({'code': 404, 'message': '订单不存在', 'data': None})
    
    if order.status != 'SHIPPED':
        return jsonify({'code': 400, 'message': '只有已发货的订单才能完成', 'data': None})
    
    try:
        order.status = 'FINISHED'
        order.finish_time = datetime.now()
        
        db.session.commit()
        return jsonify({'code': 200, 'message': '订单已完成', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/order/<int:order_id>/cancel', methods=['POST'])
def order_cancel(order_id):
    """取消订单"""
    order = SpOrder.query.get(order_id)
    
    if not order:
        return jsonify({'code': 404, 'message': '订单不存在', 'data': None})
    
    if order.status not in ['PENDING_PAY', 'PAID']:
        return jsonify({'code': 400, 'message': '当前状态无法取消订单', 'data': None})
    
    data = request.get_json()
    
    try:
        order.status = 'CANCELLED'
        order.cancel_time = datetime.now()
        order.cancel_reason = data.get('reason', '')
        
        for item in order.items:
            product = SpProduct.query.get(item.product_id)
            if product:
                product.stock += item.quantity
        
        db.session.commit()
        return jsonify({'code': 200, 'message': '订单已取消', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/order/stats', methods=['GET'])
def order_stats():
    """订单统计"""
    total = SpOrder.query.count()
    pending_pay = SpOrder.query.filter_by(status='PENDING_PAY').count()
    paid = SpOrder.query.filter_by(status='PAID').count()
    shipped = SpOrder.query.filter_by(status='SHIPPED').count()
    finished = SpOrder.query.filter_by(status='FINISHED').count()
    cancelled = SpOrder.query.filter_by(status='CANCELLED').count()
    
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'total': total,
            'pendingPay': pending_pay,
            'paid': paid,
            'shipped': shipped,
            'finished': finished,
            'cancelled': cancelled
        }
    })
