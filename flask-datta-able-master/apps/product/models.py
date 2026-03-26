# -*- encoding: utf-8 -*-
"""
商品商城模块 - 数据模型
"""

from apps import db
from datetime import datetime


class ProductCategory(db.Model):
    """商品分类表"""
    __tablename__ = 'product_category'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='分类ID')
    parent_id = db.Column(db.Integer, nullable=False, default=0, comment='父分类ID')
    category_name = db.Column(db.String(50), nullable=False, comment='分类名称')
    category_code = db.Column(db.String(50), nullable=False, unique=True, comment='分类编码')
    icon = db.Column(db.String(500), nullable=True, comment='分类图标URL')
    sort = db.Column(db.Integer, nullable=False, default=0, comment='排序')
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='状态：1启用 0禁用')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def __repr__(self):
        return f'<ProductCategory {self.category_code}:{self.category_name}>'
    
    def to_dict(self):
        return {
            'categoryId': self.id,
            'categoryName': self.category_name,
            'categoryCode': self.category_code,
            'icon': self.icon,
            'sort': self.sort,
            'status': self.status
        }


class Product(db.Model):
    """商品表"""
    __tablename__ = 'product'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='商品ID')
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False, comment='分类ID')
    product_name = db.Column(db.String(200), nullable=False, comment='商品名称')
    product_code = db.Column(db.String(50), nullable=False, unique=True, comment='商品编码')
    main_image = db.Column(db.String(500), nullable=False, comment='主图URL')
    images = db.Column(db.JSON, nullable=True, comment='商品图片列表JSON')
    price = db.Column(db.Numeric(10, 2), nullable=False, comment='销售价格')
    original_price = db.Column(db.Numeric(10, 2), nullable=True, comment='原价')
    member_price = db.Column(db.Numeric(10, 2), nullable=True, comment='会员价')
    stock = db.Column(db.Integer, nullable=False, default=0, comment='库存数量')
    sales = db.Column(db.Integer, nullable=False, default=0, comment='销量')
    brief = db.Column(db.String(500), nullable=True, comment='商品简介')
    description = db.Column(db.Text, nullable=True, comment='商品详情HTML')
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='状态：1上架 0下架')
    is_hot = db.Column(db.SmallInteger, nullable=False, default=0, comment='是否热销：1是 0否')
    is_new = db.Column(db.SmallInteger, nullable=False, default=0, comment='是否新品：1是 0否')
    is_recommend = db.Column(db.SmallInteger, nullable=False, default=0, comment='是否推荐：1是 0否')
    commission_rate = db.Column(db.Numeric(10, 2), nullable=True, default=15.0, comment='佣金比例(%)')
    commission_amount = db.Column(db.Numeric(10, 2), nullable=True, comment='固定佣金金额')
    normal_rate = db.Column(db.Numeric(10, 2), nullable=True, default=20.0, comment='普通达人佣金比例(%)')
    premium_rate = db.Column(db.Numeric(10, 2), nullable=True, default=25.0, comment='优质达人佣金比例(%)')
    top_rate = db.Column(db.Numeric(10, 2), nullable=True, default=30.0, comment='头部达人佣金比例(%)')
    settlement_type = db.Column(db.SmallInteger, nullable=True, default=1, comment='结算类型：1月结 2周结 3实时')
    sort = db.Column(db.Integer, nullable=False, default=0, comment='排序')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    skus = db.relationship('ProductSku', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Product {self.product_code}:{self.product_name}>'
    
    def to_dict(self, include_detail=False):
        price = float(self.price)
        original_price = float(self.original_price) if self.original_price else None
        commission_rate = 15.0
        commission_amount = round(price * commission_rate / 100, 2)
        tags = []
        if self.is_hot == 1:
            tags.append('热销')
        if self.is_new == 1:
            tags.append('新品')
        if self.is_recommend == 1:
            tags.append('推荐')

        discount = None
        if original_price and original_price > price:
            discount = round((1 - price / original_price) * 10, 1)

        save_amount = None
        if original_price and original_price > price:
            save_amount = round(original_price - price, 2)

        data = {
            'id': self.id,
            'name': self.product_name,
            'subtitle': self.brief or '',
            'image': self.main_image,
            'title': self.product_name,
            'price': price,
            'originalPrice': original_price,
            'discount': discount,
            'saveAmount': save_amount,
            'memberPrice': float(self.member_price) if self.member_price else None,
            'commissionRate': commission_rate,
            'commissionAmount': commission_amount,
            'sales': self.sales,
            'monthlySales': f'月销{self.sales}件' if self.sales else '月销0件',
            'tags': tags,
            'isBrand': False,
            'hasCashback': False,
            'productId': self.id,
            'categoryId': self.category_id,
            'categoryName': self.category.category_name if self.category else '',
            'productName': self.product_name,
            'productCode': self.product_code,
            'mainImage': self.main_image,
            'images': self.images or [],
            'specs': [],
            'stock': self.stock,
            'brief': self.brief,
            'status': self.status,
            'isHot': self.is_hot == 1,
            'isNew': self.is_new == 1,
            'isRecommend': self.is_recommend == 1,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        if include_detail:
            data['description'] = self.description
            data['skus'] = [sku.to_dict() for sku in self.skus.filter_by(status=1).all()]
            data['reviews'] = 0
            data['reviewList'] = []
            data['recommendations'] = []

        return data


class ProductSku(db.Model):
    """商品SKU表"""
    __tablename__ = 'product_sku'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='SKU ID')
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'), nullable=False, comment='商品ID')
    sku_code = db.Column(db.String(50), nullable=False, unique=True, comment='SKU编码')
    sku_name = db.Column(db.String(100), nullable=False, comment='SKU名称')
    spec = db.Column(db.JSON, nullable=True, comment='规格属性JSON')
    price = db.Column(db.Numeric(10, 2), nullable=False, comment='SKU价格')
    original_price = db.Column(db.Numeric(10, 2), nullable=True, comment='SKU原价')
    member_price = db.Column(db.Numeric(10, 2), nullable=True, comment='SKU会员价')
    stock = db.Column(db.Integer, nullable=False, default=0, comment='SKU库存')
    image = db.Column(db.String(500), nullable=True, comment='SKU图片')
    status = db.Column(db.SmallInteger, nullable=False, default=1, comment='状态：1启用 0禁用')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def __repr__(self):
        return f'<ProductSku {self.sku_code}:{self.sku_name}>'
    
    def to_dict(self):
        return {
            'skuId': self.id,
            'productId': self.product_id,
            'skuCode': self.sku_code,
            'skuName': self.sku_name,
            'spec': self.spec or {},
            'price': float(self.price),
            'originalPrice': float(self.original_price) if self.original_price else None,
            'memberPrice': float(self.member_price) if self.member_price else None,
            'stock': self.stock,
            'image': self.image,
            'status': self.status
        }


class Cart(db.Model):
    """购物车表"""
    __tablename__ = 'cart'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='购物车ID')
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False, comment='用户ID')
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'), nullable=False, comment='商品ID')
    sku_id = db.Column(db.BigInteger, db.ForeignKey('product_sku.id'), nullable=True, comment='SKU ID')
    quantity = db.Column(db.Integer, nullable=False, default=1, comment='数量')
    selected = db.Column(db.SmallInteger, nullable=False, default=1, comment='是否选中：1是 0否')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def __repr__(self):
        return f'<Cart {self.user_id}:{self.product_id}>'
    
    def to_dict(self):
        product = Product.query.get(self.product_id)
        sku = ProductSku.query.get(self.sku_id) if self.sku_id else None
        
        return {
            'cartId': self.id,
            'userId': self.user_id,
            'productId': self.product_id,
            'skuId': self.sku_id,
            'quantity': self.quantity,
            'selected': self.selected == 1,
            'product': product.to_dict() if product else None,
            'sku': sku.to_dict() if sku else None
        }


