# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.config import config_dict
from apps import create_app, db
from apps.xp_product.models import Product, Category

config_mode = os.getenv('FLASK_CONFIG', 'Debug')
app = create_app(config_dict[config_mode])

# 正确的商品分类映射
product_category_map = {
    "通变灵": "鼻部护理",
    "维生素C维生素E烟酰胺片": "营养颗粒",
    "前力康": "体表保健",
    "地龙红曲米颗粒": "固体饮料",
    "菊苣降舒颗粒": "固体饮料",
    "菁盈咔咔瘦代餐粉": "纤体瘦身",
    "锌镁片": "营养颗粒",
    "黄精茯苓片": "压片糖果",
    "菁盈咔咔瘦": "纤体瘦身",
    "鼻康保健膏": "鼻部护理",
    "肩背康保健液": "疼痛舒缓",
    "通络关节保健液": "疼痛舒缓",
    "古方筋络舒祛痛保健液": "疼痛舒缓",
    "鼻康舒保健膏": "鼻部护理",
    "草本通络保健液": "疼痛舒缓",
    "强筋健骨保健粉": "疼痛舒缓",
    "颈肩腰腿康泡浴保健粉": "泡浴养生",
    "排寒排湿足浴保健粉": "泡浴养生",
    "散寒祛湿足浴保健散": "泡浴养生",
    "许安民痔康保健粉": "皮肤护理",
    "紫草舒缓保健膏": "皮肤护理",
    "消痛保健贴": "疼痛舒缓",
    "眼视力保健膏": "眼部护理",
    "靓肤美白保健膏": "皮肤护理",
    "润肤抗皱保健膏": "皮肤护理",
    "杰东药业肤康抑菌膏": "皮肤护理",
    "烧烫康肤保健液": "皮肤护理",
    "疮疡生肌保健散": "皮肤护理",
    "鼻舒通保健喷剂": "鼻部护理",
    "首乌人参养发保健膏": "养发护发",
    "天竺佰草育养洗发保健粉": "养发护发",
    "筋骨康祛痛草本保健液": "疼痛舒缓",
    "鼻舒宁保健液": "鼻部护理",
    "皮肤抑菌膏": "皮肤护理",
    "筋骨通祛痛保健粉": "疼痛舒缓",
    "抑菌液": "皮肤护理",
    "皮肤抑菌液": "皮肤护理",
    "中意密芳抑菌液": "皮肤护理",
    "祛痘精华保健液": "皮肤护理",
    "纤体保健贴": "纤体瘦身",
    "荆芥皮肤抑菌粉": "皮肤护理",
    "足康保健粉": "泡浴养生",
    "足康保健液": "泡浴养生",
    "筋骨祛痛保健健": "疼痛舒缓",
    "筋骨祛痛保健膏": "疼痛舒缓",
}

with app.app_context():
    categories = {cat.name: cat.id for cat in Category.query.all()}
    print("分类映射:", categories)
    
    updated_count = 0
    for product_name, category_name in product_category_map.items():
        product = Product.query.filter_by(name=product_name).first()
        if product:
            new_category_id = categories.get(category_name)
            if new_category_id and product.category_id != new_category_id:
                old_id = product.category_id
                product.category_id = new_category_id
                updated_count += 1
                print(f"修复: {product_name} | {old_id} -> {new_category_id} ({category_name})")
    
    db.session.commit()
    print(f"\n共修复 {updated_count} 个商品的分类!")
