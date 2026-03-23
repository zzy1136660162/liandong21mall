import pymysql
import random
import json
from datetime import datetime

connection = pymysql.connect(
    host='101.126.90.255',
    port=63306,
    user='root',
    password='Gesoft9919.',
    database='liandong21mall',
    charset='utf8mb4'
)

cursor = connection.cursor()

print('开始添加测试数据...\n')

categories = [
    (1, 'skincare'),
    (2, 'makeup'),
    (3, 'personal_care'),
    (4, 'food'),
    (5, 'home')
]

products_data = [
    (1, '雅诗兰黛小棕瓶精华', 'ESTEE-LAUDER-001', 'https://via.placeholder.com/400x400/FFE4B5/000000?text=小棕瓶', 680.00, 890.00, 650.00, 100, 520, '经典抗老精华，改善细纹', '雅诗兰黛明星产品，修护肌肤，淡化细纹，提升肌肤弹性。'),
    (1, '兰蔻小黑瓶精华', 'LANCOME-001', 'https://via.placeholder.com/400x400/FFE4B5/000000?text=小黑瓶', 760.00, 980.00, 720.00, 80, 480, '肌底修护精华', '兰蔻明星产品，修护肌底，提升肌肤吸收力。'),
    (1, 'SK-II神仙水', 'SK-II-001', 'https://via.placeholder.com/400x400/FFE4B5/000000?text=神仙水', 1540.00, 1790.00, 1460.00, 60, 320, '护肤精华露', 'SK-II经典产品，改善肌肤质地，提升光泽。'),
    (1, '资生堂红腰子精华', 'SHISEIDO-001', 'https://via.placeholder.com/400x400/FFE4B5/000000?text=红腰子', 890.00, 1080.00, 840.00, 90, 280, '红腰子肌底精华', '资生堂明星产品，修护肌底，提升肌肤免疫力。'),
    (2, '迪奥999口红', 'DIOR-001', 'https://via.placeholder.com/400x400/FFB6C1/000000?text=999', 380.00, 450.00, 360.00, 200, 890, '经典正红色', '迪奥经典999，正红色，显白必备。'),
    (2, '香奈儿丝绒口红', 'CHANEL-001', 'https://via.placeholder.com/400x400/FFB6C1/000000?text=香奈儿', 420.00, 500.00, 400.00, 150, 650, '丝绒质地', '香奈儿经典口红，丝绒质地，持久显色。'),
    (2, 'MAC子弹头口红', 'MAC-001', 'https://via.placeholder.com/400x400/FFB6C1/000000?text=MAC', 170.00, 220.00, 160.00, 300, 1200, '经典色号', 'MAC经典子弹头，多色可选，性价比高。'),
    (2, 'YSL圆管口红', 'YSL-001', 'https://via.placeholder.com/400x400/FFB6C1/000000?text=YSL', 320.00, 380.00, 300.00, 180, 750, '滋润配方', 'YSL圆管口红，滋润配方，显色持久。'),
    (3, '欧舒丹护手霜', 'LOCCITANE-001', 'https://via.placeholder.com/400x400/E6E6FA/000000?text=护手霜', 80.00, 120.00, 75.00, 500, 2100, '经典护手霜', '欧舒丹经典护手霜，滋润不油腻。'),
    (3, '资生堂洗面奶', 'SHISEIDO-002', 'https://via.placeholder.com/400x400/E6E6FA/000000?text=洗面奶', 120.00, 160.00, 110.00, 400, 1800, '温和清洁', '资生堂洗面奶，温和清洁，不紧绷。'),
    (3, '舒肤佳沐浴露', 'SAFEGUARD-001', 'https://via.placeholder.com/400x400/E6E6FA/000000?text=沐浴露', 25.00, 35.00, 22.00, 800, 3500, '经典沐浴露', '舒肤佳经典沐浴露，清洁杀菌。'),
    (3, '多芬身体乳', 'DOVE-001', 'https://via.placeholder.com/400x400/E6E6FA/000000?text=身体乳', 45.00, 65.00, 40.00, 600, 2800, '滋润身体乳', '多芬身体乳，滋润保湿，持久留香。'),
    (4, '三只松鼠坚果', 'THREE-SQUIRRELS-001', 'https://via.placeholder.com/400x400/FFFACD/000000?text=坚果', 68.00, 88.00, 62.00, 1000, 4500, '混合坚果', '三只松鼠混合坚果，营养丰富。'),
    (4, '良品铺子零食', 'BESTORE-001', 'https://via.placeholder.com/400x400/FFFACD/000000?text=零食', 55.00, 75.00, 50.00, 1200, 5200, '零食礼包', '良品铺子零食礼包，多种口味。'),
    (4, '百草味肉脯', 'BAICAOWEI-001', 'https://via.placeholder.com/400x400/FFFACD/000000?text=肉脯', 45.00, 60.00, 42.00, 900, 3800, '猪肉脯', '百草味猪肉脯，香辣可口。'),
    (4, '旺旺雪饼', 'WANGWANG-001', 'https://via.placeholder.com/400x400/FFFACD/000000?text=雪饼', 15.00, 22.00, 14.00, 2000, 8900, '经典雪饼', '旺旺雪饼，酥脆香甜。'),
    (5, '宜家收纳盒', 'IKEA-001', 'https://via.placeholder.com/400x400/F5F5DC/000000?text=收纳盒', 35.00, 50.00, 32.00, 500, 2200, '透明收纳盒', '宜家透明收纳盒，实用美观。'),
    (5, '无印良品毛巾', 'MUJI-001', 'https://via.placeholder.com/400x400/F5F5DC/000000?text=毛巾', 28.00, 40.00, 26.00, 800, 3500, '纯棉毛巾', '无印良品纯棉毛巾，柔软舒适。'),
    (5, '小米台灯', 'XIAOMI-001', 'https://via.placeholder.com/400x400/F5F5DC/000000?text=台灯', 169.00, 199.00, 159.00, 300, 1200, '智能台灯', '小米智能台灯，护眼节能。'),
    (5, '飞利浦电动牙刷', 'PHILIPS-001', 'https://via.placeholder.com/400x400/F5F5DC/000000?text=电动牙刷', 299.00, 399.00, 279.00, 200, 800, '声波震动', '飞利浦电动牙刷，声波震动，清洁彻底。'),
]

