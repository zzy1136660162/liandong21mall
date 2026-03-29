# -*- encoding: utf-8 -*-
"""
人才库模块 - REST API
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from apps.talent_pool.services import TalentPoolService

api = Namespace('talent_pool', description='人才库API')

talent_model = api.model('Talent', {
    'id': fields.Integer(description='人才ID'),
    'name': fields.String(description='姓名'),
    'avatar': fields.String(description='头像URL'),
    'title': fields.String(description='职称/职位'),
    'region': fields.String(description='所在地区'),
    'expertiseAreas': fields.List(fields.String, description='专长领域'),
    'skills': fields.List(fields.String, description='专业技能'),
    'experienceYears': fields.Integer(description='从业年限'),
    'education': fields.String(description='学历'),
    'intro': fields.String(description='个人简介'),
    'projectExperience': fields.Raw(description='项目经验'),
    'achievements': fields.List(fields.String, description='成果荣誉')
})

talent_list_model = api.model('TalentList', {
    'list': fields.List(fields.Nested(talent_model), description='人才列表'),
    'total': fields.Integer(description='总数'),
    'currentPage': fields.Integer(description='当前页'),
    'totalPages': fields.Integer(description='总页数')
})


def success_response(data=None, message='success'):
    return {'code': 200, 'message': message, 'data': data}


def error_response(message, code=400):
    return {'code': code, 'message': message, 'data': None}


@api.route('/list')
class TalentList(Resource):
    @api.doc('获取人才列表')
    @api.param('page', '页码', type=int, default=1)
    @api.param('pageSize', '每页条数', type=int, default=10)
    @api.param('area', '领域筛选')
    @api.param('experience', '经验筛选 1:1-3年 2:3-5年 3:5年以上', type=int)
    @api.param('keyword', '搜索关键词')
    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)
        area = request.args.get('area')
        experience = request.args.get('experience', type=int)
        keyword = request.args.get('keyword')

        if page_size > 50:
            page_size = 50

        result = TalentPoolService.get_talent_list(
            page=page,
            page_size=page_size,
            area=area,
            experience=experience,
            keyword=keyword
        )

        return success_response(result)


@api.route('/detail/<int:talent_id>')
@api.param('talent_id', '人才ID')
class TalentDetail(Resource):
    @api.doc('获取人才详情')
    def get(self, talent_id):
        talent = TalentPoolService.get_talent_detail(talent_id)

        if not talent:
            return error_response('人才不存在', 404)

        return success_response(talent)


@api.route('/create')
class TalentCreate(Resource):
    @api.doc('创建人才')
    def post(self):
        data = request.get_json()

        if not data.get('name') or not data.get('title'):
            return error_response('姓名和职称不能为空')

        talent = TalentPoolService.create_talent(
            name=data.get('name'),
            title=data.get('title'),
            avatar=data.get('avatar'),
            region=data.get('region'),
            expertise_areas=data.get('expertiseAreas'),
            skills=data.get('skills'),
            experience_years=data.get('experienceYears'),
            education=data.get('education'),
            intro=data.get('intro'),
            project_experience=data.get('projectExperience'),
            achievements=data.get('achievements'),
            sort_order=data.get('sortOrder', 0)
        )

        return success_response(talent.to_admin_dict(), '创建成功')


@api.route('/update/<int:talent_id>')
@api.param('talent_id', '人才ID')
class TalentUpdate(Resource):
    @api.doc('更新人才')
    def put(self, talent_id):
        data = request.get_json()

        talent = TalentPoolService.update_talent(talent_id, **data)

        if not talent:
            return error_response('人才不存在', 404)

        return success_response(talent.to_admin_dict(), '更新成功')


@api.route('/delete/<int:talent_id>')
@api.param('talent_id', '人才ID')
class TalentDelete(Resource):
    @api.doc('删除人才')
    def delete(self, talent_id):
        result = TalentPoolService.delete_talent(talent_id)

        if not result:
            return error_response('人才不存在', 404)

        return success_response(None, '删除成功')


@api.route('/toggle_status/<int:talent_id>')
@api.param('talent_id', '人才ID')
class TalentToggleStatus(Resource):
    @api.doc('切换人才状态')
    def post(self, talent_id):
        data = request.get_json()
        status = data.get('status', 1)

        talent = TalentPoolService.toggle_status(talent_id, status)

        if not talent:
            return error_response('人才不存在', 404)

        return success_response(talent.to_admin_dict(), '状态更新成功')
