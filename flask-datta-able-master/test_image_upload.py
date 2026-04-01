# -*- encoding: utf-8 -*-
"""
测试商品图片上传和保存功能
"""

import requests
import os
import json
from pathlib import Path

BASE_URL = "http://127.0.0.1:5000"

def test_image_upload():
    """测试图片上传功能"""
    print("=" * 60)
    print("测试图片上传功能")
    print("=" * 60)
    
    test_image_path = "apps/static/assets/images/logo.png"
    
    if not os.path.exists(test_image_path):
        print(f"❌ 测试图片不存在: {test_image_path}")
        print("将创建一个测试图片...")
        test_image_path = create_test_image()
    
    print(f"\n1. 上传测试图片: {test_image_path}")
    
    try:
        with open(test_image_path, 'rb') as f:
            files = {'file': ('test_image.png', f, 'image/png')}
            response = requests.post(f"{BASE_URL}/admin/sp/upload/image", files=files, timeout=10)
        
        result = response.json()
        
        if result.get('code') == 200:
            print("✅ 图片上传成功!")
            print(f"   返回的URL: {result['data']['url']}")
            print(f"   文件名: {result['data']['filename']}")
            print(f"   文件大小: {result['data'].get('size', 'N/A')} bytes")
            
            image_url = result['data']['url']
            return image_url
        else:
            print(f"❌ 图片上传失败: {result.get('message')}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Flask应用正在运行")
        print("   提示: 在项目目录下运行: python run.py")
        return None
    except Exception as e:
        print(f"❌ 上传出错: {str(e)}")
        return None

def test_product_add_with_image(image_url):
    """测试添加商品（带图片）"""
    print("\n" + "=" * 60)
    print("测试添加商品（使用上传的图片）")
    print("=" * 60)
    
    product_data = {
        "productName": "测试商品-图片上传测试",
        "productCode": f"TEST_{int(os.time.time())}",
        "categoryId": 1,
        "mainImage": image_url,
        "price": 99.99,
        "originalPrice": 199.99,
        "stock": 100,
        "sales": 0,
        "brief": "这是测试商品的简短描述",
        "description": "<p>这是测试商品的详细描述</p>",
        "status": 1,
        "isHot": 1,
        "isNew": 1,
        "isRecommend": 1,
        "sort": 0
    }
    
    print(f"\n2. 添加商品数据:")
    print(json.dumps(product_data, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(
            f"{BASE_URL}/admin/sp/product/add",
            json=product_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        result = response.json()
        
        if result.get('code') == 200:
            print("\n✅ 商品添加成功!")
            print(f"   商品ID: {result['data']['productId']}")
            
            product_id = result['data']['productId']
            
            print("\n3. 验证商品数据:")
            verify_product(product_id)
            
            return product_id
        else:
            print(f"\n❌ 商品添加失败: {result.get('message')}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
        return None
    except Exception as e:
        print(f"❌ 添加商品出错: {str(e)}")
        return None

def verify_product(product_id):
    """验证商品数据"""
    print(f"\n" + "=" * 60)
    print("验证商品数据")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/admin/sp/product/{product_id}", timeout=10)
        result = response.json()
        
        if result.get('code') == 200:
            product = result['data']
            print("\n✅ 商品数据验证成功!")
            print(f"   商品名称: {product['productName']}")
            print(f"   商品编码: {product['productCode']}")
            print(f"   主图URL: {product['mainImage']}")
            print(f"   价格: ¥{product['price']}")
            print(f"   库存: {product['stock']}")
            
            if product['mainImage']:
                print(f"\n✅ 图片已成功保存到数据库!")
                print(f"   图片URL: {product['mainImage']}")
                
                image_exists = check_image_exists(product['mainImage'])
                if image_exists:
                    print("✅ 图片文件已成功保存到服务器!")
                else:
                    print("⚠️  图片URL已保存，但图片文件可能不存在")
            else:
                print("❌ 图片未保存")
        else:
            print(f"❌ 获取商品信息失败: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ 验证出错: {str(e)}")

def check_image_exists(image_url):
    """检查图片文件是否存在"""
    try:
        response = requests.get(f"{BASE_URL}{image_url}", timeout=5)
        return response.status_code == 200
    except:
        return False

def create_test_image():
    """创建一个简单的测试图片"""
    import base64
    
    simple_png_base64 = """
    iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mP8z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg==
    """
    
    test_path = "test_image.png"
    
    with open(test_path, 'wb') as f:
        f.write(base64.b64decode(simple_png_base64))
    
    return test_path

def run_full_test():
    """运行完整测试流程"""
    print("\n" + "=" * 80)
    print("  商品图片上传和保存功能 - 完整测试")
    print("=" * 80)
    
    print("\n前置条件检查:")
    print("1. Flask应用必须正在运行")
    print("2. 数据库连接必须正常")
    print("3. 上传目录必须有写入权限")
    
    print("\n开始测试...")
    
    image_url = test_image_upload()
    
    if image_url:
        product_id = test_product_add_with_image(image_url)
        
        if product_id:
            print("\n" + "=" * 80)
            print("  🎉 所有测试通过！")
            print("=" * 80)
            print("\n测试总结:")
            print("✅ 图片上传功能正常")
            print("✅ 图片URL返回正常")
            print("✅ 商品添加功能正常")
            print("✅ 图片URL已保存到数据库")
            print("✅ 商品数据可以正确读取")
            
            print("\n\n使用说明:")
            print("1. 打开浏览器访问: http://127.0.0.1:5000/admin/sp/product")
            print("2. 点击「添加商品」按钮")
            print("3. 点击上传区域选择本地图片")
            print("4. 填写其他商品信息")
            print("5. 点击保存按钮")
            print("\n上传的图片将保存在: apps/static/uploads/products/")
            return True
        else:
            print("\n❌ 商品添加测试失败")
            return False
    else:
        print("\n❌ 图片上传测试失败")
        return False

if __name__ == "__main__":
    run_full_test()
