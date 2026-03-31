# -*- encoding: utf-8 -*-
"""
登录认证模块 - REST API
"""

import random
import re
import string
from datetime import datetime, timedelta
from flask import request
from flask_restx import Namespace, Resource, fields
from apps import db
from apps.member.models import User

auth_ns = Namespace('auth', description='登录认证API')

verification_codes = {}

def generate_code(length=6):
    """生成随机验证码"""
    return ''.join(random.choices(string.digits, k=length))

def generate_token():
    """生成简单的登录token"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def success_response(data=None, message='success'):
    return {'code': 200, 'message': message, 'data': data}

def error_response(message, code=400):
    return {'code': code, 'message': message, 'data': None}


@auth_ns.route('/send-code')
class SendCode(Resource):
    @auth_ns.doc('发送验证码')
    @auth_ns.expect(auth_ns.model('SendCode', {
        'phone': fields.String(required=True, description='手机号')
    }))
    def post(self):
        """发送验证码"""
        print('=' * 50)
        print('【DEBUG】收到发送验证码请求')
        print(f'【DEBUG】请求方法: {request.method}')
        print(f'【DEBUG】请求URL: {request.url}')
        print(f'【DEBUG】请求头: {dict(request.headers)}')
        data = request.get_json()
        print(f'【DEBUG】请求body数据: {data}')
        phone = data.get('phone')
        print(f'【DEBUG】提取的手机号: {phone}')

        if not phone:
            print('【DEBUG】错误: 手机号为空')
            return error_response('手机号不能为空')

        if not re.match(r'^1[3-9]\d{9}$', phone):
            print(f'【DEBUG】错误: 手机号格式不正确 - {phone}')
            return error_response('手机号格式不正确')

        code = generate_code()
        print(f'【DEBUG】生成的验证码: {code}')
        
        verification_codes[phone] = {
            'code': code,
            'expires': datetime.now() + timedelta(minutes=5),
            'used': False
        }
        
        print(f'【DEBUG】验证码已保存，当前所有验证码: {verification_codes}')
        print(f'【测试用】验证码: {code}')
        print('=' * 50)

        return success_response({
            'expiresIn': 300,
            'message': '验证码已发送'
        }, '验证码已发送')


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc('手机号验证码登录')
    @auth_ns.expect(auth_ns.model('Login', {
        'phone': fields.String(required=True, description='手机号'),
        'code': fields.String(required=True, description='验证码')
    }))
    def post(self):
        """手机号+验证码登录"""
        data = request.get_json()
        phone = data.get('phone')
        code = data.get('code')

        if not phone or not code:
            return error_response('手机号和验证码不能为空')

        code_info = verification_codes.get(phone)
        if not code_info:
            return error_response('请先获取验证码')

        if code_info['used']:
            return error_response('验证码已使用')

        if datetime.now() > code_info['expires']:
            return error_response('验证码已过期')

        if code_info['code'] != code:
            return error_response('验证码错误')

        code_info['used'] = True

        user = User.query.filter_by(phone=phone).first()
        if not user:
            user = User(
                openid=f'phone_{phone}',
                nickname=f'用户{phone[-4:]}',
                phone=phone
            )
            db.session.add(user)
            db.session.commit()

        token = generate_token()

        return success_response({
            'token': token,
            'userInfo': {
                'userId': user.id,
                'nickname': user.nickname,
                'avatar': user.avatar,
                'phone': user.phone[:3] + '****' + user.phone[-4:] if user.phone else '',
                'isMember': user.is_member,
                'memberLevel': user.member.to_dict()['memberLevel'] if user.member else None,
                'isTalent': user.is_talent,
                'talentStatus': user.talent_apply.status if user.talent_apply else None,
                'talentStatusText': user.talent_apply.status_text if user.talent_apply else '未申请'
            }
        }, '登录成功')


@auth_ns.route('/wechat-login')
class WechatLogin(Resource):
    @auth_ns.doc('微信登录')
    @auth_ns.expect(auth_ns.model('WechatLogin', {
        'code': fields.String(required=True, description='微信code'),
        'nickname': fields.String(description='昵称'),
        'avatar': fields.String(description='头像'),
        'gender': fields.Integer(description='性别'),
        'country': fields.String(description='国家'),
        'province': fields.String(description='省份'),
        'city': fields.String(description='城市')
    }))
    def post(self):
        """微信登录"""
        data = request.get_json()
        wx_code = data.get('code')

        if not wx_code:
            return error_response('code不能为空')

        wx_data = self.get_wechat_session(wx_code)
        if not wx_data:
            return error_response('微信登录失败')

        openid = wx_data.get('openid')
        if not openid:
            return error_response('获取openid失败')

        user = User.query.filter_by(openid=openid).first()
        if not user:
            user = User(
                openid=openid,
                unionid=wx_data.get('unionid'),
                nickname=data.get('nickname', '微信用户'),
                avatar=data.get('avatar'),
                phone=data.get('phone')
            )
            db.session.add(user)
            db.session.commit()

        token = generate_token()

        return success_response({
            'token': token,
            'userInfo': {
                'userId': user.id,
                'nickname': user.nickname,
                'avatar': user.avatar,
                'phone': user.phone[:3] + '****' + user.phone[-4:] if user.phone else '',
                'isMember': user.is_member,
                'memberLevel': user.member.to_dict()['memberLevel'] if user.member else None,
                'isTalent': user.is_talent,
                'talentStatus': user.talent_apply.status if user.talent_apply else None,
                'talentStatusText': user.talent_apply.status_text if user.talent_apply else '未申请'
            }
        }, '登录成功')

    def get_wechat_session(self, code):
        """获取微信session"""
        import urllib.request
        import json

        appid = 'your_appid'
        secret = 'your_secret'
        url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'

        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                result = json.loads(response.read().decode())
                return result
        except Exception as e:
            print(f'微信session获取失败: {e}')
            return None