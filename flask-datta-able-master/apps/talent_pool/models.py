# -*- encoding: utf-8 -*-
"""
人才库模块 - 数据模型
"""

from apps import db
from datetime import datetime
import json


class TalentPool(db.Model):
    """人才库表"""
    __tablename__ = 'talent_pool'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    name = db.Column(db.String(50), nullable=False, comment='姓名')
    avatar = db.Column(db.String(500), nullable=True, comment='头像URL')
    title = db.Column(db.String(100), nullable=False, comment='职称/职位')
    region = db.Column(db.String(100), nullable=True, comment='所在地区')
    expertise_areas = db.Column(db.Text, nullable=True, comment='专长领域（JSON数组）')
    skills = db.Column(db.Text, nullable=True, comment='专业技能（JSON数组）')
    experience_years = db.Column(db.Integer, nullable=True, comment='从业年限')
    education = db.Column(db.String(50), nullable=True, comment='学历')
    intro = db.Column(db.Text, nullable=True, comment='个人简介')
    project_experience = db.Column(db.Text, nullable=True, comment='项目经验（JSON数组）')
    achievements = db.Column(db.Text, nullable=True, comment='成果荣誉（JSON数组）')
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='状态：0-隐藏 1-显示')
    sort_order = db.Column(db.Integer, nullable=False, default=0, comment='排序权重')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f'<TalentPool {self.id}:{self.name}>'

    def to_dict(self, include_detail=False):
        result = {
            'id': self.id,
            'name': self.name,
            'avatar': self.avatar or 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
            'title': self.title,
            'region': self.region or '',
            'expertiseAreas': json.loads(self.expertise_areas) if self.expertise_areas else [],
            'experienceYears': self.experience_years or 0,
            'education': self.education or ''
        }

        if include_detail:
            result.update({
                'skills': json.loads(self.skills) if self.skills else [],
                'intro': self.intro or '',
                'projectExperience': json.loads(self.project_experience) if self.project_experience else [],
                'achievements': json.loads(self.achievements) if self.achievements else []
            })

        return result

    def to_admin_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'avatar': self.avatar,
            'title': self.title,
            'region': self.region,
            'expertiseAreas': json.loads(self.expertise_areas) if self.expertise_areas else [],
            'skills': json.loads(self.skills) if self.skills else [],
            'experienceYears': self.experience_years,
            'education': self.education,
            'intro': self.intro,
            'projectExperience': json.loads(self.project_experience) if self.project_experience else [],
            'achievements': json.loads(self.achievements) if self.achievements else [],
            'status': self.status,
            'sortOrder': self.sort_order,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
