# -*- encoding: utf-8 -*-
"""
商品商城模块 - 筛选类别API
"""

from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, fields
from apps.sp_mall.sp_filter_category_models import SpFilterCategory, SpCategoryOperationLog
from apps import db
import json
import logging

sp_filter_category_ns = Namespace('filter_category', description='筛选类别API')

logger = logging.getLogger(__name__)


def success_response(data=None, message='success'):
    return {'code': 200, 'message': message, 'data': data}


def error_response(message, code=500):
    return {'code': code, 'message': message, 'data': None}


def get_operator_info():
    """获取操作者信息"""
    try:
        from flask_login import current_user
        if current_user.is_authenticated:
            return {
                'operator_id': current_user.id,
                'operator_name': current_user.username or current_user.name
            }
    except:
        pass

    return {
        'operator_id': 0,
        'operator_name': 'System'
    }


def log_operation(category_id, operation_type, old_data=None, new_data=None, description='', status=1, error_message=None):
    """记录操作日志"""
    try:
        operator_info = get_operator_info()
        operator_ip = request.remote_addr if request else None

        log = SpCategoryOperationLog(
            category_id=category_id,
            operation_type=operation_type,
            operator_id=operator_info.get('operator_id', 0),
            operator_name=operator_info.get('operator_name', 'Unknown'),
            operator_ip=operator_ip,
            old_data=json.dumps(old_data, ensure_ascii=False) if old_data else None,
            new_data=json.dumps(new_data, ensure_ascii=False) if new_data else None,
            description=description,
            status=status,
            error_message=error_message
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        logger.error(f'记录操作日志失败: {str(e)}')
        db.session.rollback()


@sp_filter_category_ns.route('/list')
class SpFilterCategoryList(Resource):
    @sp_filter_category_ns.doc('获取筛选类别列表')
    def get(self):
        """获取所有启用的筛选类别"""
        status = request.args.get('status', type=int)

        query = SpFilterCategory.query

        if status is not None:
            query = query.filter_by(status=status)

        categories = query.order_by(SpFilterCategory.sort.desc(), SpFilterCategory.id).all()

        return success_response([cat.to_dict() for cat in categories])


@sp_filter_category_ns.route('')
class SpFilterCategoryCRUD(Resource):
    @sp_filter_category_ns.doc('创建筛选类别')
    def post(self):
        """创建新的筛选类别"""
        data = request.get_json()

        if not data.get('name'):
            return error_response('类别名称不能为空', 400)

        if not data.get('code'):
            return error_response('类别编码不能为空', 400)

        existing = SpFilterCategory.query.filter_by(code=data['code']).first()
        if existing:
            return error_response('类别编码已存在', 400)

        try:
            category = SpFilterCategory(
                name=data['name'],
                code=data['code'],
                sort=data.get('sort', 0),
                status=data.get('status', 1),
                icon=data.get('icon'),
                color=data.get('color'),
                description=data.get('description'),
                product_count=data.get('productCount', 0)
            )

            db.session.add(category)
            db.session.commit()

            log_operation(
                category.id,
                'CREATE',
                new_data=category.to_dict(),
                description=f'创建筛选类别: {category.name}'
            )

            return success_response(category.to_dict(), '创建成功')

        except Exception as e:
            db.session.rollback()
            logger.error(f'创建筛选类别失败: {str(e)}')
            log_operation(None, 'CREATE', new_data=data, description=f'创建筛选类别失败', status=0, error_message=str(e))
            return error_response(f'创建失败: {str(e)}')

    @sp_filter_category_ns.doc('获取筛选类别列表(管理)')
    def get(self):
        """获取所有筛选类别(管理用)"""
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 20, type=int)
        status = request.args.get('status', type=int)
        keyword = request.args.get('keyword')

        query = SpFilterCategory.query

        if status is not None:
            query = query.filter_by(status=status)

        if keyword:
            query = query.filter(
                db.or_(
                    SpFilterCategory.name.like(f'%{keyword}%'),
                    SpFilterCategory.code.like(f'%{keyword}%')
                )
            )

        pagination = query.order_by(SpFilterCategory.sort.desc(), SpFilterCategory.id).paginate(
            page=page, per_page=page_size, error_out=False
        )

        return success_response({
            'list': [cat.to_dict() for cat in pagination.items],
            'total': pagination.total,
            'page': page,
            'pageSize': page_size,
            'totalPages': (pagination.total + page_size - 1) // page_size
        })


