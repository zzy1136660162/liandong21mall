# -*- encoding: utf-8 -*-
"""
为商品表添加测试数据 - 包含详细商品介绍（简化版）
"""

from apps import create_app, db
from apps.config import config_dict
from apps.sp_mall.sp_models import SpProduct, SpProductSku, SpProductCategory

app = create_app(config_dict['Debug'])

def create_test_products():
    """创建测试商品数据"""
    
    with app.app_context():
        print("=" * 60)
        print("开始添加测试商品数据")
        print("=" * 60)
        
        # 获取分类
        categories = SpProductCategory.query.all()
        if not categories:
            print("✗ 没有找到商品分类，请先初始化分类数据")
            return
        
        category_map = {cat.category_code: cat for cat in categories}
        
        # 测试商品数据（只包含现有字段）
        test_products = [
            {
                'category_code': 'skincare',
                'product_name': '焕颜修护精华液',
                'product_code': 'SP001',
                'main_image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&h=800&fit=crop',
                'images': [
                    'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800&h=800&fit=crop'
                ],
                'price': 299.00,
                'original_price': 399.00,
                'member_price': 269.00,
                'stock': 100,
                'sales': 528,
                'brief': '深层修护，焕发肌肤光彩，精华液中的修护专家',
                'description': '''
<div class="product-detail">
    <h2>产品介绍</h2>
    <p>焕颜修护精华液是一款专为现代都市女性研发的高端护肤产品，采用独家专利配方，深层渗透肌肤，从根源修护受损细胞，让肌肤重现年轻光彩。</p>
    
    <h3>核心成分</h3>
    <ul>
        <li><strong>玻尿酸</strong>：深层补水，锁住水分，让肌肤水润饱满</li>
        <li><strong>维生素C</strong>：抗氧化，提亮肤色，淡化色斑</li>
        <li><strong>胶原蛋白</strong>：增加肌肤弹性，减少细纹</li>
        <li><strong>烟酰胺</strong>：控油美白，收缩毛孔</li>
    </ul>
    
    <h3>产品功效</h3>
    <div class="features">
        <div class="feature-item">
            <h4>深层修护</h4>
            <p>渗透肌底，修护受损细胞，重建肌肤屏障</p>
        </div>
        <div class="feature-item">
            <h4>补水保湿</h4>
            <p>24小时长效保湿，让肌肤水润不紧绷</p>
        </div>
        <div class="feature-item">
            <h4>提亮肤色</h4>
            <p>淡化暗沉，均匀肤色，重现光泽</p>
        </div>
        <div class="feature-item">
            <h4>抗衰老</h4>
            <p>促进胶原蛋白生成，延缓肌肤衰老</p>
        </div>
    </div>
    
    <h3>适用人群</h3>
    <p>适合所有肤质，特别是干燥、暗沉、细纹明显的肌肤</p>
    
    <h3>使用方法</h3>
    <ol>
        <li>洁面后，使用爽肤水调理肌肤</li>
        <li>取适量精华液（2-3滴）于掌心</li>
        <li>轻轻按摩至完全吸收</li>
        <li>后续可使用面霜锁住营养</li>
    </ol>
    
    <h3>注意事项</h3>
    <ul>
        <li>请置于阴凉干燥处保存</li>
        <li>避免阳光直射</li>
        <li>如出现过敏现象，请立即停止使用</li>
        <li>请置于儿童接触不到的地方</li>
    </ul>
</div>
                ''',
                'status': 1,
                'is_hot': 1,
                'is_new': 1,
                'is_recommend': 1,
                'sort': 1,
                'skus': [
                    {'sku_name': '30ml装', 'spec': {'规格': '30ml'}, 'price': 299.00, 'stock': 50},
                    {'sku_name': '50ml装', 'spec': {'规格': '50ml'}, 'price': 459.00, 'stock': 30},
                    {'sku_name': '100ml装', 'spec': {'规格': '100ml'}, 'price': 799.00, 'stock': 20}
                ]
            },
            {
                'category_code': 'skincare',
                'product_name': '水感透白面霜',
                'product_code': 'SP002',
                'main_image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800&h=800&fit=crop',
                'images': [
                    'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&h=800&fit=crop'
                ],
                'price': 199.00,
                'original_price': 299.00,
                'member_price': 179.00,
                'stock': 80,
                'sales': 892,
                'brief': '水润透白，告别暗沉，拥有水光肌',
                'description': '''
<div class="product-detail">
    <h2>产品介绍</h2>
    <p>水感透白面霜采用先进的水感科技，质地轻盈如水，快速渗透肌肤，有效提亮肤色，让肌肤重现水润透亮的光泽。</p>
    
    <h3>核心成分</h3>
    <ul>
        <li><strong>熊果苷</strong>：天然美白成分，安全有效淡化色斑</li>
        <li><strong>透明质酸</strong>：超强补水，形成保湿膜</li>
        <li><strong>维生素E</strong>：抗氧化，延缓衰老</li>
        <li><strong>植物萃取精华</strong>：温和不刺激，适合敏感肌</li>
    </ul>
    
    <h3>产品功效</h3>
    <div class="features">
        <div class="feature-item">
            <h4>美白淡斑</h4>
            <p>抑制黑色素生成，淡化已有色斑</p>
        </div>
        <div class="feature-item">
            <h4>水润保湿</h4>
            <p>24小时持续补水，肌肤水润不油腻</p>
        </div>
        <div class="feature-item">
            <h4>细腻肌肤</h4>
            <p>改善粗糙，让肌肤细腻光滑</p>
        </div>
        <div class="feature-item">
            <h4>温和安全</h4>
            <p>无刺激配方，敏感肌也能使用</p>
        </div>
    </div>
    
    <h3>适用人群</h3>
    <p>适合所有肤质，特别是暗沉、有斑点、干燥的肌肤</p>
    
    <h3>使用方法</h3>
    <ol>
        <li>洁面后，使用爽肤水调理肌肤</li>
        <li>取适量面霜于掌心</li>
        <li>由内向外、由下向上轻轻按摩</li>
        <li>直至完全吸收即可</li>
    </ol>
</div>
                ''',
                'status': 1,
                'is_hot': 1,
                'is_new': 0,
                'is_recommend': 1,
                'sort': 2,
                'skus': [
                    {'sku_name': '50g装', 'spec': {'规格': '50g'}, 'price': 199.00, 'stock': 40},
                    {'sku_name': '100g装', 'spec': {'规格': '100g'}, 'price': 359.00, 'stock': 25},
                    {'sku_name': '150g装', 'spec': {'规格': '150g'}, 'price': 499.00, 'stock': 15}
                ]
            },
            {
                'category_code': 'makeup',
                'product_name': '丝绒雾面口红',
                'product_code': 'SP003',
                'main_image': 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=800&h=800&fit=crop',
                'images': [
                    'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1596462502278-27bfdd403348?w=800&h=800&fit=crop'
                ],
                'price': 128.00,
                'original_price': 188.00,
                'member_price': 115.00,
                'stock': 150,
                'sales': 1243,
                'brief': '丝绒雾面，持久不脱色，打造完美唇妆',
                'description': '''
<div class="product-detail">
    <h2>产品介绍</h2>
    <p>丝绒雾面口红采用独特的丝绒质地，上唇即化，雾面妆效持久不脱色，让您的双唇时刻保持完美状态。</p>
    
    <h3>产品特点</h3>
    <ul>
        <li><strong>丝绒质地</strong>：轻盈不厚重，舒适无负担</li>
        <li><strong>雾面妆效</strong>：高级哑光，时尚大气</li>
        <li><strong>持久不脱色</strong>：长效持妆，无需频繁补涂</li>
        <li><strong>滋润不干燥</strong>：添加保湿成分，双唇水润不干裂</li>
    </ul>
    
    <h3>色号选择</h3>
    <div class="colors">
        <div class="color-item">
            <h4>#01 烂番茄色</h4>
            <p>显白减龄，适合日常通勤</p>
        </div>
        <div class="color-item">
            <h4>#02 豆沙红</h4>
            <p>温柔气质，适合约会场合</p>
        </div>
        <div class="color-item">
            <h4>#03 正红色</h4>
            <p>经典大气，适合重要场合</p>
        </div>
        <div class="color-item">
            <h4>#04 裸粉色</h4>
            <p>自然裸妆，适合素颜妆效</p>
        </div>
    </div>
    
    <h3>使用方法</h3>
    <ol>
        <li>先用唇部打底产品滋润双唇</li>
        <li>从唇部中央开始，向外涂抹</li>
        <li>可叠加涂抹增加颜色饱和度</li>
        <li>用纸巾轻按，去除多余油脂</li>
    </ol>
</div>
                ''',
                'status': 1,
                'is_hot': 1,
                'is_new': 1,
                'is_recommend': 1,
                'sort': 3,
                'skus': [
                    {'sku_name': '#01 烂番茄色', 'spec': {'色号': '01', '颜色': '烂番茄色'}, 'price': 128.00, 'stock': 50},
                    {'sku_name': '#02 豆沙红', 'spec': {'色号': '02', '颜色': '豆沙红'}, 'price': 128.00, 'stock': 40},
                    {'sku_name': '#03 正红色', 'spec': {'色号': '03', '颜色': '正红色'}, 'price': 128.00, 'stock': 35},
                    {'sku_name': '#04 裸粉色', 'spec': {'色号': '04', '颜色': '裸粉色'}, 'price': 128.00, 'stock': 25}
                ]
            },
            {
                'category_code': 'personal_care',
                'product_name': '深层清洁洁面乳',
                'product_code': 'SP004',
                'main_image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&h=800&fit=crop',
                'images': [
                    'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800&h=800&fit=crop'
                ],
                'price': 89.00,
                'original_price': 129.00,
                'member_price': 79.00,
                'stock': 200,
                'sales': 2341,
                'brief': '深层清洁，温和不刺激，洗出健康肌肤',
                'description': '''
<div class="product-detail">
    <h2>产品介绍</h2>
    <p>深层清洁洁面乳采用温和清洁配方，深入毛孔清除污垢和油脂，同时保持肌肤水润不紧绷，是日常护肤的必备单品。</p>
    
    <h3>核心成分</h3>
    <ul>
        <li><strong>氨基酸表面活性剂</strong>：温和清洁，不刺激肌肤</li>
        <li><strong>植物萃取精华</strong>：舒缓肌肤，减少敏感</li>
        <li><strong>透明质酸</strong>：补水保湿，洗后不紧绷</li>
        <li><strong>维生素E</strong>：抗氧化，保护肌肤</li>
    </ul>
    
    <h3>产品功效</h3>
    <div class="features">
        <div class="feature-item">
            <h4>深层清洁</h4>
            <p>深入毛孔，清除污垢和多余油脂</p>
        </div>
        <div class="feature-item">
            <h4>温和不刺激</h4>
            <p>弱酸性配方，接近肌肤pH值</p>
        </div>
        <div class="feature-item">
            <h4>水润保湿</h4>
            <p>洗后不紧绷，肌肤水润舒适</p>
        </div>
        <div class="feature-item">
            <h4>适合所有肤质</h4>
            <p>敏感肌也能放心使用</p>
        </div>
    </div>
    
    <h3>使用方法</h3>
    <ol>
        <li>先用温水湿润面部</li>
        <li>取适量洁面乳于掌心</li>
        <li>加水揉搓出丰富泡沫</li>
        <li>轻柔按摩面部1-2分钟</li>
        <li>用清水彻底冲洗干净</li>
    </ol>
</div>
                ''',
                'status': 1,
                'is_hot': 1,
                'is_new': 0,
                'is_recommend': 1,
                'sort': 4,
                'skus': [
                    {'sku_name': '100ml装', 'spec': {'规格': '100ml'}, 'price': 89.00, 'stock': 80},
                    {'sku_name': '200ml装', 'spec': {'规格': '200ml'}, 'price': 159.00, 'stock': 60},
                    {'sku_name': '300ml装', 'spec': {'规格': '300ml'}, 'price': 219.00, 'stock': 60}
                ]
            },
            {
                'category_code': 'food',
                'product_name': '有机燕麦片',
                'product_code': 'SP005',
                'main_image': 'https://images.unsplash.com/photo-1517686469429-8bdb88b9f907?w=800&h=800&fit=crop',
                'images': [
                    'https://images.unsplash.com/photo-1517686469429-8bdb88b9f907?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=800&h=800&fit=crop',
                    'https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=800&h=800&fit=crop'
                ],
                'price': 59.00,
                'original_price': 89.00,
                'member_price': 53.00,
                'stock': 300,
                'sales': 3456,
                'brief': '有机燕麦，营养健康，早餐必备',
                'description': '''
<div class="product-detail">
    <h2>产品介绍</h2>
    <p>有机燕麦片精选优质有机燕麦，保留天然营养成分，无添加无防腐剂，是健康早餐的理想选择。</p>
    
    <h3>产品特点</h3>
    <ul>
        <li><strong>有机认证</strong>：通过有机认证，安全无污染</li>
        <li><strong>营养丰富</strong>：富含膳食纤维、蛋白质、维生素</li>
        <li><strong>无添加</strong>：无防腐剂、无色素、无香精</li>
        <li><strong>方便食用</strong>：即食型，开水冲泡即可</li>
    </ul>
    
    <h3>营养价值</h3>
    <div class="nutrition">
        <div class="nutrition-item">
            <h4>膳食纤维</h4>
            <p>促进肠道健康，帮助消化</p>
        </div>
        <div class="nutrition-item">
            <h4>植物蛋白</h4>
            <p>补充蛋白质，增强体质</p>
        </div>
        <div class="nutrition-item">
            <h4>维生素B族</h4>
            <p>维持神经系统正常功能</p>
        </div>
        <div class="nutrition-item">
            <h4>矿物质</h4>
            <p>补充钙、铁、锌等必需矿物质</p>
        </div>
    </div>
    
    <h3>食用方法</h3>
    <ol>
        <li>取适量燕麦片放入碗中</li>
        <li>加入热水或热牛奶</li>
        <li>搅拌2-3分钟至糊状</li>
        <li>可根据个人口味添加蜂蜜、水果等</li>
    </ol>
    
    <h3>适宜人群</h3>
    <p>适合所有人群，特别是注重健康饮食、需要控制体重的人群</p>
</div>
                ''',
                'status': 1,
                'is_hot': 1,
                'is_new': 1,
                'is_recommend': 1,
                'sort': 5,
                'skus': [
                    {'sku_name': '500g装', 'spec': {'规格': '500g'}, 'price': 59.00, 'stock': 100},
                    {'sku_name': '1000g装', 'spec': {'规格': '1000g'}, 'price': 99.00, 'stock': 80},
                    {'sku_name': '2000g装', 'spec': {'规格': '2000g'}, 'price': 179.00, 'stock': 120}
                ]
            }
        ]
        
        # 添加商品数据
        added_count = 0
        for product_data in test_products:
            try:
                # 检查商品是否已存在
                existing_product = SpProduct.query.filter_by(product_code=product_data['product_code']).first()
                if existing_product:
                    print(f"○ 商品已存在: {product_data['product_name']} ({product_data['product_code']})")
                    continue
                
                # 获取分类
                category = category_map.get(product_data['category_code'])
                if not category:
                    print(f"✗ 分类不存在: {product_data['category_code']}")
                    continue
                
                # 提取SKU数据
                skus_data = product_data.pop('skus', [])
                # 移除category_code，使用category_id
                product_data.pop('category_code', None)
                
                # 创建商品
                product = SpProduct(
                    category_id=category.id,
                    **product_data
                )
                db.session.add(product)
                db.session.flush()  # 获取商品ID
                
                # 创建SKU
                for sku_data in skus_data:
                    sku = SpProductSku(
                        product_id=product.id,
                        sku_code=f"{product_data['product_code']}_{sku_data['sku_name']}",
                        **sku_data
                    )
                    db.session.add(sku)
                
                added_count += 1
                print(f"✓ 添加商品: {product_data['product_name']} ({product_data['product_code']})")
                
            except Exception as e:
                print(f"✗ 添加商品失败: {product_data['product_name']} - {e}")
                db.session.rollback()
        
        # 提交所有更改
        try:
            db.session.commit()
            print(f"\n成功添加 {added_count} 个商品")
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ 提交失败: {e}")
        
        print("\n" + "=" * 60)
        print("测试商品数据添加完成！")
        print("=" * 60)

if __name__ == "__main__":
    create_test_products()