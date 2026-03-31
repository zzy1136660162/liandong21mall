# -*- encoding: utf-8 -*-
"""
将商品图片替换为本地图片
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpProduct
import os

app = create_app(config_dict['Debug'])

def replace_with_local_images():
    """将商品图片替换为本地图片"""
    
    with app.app_context():
        print("=" * 60)
        print("替换商品图片为本地图片")
        print("=" * 60)
        
        # 创建图片目录
        base_dir = os.path.dirname(os.path.dirname(__file__))
        images_dir = os.path.join(base_dir, 'static', 'images', 'products')
        
        if not os.path.exists(images_dir):
            os.makedirs(images_dir, exist_ok=True)
            print(f"✓ 创建图片目录: {images_dir}")
        
        # 查询所有商品
        products = SpProduct.query.all()
        
        print(f"\n找到 {len(products)} 个商品需要更新图片\n")
        
        # 为每个商品生成本地图片路径
        updated_count = 0
        for product in products:
            try:
                # 生成本地图片路径
                product_id = product.id
                local_main_image = f"/static/images/products/product_{product_id}_main.jpg"
                
                # 生成本地图片列表（假设每个商品3-5张图片）
                local_images = [
                    f"/static/images/products/product_{product_id}_1.jpg",
                    f"/static/images/products/product_{product_id}_2.jpg",
                    f"/static/images/products/product_{product_id}_3.jpg"
                ]
                
                # 更新商品图片
                product.main_image = local_main_image
                product.images = local_images
                
                updated_count += 1
                print(f"✓ 更新商品: {product.product_name} ({product.product_code})")
                print(f"  主图: {local_main_image}")
                print(f"  图片列表: {len(local_images)} 张")
                
            except Exception as e:
                print(f"✗ 更新失败: {product.product_name} - {e}")
                db.session.rollback()
        
        # 提交更改
        try:
            db.session.commit()
            print(f"\n成功更新 {updated_count} 个商品的图片")
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ 提交失败: {e}")
        
        print("\n" + "=" * 60)
        print("商品图片替换完成！")
        print("=" * 60)
        print("\n注意事项:")
        print("1. 图片目录已创建: static/images/products/")
        print("2. 请将实际商品图片放入该目录")
        print("3. 图片命名格式: product_{商品ID}_main.jpg (主图)")
        print("4. 其他图片命名: product_{商品ID}_1.jpg, product_{商品ID}_2.jpg 等")
        print("5. 图片格式支持: jpg, png, webp 等")

if __name__ == "__main__":
    replace_with_local_images()