@sp_filter_category_ns.route('/<int:category_id>')
class SpFilterCategoryDetail(Resource):
    @sp_filter_category_ns.doc('获取筛选类别详情')
    def get(self, category_id):
        """获取筛选类别详情"""
        category = SpFilterCategory.query.get(category_id)

        if not category:
            return error_response('类别不存在', 404)

        return success_response(category.to_dict())

    @sp_filter_category_ns.doc('更新筛选类别')
    def put(self, category_id):
        """更新筛选类别"""
        category = SpFilterCategory.query.get(category_id)

        if not category:
            return error_response('类别不存在', 404)

        data = request.get_json()
        old_data = category.to_dict()

        try:
            if 'name' in data:
                category.name = data['name']

            if 'code' in data:
                existing = SpFilterCategory.query.filter(
                    SpFilterCategory.code == data['code'],
                    SpFilterCategory.id != category_id
                ).first()
                if existing:
                    return error_response('类别编码已存在', 400)
                category.code = data['code']

            if 'sort' in data:
                category.sort = data['sort']

            if 'status' in data:
                category.status = data['status']

            if 'icon' in data:
                category.icon = data['icon']

            if 'color' in data:
                category.color = data['color']

            if 'description' in data:
                category.description = data['description']

            if 'productCount' in data:
                category.product_count = data['productCount']

            category.updated_at = datetime.now()
            db.session.commit()

            log_operation(
                category_id,
                'UPDATE',
                old_data=old_data,
                new_data=category.to_dict(),
                description=f'更新筛选类别: {category.name}'
            )

            return success_response(category.to_dict(), '更新成功')

        except Exception as e:
            db.session.rollback()
            logger.error(f'更新筛选类别失败: {str(e)}')
            log_operation(category_id, 'UPDATE', old_data=old_data, description=f'更新筛选类别失败', status=0, error_message=str(e))
            return error_response(f'更新失败: {str(e)}')

    @sp_filter_category_ns.doc('删除筛选类别')
    def delete(self, category_id):
        """删除筛选类别"""
        category = SpFilterCategory.query.get(category_id)

        if not category:
            return error_response('类别不存在', 404)

        old_data = category.to_dict()

        try:
            db.session.delete(category)
            db.session.commit()

            log_operation(
                category_id,
                'DELETE',
                old_data=old_data,
                description=f'删除筛选类别: {old_data["name"]}'
            )

            return success_response(None, '删除成功')

        except Exception as e:
            db.session.rollback()
            logger.error(f'删除筛选类别失败: {str(e)}')
            log_operation(category_id, 'DELETE', old_data=old_data, description=f'删除筛选类别失败', status=0, error_message=str(e))
            return error_response(f'删除失败: {str(e)}')


@sp_filter_category_ns.route('/batch-update')
class SpFilterCategoryBatchUpdate(Resource):
    @sp_filter_category_ns.doc('批量更新筛选类别')
    def post(self):
        """批量更新筛选类别"""
        data = request.get_json()
        categories = data.get('categories', [])

        if not categories:
            return error_response('没有要更新的数据', 400)

        try:
            updated_count = 0
            for item in categories:
                category_id = item.get('id')
                if not category_id:
                    continue

                category = SpFilterCategory.query.get(category_id)
                if not category:
                    continue

                if 'name' in item:
                    category.name = item['name']
                if 'sort' in item:
                    category.sort = item['sort']
                if 'status' in item:
                    category.status = item['status']
                if 'icon' in item:
                    category.icon = item['icon']
                if 'color' in item:
                    category.color = item['color']
                if 'description' in item:
                    category.description = item['description']
                if 'productCount' in item:
                    category.product_count = item['productCount']

                category.updated_at = datetime.now()
                updated_count += 1

            db.session.commit()

            log_operation(
                None,
                'BATCH_UPDATE',
                new_data={'updated_count': updated_count},
                description=f'批量更新 {updated_count} 个筛选类别'
            )

            return success_response({'updatedCount': updated_count}, f'成功更新 {updated_count} 个类别')

        except Exception as e:
            db.session.rollback()
            logger.error(f'批量更新筛选类别失败: {str(e)}')
            log_operation(None, 'BATCH_UPDATE', description=f'批量更新筛选类别失败', status=0, error_message=str(e))
            return error_response(f'批量更新失败: {str(e)}')


