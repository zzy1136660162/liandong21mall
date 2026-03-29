# -*- encoding: utf-8 -*-
"""
人才库模块 - 服务层
"""

from apps import db
from apps.talent_pool.models import TalentPool
from datetime import datetime
import json


class TalentPoolService:
    """人才库服务"""

    @staticmethod
    def get_talent_list(page=1, page_size=10, area=None, experience=None, keyword=None):
        """获取人才列表"""
        query = TalentPool.query.filter_by(status=1)

        if area:
            query = query.filter(TalentPool.expertise_areas.like(f'%{area}%'))

        if experience:
            if experience == 1:
                query = query.filter(TalentPool.experience_years < 3)
            elif experience == 2:
                query = query.filter(TalentPool.experience_years >= 3, TalentPool.experience_years < 5)
            elif experience == 3:
                query = query.filter(TalentPool.experience_years >= 5)

        if keyword:
            keyword_pattern = f'%{keyword}%'
            query = query.filter(
                db.or_(
                    TalentPool.name.like(keyword_pattern),
                    TalentPool.title.like(keyword_pattern),
                    TalentPool.expertise_areas.like(keyword_pattern),
                    TalentPool.skills.like(keyword_pattern)
                )
            )

        query = query.order_by(TalentPool.sort_order.desc(), TalentPool.id.desc())

        total = query.count()
        talents = query.offset((page - 1) * page_size).limit(page_size).all()

        return {
            'list': [t.to_dict() for t in talents],
            'total': total,
            'currentPage': page,
            'totalPages': (total + page_size - 1) // page_size
        }

    @staticmethod
    def get_talent_detail(talent_id):
        """获取人才详情"""
        talent = TalentPool.query.get(talent_id)
        if not talent or talent.status != 1:
            return None
        return talent.to_dict(include_detail=True)

    @staticmethod
    def get_talent_by_id(talent_id):
        """根据ID获取人才"""
        return TalentPool.query.get(talent_id)

    @staticmethod
    def create_talent(name, title, avatar=None, region=None, expertise_areas=None,
                     skills=None, experience_years=None, education=None, intro=None,
                     project_experience=None, achievements=None, sort_order=0):
        """创建人才"""
        talent = TalentPool(
            name=name,
            avatar=avatar,
            title=title,
            region=region,
            expertise_areas=json.dumps(expertise_areas, ensure_ascii=False) if expertise_areas else None,
            skills=json.dumps(skills, ensure_ascii=False) if skills else None,
            experience_years=experience_years,
            education=education,
            intro=intro,
            project_experience=json.dumps(project_experience, ensure_ascii=False) if project_experience else None,
            achievements=json.dumps(achievements, ensure_ascii=False) if achievements else None,
            sort_order=sort_order,
            status=1
        )
        db.session.add(talent)
        db.session.commit()
        return talent

    @staticmethod
    def update_talent(talent_id, **kwargs):
        """更新人才"""
        talent = TalentPool.query.get(talent_id)
        if not talent:
            return None

        json_fields = ['expertise_areas', 'skills', 'project_experience', 'achievements']

        for key, value in kwargs.items():
            if key in json_fields and value is not None:
                if isinstance(value, list):
                    value = json.dumps(value, ensure_ascii=False)
                setattr(talent, key, value)
            elif hasattr(talent, key):
                setattr(talent, key, value)

        talent.updated_at = datetime.now()
        db.session.commit()
        return talent

    @staticmethod
    def delete_talent(talent_id):
        """删除人才"""
        talent = TalentPool.query.get(talent_id)
        if not talent:
            return False
        db.session.delete(talent)
        db.session.commit()
        return True

    @staticmethod
    def toggle_status(talent_id, status):
        """切换人才状态"""
        talent = TalentPool.query.get(talent_id)
        if not talent:
            return None
        talent.status = status
        talent.updated_at = datetime.now()
        db.session.commit()
        return talent
