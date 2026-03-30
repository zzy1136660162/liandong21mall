# -*- encoding: utf-8 -*-
"""
验证图片更新结果
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpProduct

app = create_app(config_dict['Debug'])

def verify_image_update():
    """验证图片更新结果"""
    
    with app.app_context():
        print("=" * 60)
        print("验证图片更新结果")
        print("=" * 60)
        
        # 查询所有商品
        products = SpProduct.query.all()
        
        print(f"\n总共 {len(products)} 个商品\n")
        
        # 统计图片类型
        network_count = 0
        local_count = 0
        
        for product in products:
            main_image = product.main_image
            if main_image:
                if main_image.startswith('http'):
                    network_count += 1
                    print(f"✗ {product.product_name}: 仍使用网络图片")
                    print(f"   {main_image}")
                elif main_image.startswith('/'):
                    local_count += 1
                    print(f"✓ {product.product_name}: 已使用本地图片")
                    print(f"   {main_image}")
                    print(f"   图片数量: {len(product.images) if product.images else 0}")
                else:
                    print(f"? {product.product_name}: 未知图片格式")
                    print(f"   {main_image}")
            print("-" * 40)
        
        print("\n" + "=" * 60)
        print("统计结果:")
        print("=" * 60)
        print(f"使用本地图片: {local_count} 个")
        print(f"使用网络图片: {network_count} 个")
        print(f"总计: {len(products)} 个")
        
        if network_count == 0:
            print("\n✓ 所有商品图片已成功替换为本地图片！")
        else:
            print(f"\n✗ 还有 {network_count} 个商品使用网络图片")

if __name__ == "__main__":
    verify_image_update()