@sp_filter_category_ns.route('/toggle-status/<int:category_id>')
class SpFilterCategoryToggleStatus(Resource):
    @sp_filter_category_ns.doc('切换筛选类别状态')
    def post(self, category_id):
        """切换筛选类别启用/禁用状态"""
        category = SpFilterCategory.query.get(category_id)

        if not category:
            return error_response('类别不存在', 404)

        old_status = category.status
        old_data = category.to_dict()

        try:
            category.status = 1 if category.status == 0 else 0
            category.updated_at = datetime.now()
            db.session.commit()

            log_operation(
                category_id,
                'UPDATE',
                old_data={'status': old_status},
                new_data={'status': category.status},
                description=f'切换筛选类别状态: {category.name}'
            )

            return success_response({'status': category.status}, '状态切换成功')

        except Exception as e:
            db.session.rollback()
            logger.error(f'切换状态失败: {str(e)}')
            return error_response(f'状态切换失败: {str(e)}')


@sp_filter_category_ns.route('/export')
class SpFilterCategoryExport(Resource):
    @sp_filter_category_ns.doc('导出筛选类别')
    def get(self):
        """导出所有筛选类别为JSON"""
        categories = SpFilterCategory.query.order_by(SpFilterCategory.sort.desc()).all()

        export_data = {
            'exportTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total': len(categories),
            'categories': [cat.to_dict() for cat in categories]
        }

        log_operation(None, 'EXPORT', new_data={'count': len(categories)}, description='导出筛选类别数据')

        return success_response(export_data, '导出成功')


@sp_filter_category_ns.route('/import')
class SpFilterCategoryImport(Resource):
    @sp_filter_category_ns.doc('导入筛选类别')
    def post(self):
        """导入筛选类别数据"""
        data = request.get_json()
        categories = data.get('categories', [])

        if not categories:
            return error_response('没有要导入的数据', 400)

        try:
            imported_count = 0
            updated_count = 0

            for item in categories:
                code = item.get('code')
                if not code:
                    continue

                existing = SpFilterCategory.query.filter_by(code=code).first()

                if existing:
                    existing.name = item.get('name', existing.name)
                    existing.sort = item.get('sort', existing.sort)
                    existing.status = item.get('status', existing.status)
                    existing.icon = item.get('icon', existing.icon)
                    existing.color = item.get('color', existing.color)
                    existing.description = item.get('description', existing.description)
                    existing.updated_at = datetime.now()
                    updated_count += 1
                else:
                    category = SpFilterCategory(
                        name=item.get('name', ''),
                        code=code,
                        sort=item.get('sort', 0),
                        status=item.get('status', 1),
                        icon=item.get('icon'),
                        color=item.get('color'),
                        description=item.get('description'),
                        product_count=item.get('productCount', 0)
                    )
                    db.session.add(category)
                    imported_count += 1

            db.session.commit()

            log_operation(
                None,
                'IMPORT',
                new_data={'imported': imported_count, 'updated': updated_count},
                description=f'导入筛选类别: 新增{imported_count}个, 更新{updated_count}个'
            )

            return success_response({
                'imported': imported_count,
                'updated': updated_count
            }, f'导入成功: 新增{imported_count}个, 更新{updated_count}个')

        except Exception as e:
            db.session.rollback()
            logger.error(f'导入筛选类别失败: {str(e)}')
            log_operation(None, 'IMPORT', description='导入筛选类别失败', status=0, error_message=str(e))
            return error_response(f'导入失败: {str(e)}')


@sp_filter_category_ns.route('/logs')
class SpCategoryOperationLogs(Resource):
    @sp_filter_category_ns.doc('获取操作日志')
    def get(self):
        """获取类别操作日志"""
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 20, type=int)
        category_id = request.args.get('categoryId', type=int)
        operation_type = request.args.get('operationType')

        query = SpCategoryOperationLog.query

        if category_id:
            query = query.filter_by(category_id=category_id)

        if operation_type:
            query = query.filter_by(operation_type=operation_type)

        pagination = query.order_by(SpCategoryOperationLog.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )

        return success_response({
            'list': [log.to_dict() for log in pagination.items],
            'total': pagination.total,
            'page': page,
            'pageSize': page_size
        })
