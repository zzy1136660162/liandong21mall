# -*- encoding: utf-8 -*-
"""
商品数据初始化脚本
创建示例商品数据
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps import create_app, db
from apps.sp_mall.sp_models import SpProductCategory, SpProduct

app = create_app('apps.config.DebugConfig')


def init_products():
    """初始化商品数据"""

    # 商品数据 - 格式：(商品名称, 分类编码, 商品图片URL)
    products_data = [
        # 体表保健 - 疼痛舒缓
        ('通变灵', 'PAIN_RELIEF', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133638273_667834601454.png'),
        ('肩背康保健液', 'PAIN_RELIEF', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134030058_667834833249.png'),
        ('通络关节保健液', 'PAIN_RELIEF', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134041346_667834844538.png'),
        ('古方筋络舒祛痛保健液', 'PAIN_RELIEF', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134050468_667834853661.png'),
        ('草本通络保健液', 'PAIN_RELIEF', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134117565_667834880760.png'),
        ('强筋健骨保健粉', 'PAIN_RELIEF', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134126550_667834889746.png'),
        ('消痛保健贴', 'PAIN_RELIEF', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134330794_667835013996.png'),
        ('筋骨康祛痛草本保健液', 'PAIN_RELIEF', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134713187_667835236399.png'),
        ('筋骨通祛痛保健粉', 'PAIN_RELIEF', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134739300_667835262515.png'),
        ('筋骨祛痛保健健', 'PAIN_RELIEF', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134948268_667835391491.png'),

        # 体表保健 - 鼻部护理
        ('鼻康保健膏', 'NOSE_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134017061_667834820251.png'),
        ('鼻康舒保健膏', 'NOSE_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134105268_667834868462.png'),
        ('鼻舒通保健喷剂', 'NOSE_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134454747_667835097956.png'),
        ('鼻舒宁保健液', 'NOSE_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134713187_667835236399.png'),

        # 体表保健 - 眼部护理
        ('眼视力保健膏', 'EYE_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134342228_667835025431.png'),

        # 体表保健 - 皮肤护理
        ('许安民痔康保健粉', 'SKIN_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134225973_667834949173.png'),
        ('紫草舒缓保健膏', 'SKIN_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134318638_667835001838.png'),
        ('靓肤美白保健膏', 'SKIN_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134354086_667835037290.png'),
        ('润肤抗皱保健膏', 'SKIN_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134404591_667835047796.png'),
        ('杰东药业 肤康抑菌膏', 'SKIN_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134415819_667835059025.png'),
        ('烧烫康肤保健液', 'SKIN_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134429269_667835072476.png'),
        ('疮疡生肌保健散', 'SKIN_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134445667_667835088875.png'),
        ('皮肤抑菌膏', 'SKIN_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134730742_667835253956.png'),
        ('抑菌液', 'SKIN_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134750940_667835274156.png'),
        ('皮肤抑菌液', 'SKIN_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134759712_667835282929.png'),
        ('中意密芳 抑菌液', 'SKIN_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134810357_667835293575.png'),
        ('祛痘精华保健液', 'SKIN_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134818294_667835301513.png'),
        ('荆芥皮肤抑菌粉', 'SKIN_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134932872_667835376093.png'),

        # 体表保健 - 纤体瘦身
        ('菁盈咔咔瘦代餐粉', 'SLIMMING', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133911484_667834754670.png'),
        ('菁盈咔咔瘦', 'SLIMMING', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133955036_667834798225.png'),
        ('纤体保健贴', 'SLIMMING', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134826387_667835309607.png'),

        # 体表保健 - 养发护发
        ('首乌人参养发保健膏', 'HAIR_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134503147_667835106357.png'),
        ('天竺佰草育养洗发保健粉', 'HAIR_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134603509_667835166720.png'),

        # 体表保健 - 泡浴养生
        ('颈肩腰腿康泡浴保健粉', 'BATH_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134137716_667834900913.png'),
        ('排寒排湿足浴保健粉', 'BATH_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134156688_667834919886.png'),
        ('散寒祛湿足浴保健散', 'BATH_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134206098_667834929297.png'),
        ('足康保健粉', 'BATH_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134940060_667835383282.png'),
        ('足康保健液', 'BATH_CARE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401134948268_667835391491.png'),

        # 功能食品 - 营养颗粒
        ('地龙红曲米颗粒', 'NUTRITION_GRANULE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133807947_667834691131.png'),
        ('菊苣降舒颗粒', 'NUTRITION_GRANULE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133820681_667834703866.png'),
        ('黄精茯苓片', 'NUTRITION_GRANULE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133937739_667834780927.png'),

        # 功能食品 - 压片糖果
        ('维生素 C 维生素 E 烟酰胺片', 'TABLET_CANDY', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133742208_667834665390.png'),
        ('锌镁片', 'TABLET_CANDY', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133928912_667834772099.png'),

        # 功能食品 - 配制酒
        ('前力康', 'PREPARED_WINE', 'https://www.lslnii.com/upload/NFSImgFile/appl/images/2025/12/20260401133755787_667834678970.png'),
    ]

    with app.app_context():
        created_count = 0
        skipped_count = 0

        for product_name, category_code, image_url in products_data:
            # 检查商品是否已存在
            existing = SpProduct.query.filter_by(product_name=product_name).first()
            if existing:
                print(f'[SKIP] Product exists: {product_name}')
                skipped_count += 1
                continue

            # 查找分类
            category = SpProductCategory.query.filter_by(category_code=category_code).first()
            if not category:
                print(f'[ERROR] Category not found: {category_code} for product: {product_name}')
                continue

            # 生成商品编码
            product_code = f'PROD{created_count + 1:04d}'

            # 创建商品
            product = SpProduct(
                category_id=category.id,
                product_name=product_name,
                product_code=product_code,
                main_image=image_url,
                images=[image_url],
                price=99.00,
                original_price=199.00,
                member_price=79.00,
                stock=100,
                sales=0,
                brief=f'{product_name}，品质保障',
                status=1,
                is_hot=0,
                is_new=1,
                is_recommend=0,
                sort=created_count + 1
            )

            db.session.add(product)
            print(f'[OK] Create product: {product_name} -> {category.category_name}')
            created_count += 1

        db.session.commit()
        print(f'\n[SUCCESS] Created {created_count} products, skipped {skipped_count} products')


if __name__ == '__main__':
    init_products()
