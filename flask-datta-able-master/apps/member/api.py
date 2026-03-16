# -*- encoding: utf-8 -*-
"""
会员达人模块 - REST API
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from apps.member.services import MemberService, TalentService, AddressService
from apps.member.models import init_member_levels
from apps import db

api = Namespace('user', description='用户相关API')

# 数据模型定义
user_info_model = api.model('UserInfo', {
    'userId': fields.Integer(description='用户ID'),
    'nickname': fields.String(description='昵称'),
    'avatar': fields.String(description='头像URL'),
    'phone': fields.String(description='手机号'),
    'isMember': fields.Boolean(description='是否会员'),
    'memberLevel': fields.Raw(description='会员等级信息'),
    'isTalent': fields.Boolean(description='是否达人'),
    'talentStatus': fields.String(description='达人申请状态'),
    'talentStatusText': fields.String(description='达人申请状态文本')
})

member_info_model = api.model('MemberInfo', {
    'isMember': fields.Boolean(description='是否会员'),
    'levelCode': fields.String(description='等级编码'),
    'levelName': fields.String(description='等级名称'),
    'discount': fields.Float(description='折扣率'),
    'upgradeTime': fields.String(description='升级时间'),
    'validStart': fields.String(description='有效期开始'),
    'validEnd': fields.String(description='有效期结束'),
    'benefits': fields.Raw(description='权益列表'),
    'upgradeCondition': fields.String(description='升级条件')
})


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


@api.route('/info')
class UserInfo(Resource):
    @api.doc('获取用户信息')
    def get(self):
        """获取当前用户信息"""
        user_id = get_current_user_id()
        user = MemberService.get_user_by_id(user_id)
        
        if not user:
            return error_response('用户不存在', 404)
        
        return success_response(user.to_dict())
    
    @api.doc('修改用户信息')
    def put(self):
        """修改用户信息"""
        user_id = get_current_user_id()
        data = request.get_json()
        
        user = MemberService.update_user_info(user_id, **data)
        if not user:
            return error_response('用户不存在', 404)
        
        return success_response(user.to_dict(), '修改成功')


@api.route('/member')
class UserMember(Resource):
    @api.doc('获取会员状态')
    def get(self):
        """查询会员状态"""
        user_id = get_current_user_id()
        member_info = MemberService.get_member_info(user_id)
        
        if not member_info:
            return success_response({
                'isMember': False,
                'levelCode': 'normal',
                'levelName': '普通用户',
                'discount': 1.0,
                'upgradeTime': None,
                'validStart': None,
                'validEnd': None,
                'benefits': [{'type': 'base', 'name': '基础购物'}],
                'upgradeCondition': '完成首单购买自动升级为VIP'
            })
        
        return success_response(member_info)


@api.route('/member/upgrade')
class MemberUpgrade(Resource):
    @api.doc('首单升级VIP')
    def post(self):
        """首单自动升级VIP"""
        user_id = get_current_user_id()
        data = request.get_json()
        order_id = data.get('orderId')
        
        result, message = MemberService.upgrade_to_vip(user_id, order_id)
        
        if not result:
            return error_response(message)
        
        return success_response(result, message)


# ========== 达人相关API ==========

talent_ns = Namespace('user/talent', description='达人相关API')


@talent_ns.route('/apply')
class TalentApply(Resource):
    @api.doc('提交达人申请')
    def post(self):
        """提交达人申请"""
        user_id = get_current_user_id()
        data = request.get_json()
        
        if not data.get('realName') or not data.get('phone') or not data.get('applyReason'):
            return error_response('请填写完整信息')
        
        result, message = TalentService.submit_apply(
            user_id=user_id,
            real_name=data.get('realName'),
            phone=data.get('phone'),
            region=data.get('region'),
            apply_reason=data.get('applyReason'),
            intro=data.get('intro')
        )
        
        if not result:
            return error_response(message)
        
        return success_response(result, message)


@talent_ns.route('/status')
class TalentStatus(Resource):
    @api.doc('查询达人申请状态')
    def get(self):
        """查询达人申请状态"""
        user_id = get_current_user_id()
        status = TalentService.get_talent_status(user_id)
        
        return success_response(status)


@talent_ns.route('/info')
class TalentInfo(Resource):
    @api.doc('获取达人信息')
    def get(self):
        """获取达人信息"""
        user_id = get_current_user_id()
        talent_info = TalentService.get_talent_info(user_id)
        
        if not talent_info:
            return error_response('您还不是达人', 404)
        
        return success_response({
            'isTalent': True,
            'talentInfo': talent_info,
            'stats': {
                'promotionCount': 0,
                'sampleCount': 0,
                'demandCount': 0
            }
        })
