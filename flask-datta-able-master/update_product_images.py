# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.config import config_dict
from apps import create_app, db
from apps.xp_product.models import Product

config_mode = os.getenv('FLASK_CONFIG', 'Debug')
app = create_app(config_dict[config_mode])

products_data = [
    ("通变灵", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133638273_667834601454.png"),
    ("维生素C维生素E烟酰胺片", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133742208_667834665390.png"),
    ("前力康", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133755787_667834678970.png"),
    ("地龙红曲米颗粒", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133807947_667834691131.png"),
    ("菊苣降舒颗粒", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133820681_667834703866.png"),
    ("菁盈咔咔瘦代餐粉", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133911484_667834754670.png"),
    ("锌镁片", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133928912_667834772099.png"),
    ("黄精茯苓片", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133937739_667834780927.png"),
    ("菁盈咔咔瘦", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133955036_667834798225.png"),
    ("鼻康保健膏", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134017061_667834820251.png"),
    ("肩背康保健液", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134030058_667834833249.png"),
    ("通络关节保健液", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134041346_667834844538.png"),
    ("古方筋络舒祛痛保健液", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134050468_667834853661.png"),
    ("鼻康舒保健膏", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134105268_667834868462.png"),
    ("草本通络保健液", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134117565_667834880760.png"),
    ("强筋健骨保健粉", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134126550_667834889746.png"),
    ("颈肩腰腿康泡浴保健粉", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134137716_667834900913.png"),
    ("排寒排湿足浴保健粉", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134156688_667834919886.png"),
    ("散寒祛湿足浴保健散", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134206098_667834929297.png"),
    ("许安民痔康保健粉", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134225973_667834949173.png"),
    ("紫草舒缓保健膏", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134318638_667835001838.png"),
    ("消痛保健贴", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134330794_667835013996.png"),
    ("眼视力保健膏", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134342228_667835025431.png"),
    ("靓肤美白保健膏", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134354086_667835037290.png"),
    ("润肤抗皱保健膏", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134404591_667835047796.png"),
    ("杰东药业肤康抑菌膏", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134415819_667835059025.png"),
    ("烧烫康肤保健液", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134429269_667835072476.png"),
    ("疮疡生肌保健散", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134445667_667835088875.png"),
    ("鼻舒通保健喷剂", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134454747_667835097956.png"),
    ("首乌人参养发保健膏", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134503147_667835106357.png"),
    ("天竺佰草育养洗发保健粉", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134603509_667835166720.png"),
    ("筋骨康祛痛草本保健液", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134713187_667835236399.png"),
    ("鼻舒宁保健液", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134713187_667835236399.png"),
    ("皮肤抑菌膏", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134730742_667835253956.png"),
    ("筋骨通祛痛保健粉", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134739300_667835262515.png"),
    ("抑菌液", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134750940_667835274156.png"),
    ("皮肤抑菌液", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134759712_667835282929.png"),
    ("中意密芳抑菌液", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134810357_667835293575.png"),
    ("祛痘精华保健液", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134818294_667835301513.png"),
    ("纤体保健贴", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134826387_667835309607.png"),
    ("荆芥皮肤抑菌粉", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134932872_667835376093.png"),
    ("足康保健粉", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134940060_667835383282.png"),
    ("足康保健液", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134948268_667835391491.png"),
    ("筋骨祛痛保健健", "https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134955668_667835398892.png"),
]

with app.app_context():
    updated_count = 0
    for name, image_url in products_data:
        product = Product.query.filter_by(name=name).first()
        if product:
            product.main_image = image_url
            product.images = [image_url]
            updated_count += 1
            print(f"更新: {name}")
    
    db.session.commit()
    print(f"\n共更新 {updated_count} 个商品的图片!")
