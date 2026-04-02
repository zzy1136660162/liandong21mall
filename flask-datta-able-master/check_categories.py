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
    print("所有分类：")
    print("-" * 60)
    cats = Category.query.order_by(Category.id).all()
    for cat in cats:
        print(f"ID: {cat.id}, 名称: {cat.name}, parent_id: {cat.parent_id}, level: {cat.level}")
    print("-" * 60)