class Order(db.Model):
    """订单表"""
    __tablename__ = 'order'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='订单ID')
    order_no = db.Column(db.String(50), nullable=False, unique=True, comment='订单编号')
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False, comment='用户ID')
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, comment='订单总金额')
    discount_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00, comment='优惠金额')
    pay_amount = db.Column(db.Numeric(10, 2), nullable=False, comment='实付金额')
    freight_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00, comment='运费')
    receiver_name = db.Column(db.String(50), nullable=False, comment='收货人姓名')
    receiver_phone = db.Column(db.String(20), nullable=False, comment='收货人手机号')
    receiver_address = db.Column(db.String(500), nullable=False, comment='收货地址')
    status = db.Column(db.String(20), nullable=False, default='PENDING_PAY', comment='订单状态')
    pay_time = db.Column(db.DateTime, nullable=True, comment='支付时间')
    ship_time = db.Column(db.DateTime, nullable=True, comment='发货时间')
    finish_time = db.Column(db.DateTime, nullable=True, comment='完成时间')
    cancel_time = db.Column(db.DateTime, nullable=True, comment='取消时间')
    cancel_reason = db.Column(db.String(500), nullable=True, comment='取消原因')
    remark = db.Column(db.String(500), nullable=True, comment='订单备注')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_no}:{self.status}>'
    
    @property
    def status_text(self):
        status_map = {
            'PENDING_PAY': '待支付',
            'PAID': '待发货',
            'SHIPPED': '已发货',
            'FINISHED': '已完成',
            'CANCELLED': '已取消'
        }
        return status_map.get(self.status, '未知')
    
    def to_dict(self, include_items=False):
        data = {
            'orderId': self.id,
            'orderNo': self.order_no,
            'userId': self.user_id,
            'totalAmount': float(self.total_amount),
            'discountAmount': float(self.discount_amount),
            'payAmount': float(self.pay_amount),
            'freightAmount': float(self.freight_amount),
            'receiverName': self.receiver_name,
            'receiverPhone': self.receiver_phone,
            'receiverAddress': self.receiver_address,
            'status': self.status,
            'statusText': self.status_text,
            'payTime': self.pay_time.strftime('%Y-%m-%d %H:%M:%S') if self.pay_time else None,
            'shipTime': self.ship_time.strftime('%Y-%m-%d %H:%M:%S') if self.ship_time else None,
            'finishTime': self.finish_time.strftime('%Y-%m-%d %H:%M:%S') if self.finish_time else None,
            'cancelTime': self.cancel_time.strftime('%Y-%m-%d %H:%M:%S') if self.cancel_time else None,
            'cancelReason': self.cancel_reason,
            'remark': self.remark,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if include_items:
            data['items'] = [item.to_dict() for item in self.items.all()]
        
        return data


class OrderItem(db.Model):
    """订单明细表"""
    __tablename__ = 'order_item'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='订单明细ID')
    order_id = db.Column(db.BigInteger, db.ForeignKey('order.id'), nullable=False, comment='订单ID')
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'), nullable=False, comment='商品ID')
    sku_id = db.Column(db.BigInteger, db.ForeignKey('product_sku.id'), nullable=True, comment='SKU ID')
    product_name = db.Column(db.String(200), nullable=False, comment='商品名称')
    sku_name = db.Column(db.String(100), nullable=True, comment='SKU名称')
    product_image = db.Column(db.String(500), nullable=False, comment='商品图片')
    price = db.Column(db.Numeric(10, 2), nullable=False, comment='商品单价')
    member_price = db.Column(db.Numeric(10, 2), nullable=True, comment='会员价')
    quantity = db.Column(db.Integer, nullable=False, comment='购买数量')
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, comment='小计金额')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    
    def __repr__(self):
        return f'<OrderItem {self.order_id}:{self.product_id}>'
    
    def to_dict(self):
        return {
            'itemId': self.id,
            'orderId': self.order_id,
            'productId': self.product_id,
            'skuId': self.sku_id,
            'productName': self.product_name,
            'skuName': self.sku_name,
            'productImage': self.product_image,
            'price': float(self.price),
            'memberPrice': float(self.member_price) if self.member_price else None,
            'quantity': self.quantity,
            'totalAmount': float(self.total_amount)
        }


