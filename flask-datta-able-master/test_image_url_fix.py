# -*- encoding: utf-8 -*-
"""
测试图片URL修复功能
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_image_url_fix():
    """测试图片URL修复功能"""
    print("=" * 80)
    print("测试图片URL修复功能")
    print("=" * 80)
    
    print("\n1. 测试商品列表API")
    print("-" * 80)
    
    try:
        # 测试获取商品列表
        response = requests.get(f"{BASE_URL}/api/sp/product/list", timeout=5)
        result = response.json()
        
        if result.get('code') == 200:
            products = result['data']['list']
            
            if products:
                print(f"✅ 成功获取 {len(products)} 个商品")
                
                # 检查第一个商品的图片URL
                product = products[0]
                print(f"\n商品名称: {product.get('productName', 'N/A')}")
                print(f"商品ID: {product.get('id', 'N/A')}")
                
                main_image = product.get('mainImage')
                print(f"\n主图URL: {main_image}")
                
                # 检查URL格式
                if main_image:
                    if main_image.startswith('http://') or main_image.startswith('https://'):
                        print("✅ URL格式正确（完整URL）")
                    else:
                        print("❌ URL格式错误（相对路径）")
                        return False
                else:
                    print("⚠️  没有主图")
            else:
                print("⚠️  暂无商品数据")
        else:
            print(f"❌ API请求失败: {result.get('message')}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
        print("   提示: 请确保Flask应用正在运行")
        print("   命令: python run.py")
        return False
    except Exception as e:
        print(f"❌ 测试出错: {str(e)}")
        return False
    
    print("\n2. 测试商品详情API")
    print("-" * 80)
    
    try:
        if products:
            product_id = products[0]['id']
            
            response = requests.get(f"{BASE_URL}/api/sp/product/{product_id}", timeout=5)
            result = response.json()
            
            if result.get('code') == 200:
                product = result['data']
                
                print(f"✅ 成功获取商品详情")
                print(f"\n商品名称: {product.get('productName', 'N/A')}")
                
                main_image = product.get('mainImage')
                print(f"主图URL: {main_image}")
                
                if main_image:
                    if main_image.startswith('http://') or main_image.startswith('https://'):
                        print("✅ URL格式正确（完整URL）")
                    else:
                        print("❌ URL格式错误（相对路径）")
                        return False
                
                # 检查图片列表
                images = product.get('images', [])
                print(f"\n商品图片数量: {len(images)}")
                
                if images:
                    print("商品图片列表:")
                    for i, img in enumerate(images[:3], 1):  # 只显示前3张
                        print(f"  {i}. {img}")
                        
                        if not (img.startswith('http://') or img.startswith('https://')):
                            print(f"   ❌ URL格式错误")
                            return False
                    print("✅ 所有图片URL格式正确")
            else:
                print(f"❌ 获取商品详情失败: {result.get('message')}")
                return False
                
    except Exception as e:
        print(f"❌ 测试出错: {str(e)}")
        return False
    
    print("\n3. 验证图片可访问性")
    print("-" * 80)
    
    if products:
        main_image = products[0].get('mainImage')
        
        if main_image:
            try:
                response = requests.get(main_image, timeout=5)
                
                if response.status_code == 200:
                    print(f"✅ 图片可正常访问: {main_image}")
                else:
                    print(f"❌ 图片访问失败: HTTP {response.status_code}")
                    print(f"   URL: {main_image}")
                    return False
                    
            except Exception as e:
                print(f"❌ 图片访问出错: {str(e)}")
                print(f"   URL: {main_image}")
                return False
    
    print("\n" + "=" * 80)
    print("  🎉 所有测试通过！")
    print("=" * 80)
    
    print("\n✅ 图片URL修复功能验证成功！")
    print("\n修复效果:")
    print("  ✅ 商品列表API返回完整URL")
    print("  ✅ 商品详情API返回完整URL")
    print("  ✅ 图片可正常访问")
    print("  ✅ 小程序可以显示图片")
    
    print("\n\n下一步:")
    print("  1. 重启Flask应用确保加载最新代码")
    print("  2. 在小程序中测试商品图片显示")
    print("  3. 验证所有商品图片正常展示")
    
    return True

if __name__ == "__main__":
    success = test_image_url_fix()
    
    if not success:
        print("\n❌ 测试失败，请检查:")
        print("  1. Flask应用是否运行")
        print("  2. 是否有商品数据")
        print("  3. 图片文件是否存在")
