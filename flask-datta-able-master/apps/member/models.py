# -*- encoding: utf-8 -*-
"""
会员达人模块 - 数据模型
"""

from apps import db
from datetime import datetime


class User(db.Model):
    """用户主表"""
    __tablename__ = 'user'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='用户ID')
    openid = db.Column(db.String(100), nullable=False, unique=True, comment='微信openid')
    unionid = db.Column(db.String(100), nullable=True, comment='微信unionid')
    nickname = db.Column(db.String(100), nullable=True, comment='昵称')
    avatar = db.Column(db.String(500), nullable=True, comment='头像URL')
    phone = db.Column(db.String(20), nullable=True, comment='手机号')
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='状态：1正常 0禁用')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    member = db.relationship('UserMember', backref='user', uselist=False, lazy=True)
    talent_apply = db.relationship('TalentApply', backref='user', uselist=False, lazy=True)
    addresses = db.relationship('UserAddress', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.id}:{self.nickname}>'
    
    @property
    def is_member(self):
        return self.member is not None
    
    @property
    def is_talent(self):
        return self.talent_apply is not None and self.talent_apply.status == 'APPROVED'
    
    def to_dict(self):
        return {
            'userId': self.id,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'phone': self.phone[:3] + '****' + self.phone[-4:] if self.phone else '',
            'isMember': self.is_member,
            'memberLevel': self.member.to_dict()['memberLevel'] if self.member else None,
            'isTalent': self.is_talent,
            'talentStatus': self.talent_apply.status if self.talent_apply else None,
            'talentStatusText': self.talent_apply.status_text if self.talent_apply else '未申请'
        }


class MemberLevel(db.Model):
    """会员等级表"""
    __tablename__ = 'member_level'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='等级ID')
    level_code = db.Column(db.String(20), nullable=False, unique=True, comment='等级编码：normal/vip/partner')
    level_name = db.Column(db.String(50), nullable=False, comment='等级名称')
    discount = db.Column(db.Numeric(3, 2), nullable=False, default=1.00, comment='折扣率，0.95表示95折')
    upgrade_condition = db.Column(db.Text, nullable=True, comment='升级条件描述')
    benefits = db.Column(db.JSON, nullable=True, comment='权益配置JSON')
    sort = db.Column(db.Integer, nullable=False, default=0, comment='排序')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    
    user_members = db.relationship('UserMember', backref='level', lazy='dynamic')
    
    def __repr__(self):
        return f'<MemberLevel {self.level_code}:{self.level_name}>'
    
    def to_dict(self):
        return {
            'levelCode': self.level_code,
            'levelName': self.level_name,
            'discount': float(self.discount),
            'upgradeCondition': self.upgrade_condition,
            'benefits': self.benefits or []
        }


class UserMember(db.Model):
    """用户会员关系表"""
    __tablename__ = 'user_member'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='ID')
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False, unique=True, comment='用户ID')
    level_id = db.Column(db.Integer, db.ForeignKey('member_level.id'), nullable=False, comment='等级ID')
    level_code = db.Column(db.String(20), nullable=False, comment='等级编码')
    upgrade_type = db.Column(db.SmallInteger, nullable=False, default=1, comment='升级方式：1首单自动 2手动 3后台')
    upgrade_time = db.Column(db.DateTime, nullable=True, comment='升级时间')
    first_order_id = db.Column(db.BigInteger, nullable=True, comment='首单订单ID')
    valid_start = db.Column(db.DateTime, nullable=False, comment='有效期开始')
    valid_end = db.Column(db.DateTime, nullable=True, comment='有效期结束，null表示永久')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def __repr__(self):
        return f'<UserMember {self.user_id}:{self.level_code}>'
    
    def to_dict(self):
        level_info = MemberLevel.query.get(self.level_id)
        return {
            'id': self.id,
            'userId': self.user_id,
            'levelCode': self.level_code,
            'levelName': level_info.level_name if level_info else '',
            'discount': float(level_info.discount) if level_info else 1.0,
            'upgradeType': self.upgrade_type,
            'upgradeTime': self.upgrade_time.strftime('%Y-%m-%d %H:%M:%S') if self.upgrade_time else None,
            'validStart': self.valid_start.strftime('%Y-%m-%d %H:%M:%S') if self.valid_start else None,
            'validEnd': self.valid_end.strftime('%Y-%m-%d %H:%M:%S') if self.valid_end else None,
            'memberLevel': level_info.to_dict() if level_info else None
        }


