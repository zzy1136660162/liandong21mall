# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.config import config_dict
from apps import create_app, db
from apps.xp_product.models import Category

config_mode = os.getenv('FLASK_CONFIG', 'Debug')
app = create_app(config_dict[config_mode])

with app.app_context():
    Category.query.delete()
    db.session.commit()

    categories_data = [
        ('疼痛舒缓', '体表保健'),
        ('鼻部护理', '体表保健'),
        ('眼部护理', '体表保健'),
        ('皮肤护理', '体表保健'),
        ('女性调理', '体表保健'),
        ('男性养护', '体表保健'),
        ('小儿护理', '体表保健'),
        ('纤体瘦身', '体表保健'),
        ('养发护发', '体表保健'),
        ('泡浴养生', '体表保健'),
        ('人参滋补', '功能食品'),
        ('阿胶膏滋', '功能食品'),
        ('草本茶饮', '功能食品'),
        ('固体饮料', '功能食品'),
        ('压片糖果', '功能食品'),
        ('营养颗粒', '功能食品'),
        ('植物饮品', '功能食品'),
        ('配制酒', '功能食品'),
    ]

    parent_names = ['体表保健', '功能食品']
    parent_ids = {}
    
    for i, name in enumerate(parent_names):
        cat = Category(name=name, parent_id=0, level=1, sort=i+1, status=1)
        db.session.add(cat)
        db.session.flush()
        parent_ids[name] = cat.id

    for name, parent_name in categories_data:
        cat = Category(
            name=name,
            parent_id=parent_ids[parent_name],
            level=2,
            sort=0,
            status=1
        )
        db.session.add(cat)

    db.session.commit()
    print('分类更新完成!')
    
    all_cats = Category.query.order_by(Category.parent_id, Category.sort).all()
    for cat in all_cats:
        print(f'ID: {cat.id}, 名称: {cat.name}, 父ID: {cat.parent_id}, 层级: {cat.level}')
