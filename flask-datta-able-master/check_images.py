# -*- encoding: utf-8 -*-
"""
检查数据库中的图片资源
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpProduct
import os

app = create_app(config_dict['Debug'])

def check_images():
    """检查图片资源"""
    
    with app.app_context():
        print("=" * 60)
        print("检查数据库图片资源")
        print("=" * 60)
        
        # 查询所有商品
        products = SpProduct.query.all()
        
        print(f"\n总共 {len(products)} 个商品\n")
        
        # 检查静态文件目录
        static_dirs = [
            'static/images/products',
            'static/uploads',
            'static/media',
            'apps/sp_mall/static/images'
        ]
        
        print("检查静态文件目录:")
        for dir_path in static_dirs:
            full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), dir_path)
            if os.path.exists(full_path):
                files = os.listdir(full_path)
                print(f"✓ {dir_path}: {len(files)} 个文件")
                # 显示前5个文件
                for i, file in enumerate(files[:5]):
                    print(f"  - {file}")
                if len(files) > 5:
                    print(f"  ... 还有 {len(files)-5} 个文件")
            else:
                print(f"✗ {dir_path}: 不存在")
        
        print("\n" + "=" * 60)
        print("当前商品图片使用情况:")
        print("=" * 60)
        
        # 统计图片来源
        network_images = []
        local_images = []
        
        for product in products:
            main_image = product.main_image
            if main_image:
                if main_image.startswith('http'):
                    network_images.append(product.product_name)
                elif main_image.startswith('/'):
                    local_images.append(product.product_name)
        
        print(f"\n使用网络图片的商品: {len(network_images)} 个")
        for name in network_images[:5]:
            print(f"  - {name}")
        if len(network_images) > 5:
            print(f"  ... 还有 {len(network_images)-5} 个")
        
        print(f"\n使用本地图片的商品: {len(local_images)} 个")
        for name in local_images[:5]:
            print(f"  - {name}")
        if len(local_images) > 5:
            print(f"  ... 还有 {len(local_images)-5} 个")

if __name__ == "__main__":
    check_images()