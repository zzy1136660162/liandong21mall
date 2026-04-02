# -*- encoding: utf-8 -*-
"""
商品选品模块 - 数据模型
"""

from apps import db
from datetime import datetime


class Category(db.Model):
    """商品分类"""
    __tablename__ = 'xp_categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, default=0)
    level = db.Column(db.SmallInteger, default=1)
    icon = db.Column(db.String(500))
    sort = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id,
            'level': self.level,
            'icon': self.icon,
            'sort': self.sort,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

    def to_api_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'icon': self.icon or ''
        }

    def to_api_with_subcategories(self, all_categories):
        sub_cats = [cat for cat in all_categories if cat.parent_id == self.id]
        return {
            'id': str(self.id),
            'name': self.name,
            'icon': self.icon or '',
            'subCategories': [{'id': str(sub.id), 'name': sub.name} for sub in sub_cats]
        }


class Product(db.Model):
    """商品"""
    __tablename__ = 'xp_products'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    product_no = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(500))
    category_id = db.Column(db.Integer, nullable=False)
    main_image = db.Column(db.String(500), nullable=False)
    images = db.Column(db.JSON)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    original_price = db.Column(db.Numeric(10, 2))
    supply_price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    sales = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(20), default='件')
    weight = db.Column(db.Numeric(8, 2))
    description = db.Column(db.Text)
    specifications = db.Column(db.JSON)
    shop_id = db.Column(db.BigInteger, nullable=False)
    is_brand = db.Column(db.SmallInteger, default=0)
    is_cashback = db.Column(db.SmallInteger, default=0)
    is_trust = db.Column(db.SmallInteger, default=0)
    status = db.Column(db.SmallInteger, default=1)
    sort = db.Column(db.Integer, default=0)
    is_hot = db.Column(db.SmallInteger, default=0)
    is_new = db.Column(db.SmallInteger, default=0)
    is_recommend = db.Column(db.SmallInteger, default=0)
    commission_rate = db.Column(db.Numeric(4, 2), default=10.00)
    normal_rate = db.Column(db.Numeric(4, 2), default=10.00)
    premium_rate = db.Column(db.Numeric(4, 2), default=15.00)
    top_rate = db.Column(db.Numeric(4, 2), default=20.00)
    settlement_type = db.Column(db.SmallInteger, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'product_no': self.product_no,
            'name': self.name,
            'subtitle': self.subtitle,
            'category_id': self.category_id,
            'category_name': '',
            'main_image': self.main_image,
            'images': self.images,
            'price': float(self.price) if self.price else 0,
            'original_price': float(self.original_price) if self.original_price else None,
            'supply_price': float(self.supply_price) if self.supply_price else 0,
            'stock': self.stock,
            'sales': self.sales,
            'unit': self.unit,
            'is_brand': self.is_brand,
            'is_cashback': self.is_cashback,
            'is_trust': self.is_trust,
            'status': self.status,
            'sort': self.sort,
            'is_hot': self.is_hot,
            'is_new': self.is_new,
            'is_recommend': self.is_recommend,
            'commission_rate': float(self.commission_rate) if self.commission_rate else 10,
            'normal_rate': float(self.normal_rate) if self.normal_rate else 10,
            'premium_rate': float(self.premium_rate) if self.premium_rate else 15,
            'top_rate': float(self.top_rate) if self.top_rate else 20,
            'settlement_type': self.settlement_type,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

    def to_api_dict(self):
        commission_amount = float(self.price) * float(self.commission_rate) / 100 if self.commission_rate else 0
        tags = []
        if self.is_brand:
            tags.append('品牌')
        if self.is_trust:
            tags.append('信任购')
        if self.is_cashback:
            tags.append('单单返现')
        
        return {
            'id': str(self.id),
            'name': self.name,
            'image': self.main_image,
            'price': float(self.price) if self.price else 0,
            'supplyPrice': float(self.supply_price) if self.supply_price else 0,
            'commissionRate': float(self.commission_rate) if self.commission_rate else 0,
            'commissionAmount': round(commission_amount, 2),
            'sales': self.sales,
            'monthlySales': f'月销{self.sales}件' if self.sales else '月销0件',
            'category': '',
            'tags': tags,
            'isBrand': bool(self.is_brand),
            'hasCashback': bool(self.is_cashback)
        }

    def to_api_detail_dict(self):
        commission_amount = float(self.price) * float(self.commission_rate) / 100 if self.commission_rate else 0
        tags = []
        if self.is_brand:
            tags.append('品牌')
        if self.is_trust:
            tags.append('信任购')
        if self.is_cashback:
            tags.append('单单返现')

        settlement_map = {1: '月结', 2: '周结', 3: '实时'}

        return {
            'id': str(self.id),
            'title': self.name,
            'name': self.name,
            'subtitle': self.subtitle or '',
            'images': self.images if self.images else [self.main_image],
            'price': float(self.price) if self.price else 0,
            'originalPrice': float(self.original_price) if self.original_price else 0,
            'supplyPrice': float(self.supply_price) if self.supply_price else 0,
            'commissionRate': float(self.commission_rate) if self.commission_rate else 0,
            'commissionAmount': round(commission_amount, 2),
            'commissionLevel': {
                'normal': float(self.normal_rate) if self.normal_rate else 10,
                'premium': float(self.premium_rate) if self.premium_rate else 15,
                'top': float(self.top_rate) if self.top_rate else 20
            },
            'sales': self.sales,
            'monthSales': str(self.sales) if self.sales else '0',
            'stock': self.stock if self.stock else 0,
            'positiveRate': '98%',
            'description': self.description or '',
            'specifications': self.specifications if self.specifications else [],
            'specs': self.specifications if self.specifications else [],
            'samplePolicy': {
                'canApply': True,
                'maxCount': 3,
                'description': '每位达人限申请3件'
            },
            'shopName': '立白Liby旗舰店',
            'shopLogo': 'https://picsum.photos/80/80?random=10',
            'shopSales': '6860',
            'shopScore': '4.84',
            'productScore': '4.96',
            'logisticsScore': '4.74',
            'serviceScore': '4.79',
            'darenCount': '4',
            'location': '贵州省黔南布依族苗族自治州',
            'monthViews': '3166',
            'monthDaren': '1万',
            'reviewCount': '0',
            'goodRate': '98',
            'reviewTags': ['有图/视频', '很好用', '味道好', '香味很香'],
            'tuanzhangName': '飞鸽传媒团长精选',
            'tuanzhangAvatar': 'https://picsum.photos/80/80?random=20',
            'tuanzhangDesc': '聊高佣·帮申样·响应快',
            'tags': tags
        }
