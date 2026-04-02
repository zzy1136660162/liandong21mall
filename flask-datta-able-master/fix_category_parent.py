# -*- encoding: utf-8 -*-
import os
from apps import create_app, db
from apps.xp_product.models import Category
from apps.config import config_dict

DEBUG = (os.getenv('DEBUG', 'False') == 'True')
get_config_mode = 'Debug' if DEBUG else 'Production'
app_config = config_dict[get_config_mode.capitalize()]

app = create_app(app_config)
with app.app_context():
    # 创建父分类
    parent1 = Category.query.get(1)
    if not parent1:
        parent1 = Category(id=1, name='体表保健', parent_id=0, level=1, sort=1, status=1)
        db.session.add(parent1)
        print('创建父分类: 体表保健')
    
    parent2 = Category.query.get(2)
    if not parent2:
        parent2 = Category(id=2, name='功能食品', parent_id=0, level=1, sort=2, status=1)
        db.session.add(parent2)
        print('创建父分类: 功能食品')
    
    # 更新所有子分类的parent_id
    # 疼痛舒缓 -> 体表保健
    cats = Category.query.filter(Category.name.in_(['疼痛舒缓', '鼻部护理', '眼部护理', '皮肤护理', '女性调理', '男性养护', '小儿护理', '纤体瘦身', '养发护发', '泡浴养生'])).all()
    for cat in cats:
        cat.parent_id = 1
        cat.level = 2
        print(f'更新分类: {cat.name} -> parent_id=1')
    
    # 人参滋补 -> 功能食品
    cats2 = Category.query.filter(Category.name.in_(['人参滋补', '阿胶膏滋', '草本茶饮', '固体饮料', '压片糖果', '营养颗粒', '植物饮品', '配制酒'])).all()
    for cat in cats2:
        cat.parent_id = 2
        cat.level = 2
        print(f'更新分类: {cat.name} -> parent_id=2')
    
    db.session.commit()
    print('\n修复完成！')
