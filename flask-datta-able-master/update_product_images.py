import pymysql

conn = pymysql.connect(
    host='101.126.90.255',
    port=63306,
    user='root',
    password='Gesoft9919.',
    database='liandong21mall',
    charset='utf8mb4'
)

cursor = conn.cursor()

# 更新商品图片为可访问的URL
updates = [
    (42, 'https://images.unsplash.com/photo-1522335789203-aabd016d8d3?w=400&h=400&fit=crop'),
    (43, 'https://images.unsplash.com/photo-1571781926291-c479ebd016b?w=400&h=400&fit=crop'),
    (44, 'https://images.unsplash.com/photo-1611930022073-b7a4ba954f2c?w=400&h=400&fit=crop'),
    (45, 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop'),
    (46, 'https://images.unsplash.com/photo-15864957774-801263fa4d7b?w=400&h=400&fit=crop'),
    (47, 'https://images.unsplash.com/photo-1570194045486-4c2472b4f74?w=400&h=400&fit=crop'),
    (48, 'https://images.unsplash.com/photo-1512496014315-7a947e6e9ce?w=400&h=400&fit=crop'),
    (49, 'https://images.unsplash.com/photo-1583241802754-069aa1bf3a4a?w=400&h=400&fit=crop'),
    (50, 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop'),
    (51, 'https://images.unsplash.com/photo-1608248543803-fa77548c5424?w=400&h=400&fit=crop'),
    (52, 'https://images.unsplash.com/photo-1571872235066-0c6848374b0?w=400&h=400&fit=crop'),
    (53, 'https://images.unsplash.com/photo-1583241802754-069aa1bf3a4a?w=400&h=400&fit=crop'),
    (54, 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop'),
    (55, 'https://images.unsplash.com/photo-15864957774-801263fa4d7b?w=400&h=400&fit=crop'),
    (56, 'https://images.unsplash.com/photo-1570194045486-4c2472b4f74?w=400&h=400&fit=crop'),
    (57, 'https://images.unsplash.com/photo-1512496014315-7a947e6e9ce?w=400&h=400&fit=crop'),
    (58, 'https://images.unsplash.com/photo-1611930022073-b7a4ba954f2c?w=400&h=400&fit=crop'),
    (59, 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop'),
    (60, 'https://images.unsplash.com/photo-1608248543803-fa77548c5424?w=400&h=400&fit=crop'),
    (61, 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop'),
]

for product_id, image_url in updates:
    cursor.execute('UPDATE product SET main_image = %s WHERE id = %s', (image_url, product_id))

conn.commit()
print(f'Updated {len(updates)} product images to accessible URLs')

conn.close()