print('1. 添加商品数据...')
for product in products_data:
    sql = """
    INSERT INTO product (category_id, product_name, product_code, main_image, price, original_price, member_price, stock, sales, brief, description, status, is_hot, is_new, is_recommend, sort)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, %s, %s, %s, %s)
    """
    is_hot = 1 if random.random() > 0.7 else 0
    is_new = 1 if random.random() > 0.6 else 0
    is_recommend = 1 if random.random() > 0.5 else 0
    sort = random.randint(1, 100)
    
    cursor.execute(sql, (*product, is_hot, is_new, is_recommend, sort))
    print(f'  ✓ 添加商品: {product[1]}')

print('\n2. 添加商品SKU数据...')
cursor.execute("SELECT id, product_name, price FROM product")
products = cursor.fetchall()

for product in products:
    product_id, product_name, price = product
    price_float = float(price)
    
    for i in range(1, 4):
        sku_name = f'规格{i}'
        sku_code = f'{product_name}-SKU{i}'
        sku_price = price_float * (1 - (i - 1) * 0.05)
        stock = random.randint(50, 200)
        
        sql = """
        INSERT INTO product_sku (product_id, sku_code, sku_name, spec, price, original_price, member_price, stock, image, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
        """
        spec = json.dumps({'size': f'规格{i}', 'weight': f'{100 + i * 50}g'})
        
        cursor.execute(sql, (
            product_id,
            sku_code,
            sku_name,
            str(spec),
            sku_price,
            sku_price * 1.1,
            sku_price * 0.95,
            stock,
            f'https://via.placeholder.com/400x400/FFE4B5/000000?text=SKU{i}'
        ))
    
    print(f'  ✓ 添加SKU: {product_name} (3个规格)')

connection.commit()
cursor.close()
connection.close()

print('\n✅ 测试数据添加完成！')
print(f'   - 商品数量: {len(products_data)}')
print(f'   - SKU数量: {len(products_data) * 3}')
