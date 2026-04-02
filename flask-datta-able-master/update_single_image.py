# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.config import config_dict
from apps import create_app, db
from apps.xp_product.models import Product

config_mode = os.getenv('FLASK_CONFIG', 'Debug')
app = create_app(config_dict[config_mode])

with app.app_context():
    # 为筋骨祛痛保健膏添加图片
    product = Product.query.filter_by(name="筋骨祛痛保健膏").first()
    if product:
        image_url = "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401143805659_667838288885.png"
        product.main_image = image_url
        product.images = [image_url]
        db.session.commit()
        print(f"已为 {product.name} 添加图片")
        print(f"图片URL: {image_url}")
    else:
        print("未找到商品: 筋骨祛痛保健膏")
