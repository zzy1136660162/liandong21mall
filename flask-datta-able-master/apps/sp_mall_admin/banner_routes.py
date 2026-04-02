# -*- encoding: utf-8 -*-
"""
商品商城模块 - 轮播图管理路由
"""

import os
import uuid
from flask import render_template, request, jsonify, current_app
from apps import db
from apps.sp_mall.sp_banner_models import SpBanner
from apps.sp_mall.sp_models import SpProductCategory
from apps.sp_mall_admin import sp_banner_admin_bp as blueprint
import logging

logger = logging.getLogger(__name__)


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})


@blueprint.route('/upload/banner', methods=['POST'])
def upload_banner_image():
    """上传轮播图"""
    try:
        if 'file' not in request.files:
            return jsonify({'code': 400, 'message': '没有文件', 'data': None})
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'code': 400, 'message': '没有选择文件', 'data': None})
        
        if not allowed_file(file.filename):
            return jsonify({'code': 400, 'message': '不支持的文件类型，请上传 JPG、PNG、GIF、WebP 格式的图片', 'data': None})
        
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"banner_{uuid.uuid4().hex}.{ext}"
        
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'banners')
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        file_size = os.path.getsize(filepath)
        logger.info(f'轮播图上传成功: {filename}, 大小: {file_size} bytes')
        
        image_url = f'/static/uploads/banners/{filename}'
        
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
        logger.error(f'轮播图上传失败: {str(e)}')
        return jsonify({'code': 500, 'message': f'上传失败: {str(e)}', 'data': None})


@blueprint.route('')
def banner_list():
    """轮播图列表"""
    position = request.args.get('position')
    status = request.args.get('status', type=int)
    
    query = SpBanner.query
    
    if position:
        query = query.filter_by(position=position)
    
    if status is not None:
        query = query.filter_by(status=status)
    
    banners = query.order_by(SpBanner.sort.desc(), SpBanner.created_at.desc()).all()
    
    return render_template('sp_mall_admin/sp_banner_list.html',
                          banners=banners,
                          segment='sp/banner')


@blueprint.route('/add', methods=['POST'])
def banner_add():
    """添加轮播图"""
    data = request.get_json()
    
    if not data.get('title'):
        return jsonify({'code': 400, 'message': '请输入轮播图标题', 'data': None})
    
    if not data.get('imageUrl'):
        return jsonify({'code': 400, 'message': '请上传轮播图图片', 'data': None})
    
    banner = SpBanner(
        title=data.get('title'),
        image_url=data.get('imageUrl'),
        position=data.get('position', 'home'),
        link_type=data.get('linkType', 'none'),
        link_value=data.get('linkValue'),
        sort=data.get('sort', 0),
        status=data.get('status', 1)
    )
    
    try:
        db.session.add(banner)
        db.session.commit()
        logger.info(f'轮播图添加成功: {banner.title}, ID: {banner.id}, 图片: {banner.image_url}')
        return jsonify({'code': 200, 'message': '添加成功', 'data': {'bannerId': banner.id}})
    except Exception as e:
        db.session.rollback()
        logger.error(f'轮播图添加失败: {str(e)}')
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/<int:banner_id>', methods=['GET'])
def banner_detail(banner_id):
    """获取轮播图详情"""
    banner = SpBanner.query.get(banner_id)
    
    if not banner:
        return jsonify({'code': 404, 'message': '轮播图不存在', 'data': None})
    
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': banner.to_dict()
    })


@blueprint.route('/<int:banner_id>', methods=['PUT'])
def banner_update(banner_id):
    """更新轮播图"""
    banner = SpBanner.query.get(banner_id)
    
    if not banner:
        return jsonify({'code': 404, 'message': '轮播图不存在', 'data': None})
    
    data = request.get_json()
    
    if not data.get('title'):
        return jsonify({'code': 400, 'message': '请输入轮播图标题', 'data': None})
    
    if not data.get('imageUrl'):
        return jsonify({'code': 400, 'message': '请上传轮播图图片', 'data': None})
    
    try:
        banner.title = data.get('title')
        banner.image_url = data.get('imageUrl')
        banner.position = data.get('position', 'home')
        banner.link_type = data.get('linkType', 'none')
        banner.link_value = data.get('linkValue')
        banner.sort = data.get('sort', 0)
        banner.status = data.get('status', 1)
        
        db.session.commit()
        logger.info(f'轮播图更新成功: {banner.title}, ID: {banner.id}')
        return jsonify({'code': 200, 'message': '更新成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        logger.error(f'轮播图更新失败: {str(e)}')
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/<int:banner_id>', methods=['DELETE'])
def banner_delete(banner_id):
    """删除轮播图"""
    banner = SpBanner.query.get(banner_id)
    
    if not banner:
        return jsonify({'code': 404, 'message': '轮播图不存在', 'data': None})
    
    try:
        db.session.delete(banner)
        db.session.commit()
        logger.info(f'轮播图删除成功: ID: {banner_id}')
        return jsonify({'code': 200, 'message': '删除成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        logger.error(f'轮播图删除失败: {str(e)}')
        return jsonify({'code': 500, 'message': str(e), 'data': None})


@blueprint.route('/toggle-status/<int:banner_id>', methods=['POST'])
def banner_toggle_status(banner_id):
    """切换轮播图状态"""
    banner = SpBanner.query.get(banner_id)
    
    if not banner:
        return jsonify({'code': 404, 'message': '轮播图不存在', 'data': None})
    
    try:
        banner.status = 1 if banner.status == 0 else 0
        db.session.commit()
        logger.info(f'轮播图状态切换: ID: {banner_id}, 新状态: {banner.status}')
        return jsonify({'code': 200, 'message': '状态更新成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        logger.error(f'轮播图状态切换失败: {str(e)}')
        return jsonify({'code': 500, 'message': str(e), 'data': None})
