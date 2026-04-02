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
    # 检查ID为1的分类
    cat1 = Category.query.get(1)
    if not cat1:
        print("ID 1 不存在，创建体表保健")
        # 由于ID是自增的，不能直接指定ID=1
        # 先找到最大的ID，然后插入
        max_id = db.session.query(db.func.max(Category.id)).scalar() or 0
        print(f"当前最大ID: {max_id}")
        
        # 创建体表保健
        new_cat = Category(name='体表保健', parent_id=0, level=1, sort=1, status=1)
        db.session.add(new_cat)
        db.session.flush()
        
        # 如果新创建的ID不是1，需要更新所有parent_id=1的记录
        new_id = new_cat.id
        print(f"新创建的体表保健ID: {new_id}")
        
        # 更新所有parent_id=1的记录为新的ID
        cats = Category.query.filter_by(parent_id=1).all()
        for cat in cats:
            cat.parent_id = new_id
            print(f"更新 {cat.name} 的parent_id为 {new_id}")
        
        db.session.commit()
        print("修复完成！")
    else:
        print(f"ID 1 已存在: {cat1.name}")