class TalentApply(db.Model):
    """达人申请表"""
    __tablename__ = 'talent_apply'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='申请ID')
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False, unique=True, comment='申请人ID')
    real_name = db.Column(db.String(50), nullable=False, comment='真实姓名')
    phone = db.Column(db.String(20), nullable=False, comment='手机号')
    region = db.Column(db.String(100), nullable=True, comment='所在地区')
    apply_reason = db.Column(db.Text, nullable=True, comment='申请理由')
    intro = db.Column(db.Text, nullable=True, comment='个人简介')
    status = db.Column(db.String(20), nullable=False, default='PENDING', comment='状态：PENDING/APPROVED/REJECTED')
    reject_reason = db.Column(db.String(500), nullable=True, comment='拒绝原因')
    audit_time = db.Column(db.DateTime, nullable=True, comment='审核时间')
    audit_by = db.Column(db.BigInteger, nullable=True, comment='审核人ID')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def __repr__(self):
        return f'<TalentApply {self.user_id}:{self.status}>'
    
    @property
    def status_text(self):
        status_map = {
            'PENDING': '审核中',
            'APPROVED': '已通过',
            'REJECTED': '已拒绝'
        }
        return status_map.get(self.status, '未知')
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'realName': self.real_name,
            'phone': self.phone,
            'region': self.region,
            'applyReason': self.apply_reason,
            'intro': self.intro,
            'status': self.status,
            'statusText': self.status_text,
            'rejectReason': self.reject_reason,
            'auditTime': self.audit_time.strftime('%Y-%m-%d %H:%M:%S') if self.audit_time else None,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class UserAddress(db.Model):
    """用户地址表"""
    __tablename__ = 'user_address'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='地址ID')
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False, comment='用户ID')
    name = db.Column(db.String(50), nullable=False, comment='收货人姓名')
    phone = db.Column(db.String(20), nullable=False, comment='收货人手机号')
    province = db.Column(db.String(50), nullable=False, comment='省份')
    city = db.Column(db.String(50), nullable=False, comment='城市')
    district = db.Column(db.String(50), nullable=False, comment='区县')
    detail = db.Column(db.String(200), nullable=False, comment='详细地址')
    is_default = db.Column(db.SmallInteger, nullable=False, default=0, comment='是否默认：1是 0否')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def __repr__(self):
        return f'<UserAddress {self.user_id}:{self.province}{self.city}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'province': self.province,
            'city': self.city,
            'district': self.district,
            'detail': self.detail,
            'isDefault': self.is_default == 1,
            'fullAddress': f'{self.province}{self.city}{self.district}{self.detail}'
        }


def init_member_levels():
    """初始化会员等级数据"""
    levels = [
        {
            'level_code': 'normal',
            'level_name': '普通用户',
            'discount': 1.00,
            'upgrade_condition': '注册即成为普通用户',
            'benefits': [{'type': 'base', 'name': '基础购物'}]
        },
        {
            'level_code': 'vip',
            'level_name': 'VIP会员',
            'discount': 0.95,
            'upgrade_condition': '完成首单购买自动升级为VIP，享受全场95折优惠',
            'benefits': [
                {'type': 'discount', 'name': '全场95折'},
                {'type': 'points', 'name': '积分翻倍'}
            ]
        },
        {
            'level_code': 'partner',
            'level_name': '合伙人',
            'discount': 0.90,
            'upgrade_condition': '推广业绩达标后可申请成为合伙人',
            'benefits': [
                {'type': 'discount', 'name': '全场9折'},
                {'type': 'commission', 'name': '分销佣金'},
                {'type': 'team', 'name': '团队管理奖'}
            ]
        }
    ]
    
    for level_data in levels:
        if not MemberLevel.query.filter_by(level_code=level_data['level_code']).first():
            db.session.add(MemberLevel(**level_data))
    db.session.commit()
