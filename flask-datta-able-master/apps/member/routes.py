# -*- encoding: utf-8 -*-
"""
会员达人模块 - 后台管理路由
"""

import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from apps.member.services import MemberService, TalentService, AddressService
from apps.member.models import User, MemberLevel, TalentApply, UserAddress, init_member_levels
from apps import db

blueprint = Blueprint('member', __name__, url_prefix='/admin/member')


@blueprint.route('/')
@login_required
def index():
    """会员管理首页"""
    return render_template('member/index.html')


@blueprint.route('/user/list')
@login_required
def user_list():
    """用户列表"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    keyword = request.args.get('keyword', '')
    
    query = User.query
    if keyword:
        query = query.filter(
            (User.nickname.like(f'%{keyword}%')) | 
            (User.phone.like(f'%{keyword}%'))
        )
    
    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    users = pagination.items
    
    return render_template('member/user_list.html', 
                          users=users, 
                          pagination=pagination,
                          keyword=keyword)


@blueprint.route('/user/<int:user_id>')
@login_required
def user_detail(user_id):
    """用户详情"""
    user = User.query.get_or_404(user_id)
    member_info = MemberService.get_member_info(user_id)
    talent_status = TalentService.get_talent_status(user_id)
    addresses = AddressService.get_address_list(user_id)
    
    return render_template('member/user_detail.html',
                          user=user,
                          member_info=member_info,
                          talent_status=talent_status,
                          addresses=addresses)


@blueprint.route('/level')
@login_required
def member_level():
    """会员等级配置"""
    levels = MemberLevel.query.order_by(MemberLevel.sort).all()
    
    # 处理数据库中可能存储的字符串格式JSON
    for level in levels:
        if level.benefits and isinstance(level.benefits, str):
            try:
                level.benefits = json.loads(level.benefits)
            except json.JSONDecodeError:
                level.benefits = []
    
    return render_template('member/member_level.html', levels=levels)


@blueprint.route('/level/edit/<int:level_id>', methods=['GET', 'POST'])
@login_required
def level_edit(level_id):
    """编辑会员等级"""
    level = MemberLevel.query.get_or_404(level_id)
    
    # 处理数据库中可能存储的字符串格式JSON
    if level.benefits and isinstance(level.benefits, str):
        try:
            level.benefits = json.loads(level.benefits)
        except json.JSONDecodeError:
            level.benefits = []
    
    if request.method == 'POST':
        level.level_name = request.form.get('level_name')
        level.discount = request.form.get('discount')
        level.upgrade_condition = request.form.get('upgrade_condition')
        
        # 处理权益配置，从表单字段构建JSON
        benefits = []
        benefit1 = request.form.get('benefit1')
        benefit2 = request.form.get('benefit2')
        benefit3 = request.form.get('benefit3')
        
        if benefit1:
            benefits.append({'type': 'discount', 'name': benefit1})
        if benefit2:
            benefits.append({'type': 'points', 'name': benefit2})
        if benefit3:
            benefits.append({'type': 'commission', 'name': benefit3})
        
        level.benefits = benefits
        db.session.commit()
        flash('保存成功', 'success')
        return redirect(url_for('member.member_level'))
    
    return render_template('member/level_edit.html', level=level)


@blueprint.route('/level/add', methods=['GET', 'POST'])
@login_required
def level_add():
    """新增会员等级"""
    if request.method == 'POST':
        level_code = request.form.get('level_code')
        existing = MemberLevel.query.filter_by(level_code=level_code).first()
        if existing:
            flash('等级编码已存在', 'danger')
            return redirect(url_for('member.level_add'))
        
        # 处理权益配置，从表单字段构建JSON
        benefits = []
        benefit1 = request.form.get('benefit1')
        benefit2 = request.form.get('benefit2')
        benefit3 = request.form.get('benefit3')
        
        if benefit1:
            benefits.append({'type': 'discount', 'name': benefit1})
        if benefit2:
            benefits.append({'type': 'points', 'name': benefit2})
        if benefit3:
            benefits.append({'type': 'commission', 'name': benefit3})
        
        level = MemberLevel(
            level_code=level_code,
            level_name=request.form.get('level_name'),
            discount=request.form.get('discount'),
            upgrade_condition=request.form.get('upgrade_condition'),
            benefits=benefits,
            sort=request.form.get('sort', 0)
        )
        db.session.add(level)
        db.session.commit()
        flash('创建成功', 'success')
        return redirect(url_for('member.member_level'))
    
    return render_template('member/level_edit.html', level=None)


@blueprint.route('/level/delete/<int:level_id>', methods=['POST'])
@login_required
def level_delete(level_id):
    """删除会员等级"""
    level = MemberLevel.query.get_or_404(level_id)
    
    if level.user_members.count() > 0:
        flash('该等级下有会员，无法删除', 'danger')
        return redirect(url_for('member.member_level'))
    
    db.session.delete(level)
    db.session.commit()
    flash('删除成功', 'success')
    return redirect(url_for('member.member_level'))


@blueprint.route('/user/toggle/<int:user_id>', methods=['POST'])
@login_required
def user_toggle_status(user_id):
    """启用/禁用用户"""
    user = User.query.get_or_404(user_id)
    user.status = 0 if user.status == 1 else 1
    db.session.commit()
    
    status_text = '禁用' if user.status == 0 else '启用'
    flash(f'用户已{status_text}', 'success')
    return redirect(url_for('member.user_detail', user_id=user_id))


@blueprint.route('/talent/apply')
@login_required
def talent_apply_list():
    """达人申请列表"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    status = request.args.get('status', '')
    
    query = TalentApply.query
    if status:
        query = query.filter_by(status=status)
    
    pagination = query.order_by(TalentApply.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    applies = pagination.items
    
    return render_template('member/talent_apply_list.html',
                          applies=applies,
                          pagination=pagination,
                          status=status)


@blueprint.route('/talent/audit/<int:apply_id>', methods=['GET', 'POST'])
@login_required
def talent_audit(apply_id):
    """达人申请审核"""
    apply = TalentApply.query.get_or_404(apply_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        reject_reason = request.form.get('reject_reason', '')
        
        if action == 'approve':
            apply.status = 'APPROVED'
            message = '审核通过'
        else:
            apply.status = 'REJECTED'
            apply.reject_reason = reject_reason
            message = '已拒绝'
        
        from datetime import datetime
        apply.audit_time = datetime.now()
        apply.audit_by = current_user.id
        db.session.commit()
        
        flash(message, 'success')
        return redirect(url_for('member.talent_apply_list'))
    
    return render_template('member/talent_audit.html', apply=apply)


@blueprint.route('/talent/list')
@login_required
def talent_list():
    """达人列表"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    query = TalentApply.query.filter_by(status='APPROVED')
    pagination = query.order_by(TalentApply.audit_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    talents = pagination.items
    
    return render_template('member/talent_list.html',
                          talents=talents,
                          pagination=pagination)


def init_module(app):
    """初始化模块"""
    # 注册蓝图
    app.register_blueprint(blueprint)
    
    # 初始化会员等级数据
    with app.app_context():
        init_member_levels()
