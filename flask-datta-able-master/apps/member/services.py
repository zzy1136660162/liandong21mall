# -*- encoding: utf-8 -*-
"""
会员达人模块 - 服务层
"""

from apps import db
from apps.member.models import User, UserMember, MemberLevel, TalentApply, UserAddress
from datetime import datetime


class MemberService:
    """会员服务"""
    
    @staticmethod
    def get_user_by_id(user_id):
        """根据ID获取用户"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_openid(openid):
        """根据openid获取用户"""
        return User.query.filter_by(openid=openid).first()
    
    @staticmethod
    def create_user(openid, unionid=None, nickname=None, avatar=None):
        """创建新用户"""
        user = User(
            openid=openid,
            unionid=unionid,
            nickname=nickname,
            avatar=avatar
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_user_info(user_id, **kwargs):
        """更新用户信息"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.session.commit()
        return user
    
    @staticmethod
    def get_member_info(user_id):
        """获取会员信息"""
        user = User.query.get(user_id)
        if not user or not user.member:
            return None
        
        return user.member.to_dict()
    
    @staticmethod
    def upgrade_to_vip(user_id, order_id=None):
        """升级为VIP会员"""
        user = User.query.get(user_id)
        if not user:
            return None, '用户不存在'
        
        if user.member and user.member.level_code == 'vip':
            return user.member.to_dict(), '已是VIP会员'
        
        vip_level = MemberLevel.query.filter_by(level_code='vip').first()
        if not vip_level:
            return None, 'VIP等级不存在'
        
        now = datetime.now()
        
        if user.member:
            user.member.level_id = vip_level.id
            user.member.level_code = 'vip'
            user.member.upgrade_type = 1
            user.member.upgrade_time = now
            user.member.first_order_id = order_id
        else:
            user_member = UserMember(
                user_id=user_id,
                level_id=vip_level.id,
                level_code='vip',
                upgrade_type=1,
                upgrade_time=now,
                first_order_id=order_id,
                valid_start=now,
                valid_end=None
            )
            db.session.add(user_member)
        
        db.session.commit()
        
        return UserMember.query.filter_by(user_id=user_id).first().to_dict(), '升级成功'
    
    @staticmethod
    def get_user_discount(user_id):
        """获取用户折扣"""
        user = User.query.get(user_id)
        if not user or not user.member:
            return 1.0
        
        level = user.member.level
        return float(level.discount) if level else 1.0


class TalentService:
    """达人服务"""
    
    @staticmethod
    def get_talent_status(user_id):
        """获取达人申请状态"""
        apply = TalentApply.query.filter_by(user_id=user_id).first()
        if not apply:
            return {
                'status': None,
                'statusText': '未申请',
                'applyTime': None,
                'auditTime': None,
                'rejectReason': None
            }
        
        return {
            'status': apply.status,
            'statusText': apply.status_text,
            'applyTime': apply.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'auditTime': apply.audit_time.strftime('%Y-%m-%d %H:%M:%S') if apply.audit_time else None,
            'rejectReason': apply.reject_reason
        }
    
    @staticmethod
    def get_talent_info(user_id):
        """获取达人信息"""
        apply = TalentApply.query.filter_by(user_id=user_id, status='APPROVED').first()
        if not apply:
            return None
        
        return apply.to_dict()
    
    @staticmethod
    def submit_apply(user_id, real_name, phone, region=None, apply_reason=None, intro=None):
        """提交达人申请"""
        existing = TalentApply.query.filter_by(user_id=user_id).first()
        
        if existing:
            if existing.status == 'PENDING':
                return None, '已有待审核的申请'
            if existing.status == 'APPROVED':
                return None, '已是达人，无需重复申请'
        
        if existing and existing.status == 'REJECTED':
            existing.real_name = real_name
            existing.phone = phone
            existing.region = region
            existing.apply_reason = apply_reason
            existing.intro = intro
            existing.status = 'PENDING'
            existing.reject_reason = None
            existing.audit_time = None
            existing.created_at = datetime.now()
            db.session.commit()
            return existing.to_dict(), '申请提交成功'
        
        apply = TalentApply(
            user_id=user_id,
            real_name=real_name,
            phone=phone,
            region=region,
            apply_reason=apply_reason,
            intro=intro,
            status='PENDING'
        )
        db.session.add(apply)
        db.session.commit()
        
        return apply.to_dict(), '申请提交成功'
    
    @staticmethod
    def audit_apply(apply_id, audit_result, reject_reason=None, audit_by=None):
        """审核达人申请"""
        apply = TalentApply.query.get(apply_id)
        if not apply:
            return None, '申请不存在'
        
        if audit_result == 'approve':
            apply.status = 'APPROVED'
        else:
            apply.status = 'REJECTED'
            apply.reject_reason = reject_reason
        
        apply.audit_time = datetime.now()
        apply.audit_by = audit_by
        
        db.session.commit()
        
        return apply.to_dict(), '审核完成'
    
    @staticmethod
    def is_talent(user_id):
        """判断用户是否为达人"""
        apply = TalentApply.query.filter_by(user_id=user_id, status='APPROVED').first()
        return apply is not None


class AddressService:
    """地址服务"""
    
    @staticmethod
    def get_address_list(user_id):
        """获取用户地址列表"""
        addresses = UserAddress.query.filter_by(user_id=user_id).order_by(UserAddress.is_default.desc(), UserAddress.created_at.desc()).all()
        return [addr.to_dict() for addr in addresses]
    
    @staticmethod
    def get_address(user_id, address_id):
        """获取地址详情"""
        return UserAddress.query.filter_by(id=address_id, user_id=user_id).first()
    
    @staticmethod
    def create_address(user_id, name, phone, province, city, district, detail, is_default=0):
        """创建地址"""
        if is_default == 1:
            UserAddress.query.filter_by(user_id=user_id, is_default=1).update({'is_default': 0})
        
        address = UserAddress(
            user_id=user_id,
            name=name,
            phone=phone,
            province=province,
            city=city,
            district=district,
            detail=detail,
            is_default=is_default
        )
        db.session.add(address)
        db.session.commit()
        
        return address.to_dict()
    
    @staticmethod
    def update_address(user_id, address_id, **kwargs):
        """更新地址"""
        address = UserAddress.query.filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return None
        
        if 'is_default' in kwargs and kwargs['is_default'] == 1:
            UserAddress.query.filter_by(user_id=user_id, is_default=1).update({'is_default': 0})
        
        for key, value in kwargs.items():
            if hasattr(address, key):
                setattr(address, key, value)
        
        db.session.commit()
        
        return address.to_dict()
    
    @staticmethod
    def delete_address(user_id, address_id):
        """删除地址"""
        address = UserAddress.query.filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return False
        
        db.session.delete(address)
        db.session.commit()
        
        return True
