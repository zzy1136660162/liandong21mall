# -*- encoding: utf-8 -*-
"""
商品清理脚本
删除除了指定商品之外的所有商品
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps import create_app, db
from apps.sp_mall.sp_models import SpProduct, SpProductSku, SpOrderItem

app = create_app('apps.config.DebugConfig')


def cleanup_products():
    """删除除指定商品外的所有商品"""

    # 需要保留的商品名称列表
    keep_products = [
        '通变灵',
        '维生素 C 维生素 E 烟酰胺片',
        '前力康',
        '地龙红曲米颗粒',
        '菊苣降舒颗粒',
        '菁盈咔咔瘦代餐粉',
        '锌镁片',
        '黄精茯苓片',
        '菁盈咔咔瘦',
        '鼻康保健膏',
        '肩背康保健液',
        '通络关节保健液',
        '古方筋络舒祛痛保健液',
        '鼻康舒保健膏',
        '草本通络保健液',
        '强筋健骨保健粉',
        '颈肩腰腿康泡浴保健粉',
        '排寒排湿足浴保健粉',
        '散寒祛湿足浴保健散',
        '许安民痔康保健粉',
        '紫草舒缓保健膏',
        '消痛保健贴',
        '眼视力保健膏',
        '靓肤美白保健膏',
        '润肤抗皱保健膏',
        '杰东药业 肤康抑菌膏',
        '烧烫康肤保健液',
        '疮疡生肌保健散',
        '鼻舒通保健喷剂',
        '首乌人参养发保健膏',
        '天竺佰草育养洗发保健粉',
        '筋骨康祛痛草本保健液',
        '鼻舒宁保健液',
        '皮肤抑菌膏',
        '筋骨通祛痛保健粉',
        '抑菌液',
        '皮肤抑菌液',
        '中意密芳  抑菌液',
        '祛痘精华保健液',
        '纤体保健贴',
        '荆芥皮肤抑菌粉',
        '足康保健粉',
        '足康保健液',
        '筋骨祛痛保健健'
    ]

    with app.app_context():
        # 获取所有商品
        all_products = SpProduct.query.all()
        print(f'Total products: {len(all_products)}')
        print(f'Products to keep: {len(keep_products)}')

        deleted_count = 0
        kept_count = 0
        skipped_count = 0

        for product in all_products:
            # 检查是否需要保留
            if product.product_name in keep_products:
                kept_count += 1
                print(f'[KEEP] {product.product_name}')
                continue

            # 检查是否有订单关联
            order_items = SpOrderItem.query.filter_by(product_id=product.id).first()
            if order_items:
                print(f'[SKIP] {product.product_name} - has order items')
                skipped_count += 1
                continue

            try:
                # 删除关联的SKU
                SpProductSku.query.filter_by(product_id=product.id).delete()

                # 删除商品
                db.session.delete(product)
                db.session.commit()
                deleted_count += 1
                print(f'[DELETE] {product.product_name}')
            except Exception as e:
                db.session.rollback()
                print(f'[ERROR] {product.product_name} - {str(e)}')
                skipped_count += 1

        print(f'\n[RESULT]')
        print(f'  Kept: {kept_count}')
        print(f'  Deleted: {deleted_count}')
        print(f'  Skipped: {skipped_count}')


if __name__ == '__main__':
    cleanup_products()
