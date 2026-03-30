# -*- encoding: utf-8 -*-
"""
生成商品占位图片
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_images():
    """创建商品占位图片"""
    
    print("=" * 60)
    print("生成商品占位图片")
    print("=" * 60)
    
    # 创建图片目录
    base_dir = os.path.dirname(os.path.dirname(__file__))
    images_dir = os.path.join(base_dir, 'static', 'images', 'products')
    
    if not os.path.exists(images_dir):
        os.makedirs(images_dir, exist_ok=True)
        print(f"✓ 创建图片目录: {images_dir}")
    
    # 商品信息
    products = [
        {'id': 1, 'name': '焕颜修护精华液', 'code': 'P001', 'color': '#FFB6C1'},
        {'id': 2, 'name': '深层清洁洁面乳', 'code': 'P002', 'color': '#87CEEB'},
        {'id': 3, 'name': '保湿修护面霜', 'code': 'P003', 'color': '#98FB98'},
        {'id': 4, 'name': '舒缓修护精华水', 'code': 'P004', 'color': '#DDA0DD'},
        {'id': 5, 'name': '紧致抗皱眼霜', 'code': 'P005', 'color': '#F0E68C'},
        {'id': 6, 'name': '氨基酸温和洁面泡沫', 'code': 'P006', 'color': '#FFD700'},
        {'id': 7, 'name': '烟酰胺美白精华', 'code': 'P007', 'color': '#FF69B4'},
        {'id': 8, 'name': '玻尿酸补水喷雾', 'code': 'P008', 'color': '#00CED1'},
        {'id': 9, 'name': '水润唇釉', 'code': 'P009', 'color': '#FF6347'},
        {'id': 10, 'name': '气垫BB霜', 'code': 'P010', 'color': '#40E0D0'},
        {'id': 11, 'name': '焕颜修护精华液', 'code': 'SP001', 'color': '#FFB6C1'},
        {'id': 12, 'name': '水感透白面霜', 'code': 'SP002', 'color': '#E6E6FA'},
        {'id': 13, 'name': '丝绒雾面口红', 'code': 'SP003', 'color': '#DC143C'},
        {'id': 14, 'name': '深层清洁洁面乳', 'code': 'SP004', 'color': '#87CEEB'},
        {'id': 15, 'name': '有机燕麦片', 'code': 'SP005', 'color': '#DEB887'}
    ]
    
    created_count = 0
    
    for product in products:
        try:
            # 创建主图 (800x800)
            main_img = Image.new('RGB', (800, 800), color=product['color'])
            draw = ImageDraw.Draw(main_img)
            
            # 添加商品名称
            try:
                # 尝试使用系统字体
                font_large = ImageFont.truetype("arial.ttf", 40)
                font_small = ImageFont.truetype("arial.ttf", 24)
            except:
                # 如果找不到字体，使用默认字体
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # 计算文本位置（居中）
            text_bbox = draw.textbbox((0, 0), product['name'], font=font_large)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = (800 - text_width) // 2
            y = (800 - text_height) // 2
            
            # 绘制商品名称
            draw.text((x, y - 50), product['name'], fill='black', font=font_large)
            draw.text((x, y + 50), product['code'], fill='black', font=font_small)
            
            # 保存主图
            main_path = os.path.join(images_dir, f"product_{product['id']}_main.jpg")
            main_img.save(main_path, 'JPEG', quality=85)
            created_count += 1
            print(f"✓ 创建主图: product_{product['id']}_main.jpg")
            
            # 创建3张商品图片 (不同颜色变体）
            colors = [
                product['color'],
                adjust_color(product['color'], 20),
                adjust_color(product['color'], -20)
            ]
            
            for i, color in enumerate(colors, 1):
                img = Image.new('RGB', (800, 800), color=color)
                draw = ImageDraw.Draw(img)
                
                # 添加序号
                draw.text((x, y - 50), f"图片 {i}", fill='black', font=font_large)
                draw.text((x, y), product['name'], fill='black', font=font_small)
                
                # 保存商品图片
                img_path = os.path.join(images_dir, f"product_{product['id']}_{i}.jpg")
                img.save(img_path, 'JPEG', quality=85)
                created_count += 1
                print(f"✓ 创建图片: product_{product['id']}_{i}.jpg")
            
        except Exception as e:
            print(f"✗ 创建商品 {product['name']} 图片失败: {e}")
    
    print("\n" + "=" * 60)
    print(f"成功创建 {created_count} 张占位图片")
    print("=" * 60)
    print(f"\n图片保存位置: {images_dir}")
    print("每个商品4张图片（1张主图 + 3张商品图片）")

def adjust_color(hex_color, amount):
    """调整颜色亮度"""
    # 移除#号
    hex_color = hex_color.lstrip('#')
    
    # 转换为RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # 调整亮度
    r = max(0, min(255, r + amount))
    g = max(0, min(255, g + amount))
    b = max(0, min(255, b + amount))
    
    # 转换回hex
    return f'#{r:02x}{g:02x}{b:02x}'

if __name__ == "__main__":
    try:
        create_placeholder_images()
        print("\n✓ 占位图片生成完成！")
        print("注意: 这是临时占位图片，建议替换为实际商品图片")
    except ImportError:
        print("✗ 需要安装Pillow库: pip install Pillow")
    except Exception as e:
        print(f"✗ 生成图片失败: {e}")