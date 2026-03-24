# -*- encoding: utf-8 -*-
"""
添加商品测试数据到数据库
"""

import pymysql

# 数据库配置
DB_CONFIG = {
    'host': '101.126.90.255',
    'port': 63306,
    'user': 'root',
    'password': 'Gesoft9919.',
    'database': 'liandong21mall',
    'charset': 'utf8mb4'
}

def add_test_products():
    """添加商品测试数据"""
    
    connection = pymysql.connect(**DB_CONFIG)
    
    try:
        with connection.cursor() as cursor:
            # 检查是否已有商品数据
            cursor.execute("SELECT COUNT(*) FROM sp_product")
            count = cursor.fetchone()[0]
            
            if count > 0:
                print('已有商品数据，跳过插入')
                return
            
            print('开始插入商品测试数据...')
            
            # 插入商品数据
            products = [
                (1, 1, '焕颜修护精华液', 'P001', 'https://images.unsplash.com/photo-1522335789203-aabd016d8d3?w=400&h=400&fit=crop', 299.00, 399.00, 259.00, 1000, 5280, '焕颜修护，深层滋养肌肤', 1, 1, 1, 10),
                (2, 1, '深层清洁洁面乳', 'P002', 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop', 158.00, 198.00, 138.00, 2000, 8560, '温和深层清洁，洁面不紧绷', 1, 1, 0, 9),
                (3, 1, '保湿修护面霜', 'P003', 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=400&h=400&fit=crop', 358.00, 458.00, 318.00, 800, 3250, '保湿修护，深层滋养肌肤', 1, 1, 1, 8),
                (4, 1, '舒缓修护精华水', 'P004', 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc8?w=400&h=400&fit=crop', 228.00, 298.00, 198.00, 1500, 4120, '舒缓修护，肌肤水润光滑', 0, 1, 1, 7),
                (5, 1, '紧致抗皱眼霜', 'P005', 'https://images.unsplash.com/photo-1570194065650-d99fb4b38b15?w=400&h=400&fit=crop', 268.00, 368.00, 238.00, 600, 2150, '紧致抗皱，淡化黑眼圈', 1, 0, 1, 6),
                (6, 1, '氨基酸温和洁面泡沫', 'P006', 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop', 128.00, 168.00, 108.00, 3000, 9850, '氨基酸温和配方，敏感肌适用', 1, 1, 1, 5),
                (7, 1, '烟酰胺美白精华', 'P007', 'https://images.unsplash.com/photo-1615397349754-cfa2066a298e?w=400&h=400&fit=crop', 388.00, 488.00, 358.00, 500, 1580, '烟酰胺美白，淡化色斑', 0, 0, 1, 4),
                (8, 1, '玻尿酸补水喷雾', 'P008', 'https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=400&h=400&fit=crop', 88.00, 128.00, 68.00, 5000, 15600, '随时补水，一喷锁水', 1, 1, 1, 3),
                (9, 2, '水润唇釉', 'P009', 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400&h=400&fit=crop', 129.00, 169.00, 99.00, 2000, 6850, '水润不干，持久显色', 1, 1, 0, 2),
                (10, 2, '气垫BB霜', 'P010', 'https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=400&h=400&fit=crop', 268.00, 358.00, 238.00, 1200, 4250, '轻薄遮瑕，自然服帖', 1, 1, 0, 1)
            ]
            
            for product in products:
                (product_id, category_id, name, code, image, price, original_price, member_price, stock, sales, brief, is_hot, is_new, is_recommend, sort) = product
                
                cursor.execute("""
                    INSERT INTO sp_product 
                    (id, category_id, product_name, product_code, main_image, price, original_price, member_price, stock, sales, brief, is_hot, is_new, is_recommend, sort)
                    VALUES (%s, %s, '%s', '%s', '%s', %s, %s, %s, %s, %s, '%s', %s, %s, %s, %s)
                """ % product)
            
            connection.commit()
            print('✓ 商品数据插入成功！')
            
    except Exception as e:
        print(f'✗ 插入商品数据失败: {e}')
        connection.rollback()
    finally:
        connection.close()

if __name__ == '__main__':
    add_test_products()