class ProductFavorite(db.Model):
    """商品收藏表"""
    __tablename__ = 'product_favorite'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='收藏ID')
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False, comment='用户ID')
    product_id = db.Column(db.BigInteger, db.ForeignKey('xp_products.id'), nullable=False, comment='商品ID')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='uk_user_product'),
    )
    
    def __repr__(self):
        return f'<ProductFavorite {self.user_id}:{self.product_id}>'
    
    def to_dict(self):
        return {
            'favoriteId': self.id,
            'userId': self.user_id,
            'productId': self.product_id,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


def init_product_categories():
    """初始化商品分类数据"""
    categories = [
        {
            'parent_id': 0,
            'category_name': '护肤',
            'category_code': 'skincare',
            'icon': '/static/images/category/skincare.png',
            'sort': 1,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '彩妆',
            'category_code': 'makeup',
            'icon': '/static/images/category/makeup.png',
            'sort': 2,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '个护',
            'category_code': 'personal_care',
            'icon': '/static/images/category/personal_care.png',
            'sort': 3,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '食品',
            'category_code': 'food',
            'icon': '/static/images/category/food.png',
            'sort': 4,
            'status': 1
        },
        {
            'parent_id': 0,
            'category_name': '家居',
            'category_code': 'home',
            'icon': '/static/images/category/home.png',
            'sort': 5,
            'status': 1
        }
    ]
    
    for category_data in categories:
        if not ProductCategory.query.filter_by(category_code=category_data['category_code']).first():
            db.session.add(ProductCategory(**category_data))
    db.session.commit()
