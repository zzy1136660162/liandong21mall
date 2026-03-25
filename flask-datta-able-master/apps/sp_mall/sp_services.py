# -*- encoding: utf-8 -*-
"""
商品商城模块 - 业务逻辑层 (sp_前缀)
成员1负责：商品、购物车、订单、地址
"""

from apps import db
from apps.sp_mall.sp_models import (
    SpProductCategory, SpProduct, SpProductSku, 
    SpCart, SpOrder, SpOrderItem, SpAddress
)
from datetime import datetime, timedelta
import random
import string


class SpProductService:
    """商品服务"""
    
    @staticmethod
    def get_categories():
        """获取所有商品分类"""
        categories = SpProductCategory.query.filter_by(status=1).order_by(SpProductCategory.sort).all()
        return [category.to_dict() for category in categories]
    
    @staticmethod
    def get_category_by_id(category_id):
        """根据ID获取分类"""
        category = SpProductCategory.query.get(category_id)
        return category.to_dict() if category else None
    
    @staticmethod
    def get_products(category_id=None, page=1, page_size=10, keyword=None):
        """获取商品列表"""
        query = SpProduct.query.filter_by(status=1)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if keyword:
            query = query.filter(SpProduct.product_name.like(f'%{keyword}%'))
        
        pagination = query.order_by(SpProduct.sort.desc(), SpProduct.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        return {
            'list': [product.to_dict() for product in pagination.items],
            'total': pagination.total,
            'page': page,
            'pageSize': page_size,
            'totalPages': (pagination.total + page_size - 1) // page_size
        }
    
    @staticmethod
    def get_product_by_id(product_id):
        """根据ID获取商品详情"""
        product = SpProduct.query.get(product_id)
        if not product or product.status != 1:
            return None
        
        product_dict = product.to_dict(include_detail=True)
        
        product_dict['id'] = product_dict['productId']
        product_dict['name'] = product_dict['productName']
        product_dict['title'] = product_dict['productName']
        
        product_dict['subtitle'] = product_dict.get('brief', '')
        
        original_price = float(product.original_price) if product.original_price else 0
        current_price = float(product.price)
        if original_price > 0:
            discount = round(current_price / original_price * 10, 1)
        else:
            discount = 10.0
        product_dict['discount'] = str(discount)
        
        product_dict['memberPrice'] = float(product.member_price) if product.member_price else round(current_price * 0.9, 2)
        product_dict['saveAmount'] = round(original_price - current_price, 2) if original_price > 0 else 0
        
        product_dict['stock'] = product.stock if product.stock else 0
        product_dict['sales'] = product.sales if product.sales else 0
        
        product_dict['reviews'] = 0
        
        tags = []
        if product.is_hot:
            tags.append('热销')
        if product.is_new:
            tags.append('新品')
        product_dict['tags'] = tags
        
        specs_list = []
        if product.skus and product.skus.count() > 0:
            spec_keys = set()
            for sku in product.skus.all():
                if hasattr(sku, 'spec') and sku.spec:
                    for key in sku.spec.keys():
                        spec_keys.add(key)
            
            for key in spec_keys:
                spec_values = set()
                for sku in product.skus.all():
                    if hasattr(sku, 'spec') and sku.spec and key in sku.spec:
                        spec_values.add(sku.spec[key])
                
                if spec_values:
                    specs_list.append({
                        'name': key,
                        'values': list(spec_values)
                    })
        
        if not specs_list:
            specs_list = [
                {
                    'name': '规格',
                    'values': ['默认']
                }
            ]
        
        product_dict['specs'] = specs_list
        
        product_dict['shopName'] = '立白Liby旗舰店'
        product_dict['shopLogo'] = 'https://picsum.photos/80/80?random=10'
        product_dict['shopSales'] = '6860'
        product_dict['shopScore'] = '4.84'
        product_dict['productScore'] = '4.96'
        product_dict['logisticsScore'] = '4.74'
        product_dict['serviceScore'] = '4.79'
        
        product_dict['darenCount'] = '4'
        product_dict['location'] = '贵州省黔南布依族苗族自治州'
        
        product_dict['monthSales'] = str(product.sales if product.sales else 0)
        product_dict['monthViews'] = '3166'
        product_dict['monthDaren'] = '1万'
        
        product_dict['reviewCount'] = '0'
        product_dict['goodRate'] = '98'
        product_dict['reviewTags'] = ['有图/视频', '很好用', '味道好', '香味很香']
        
        product_dict['tuanzhangName'] = '飞鸽传媒团长精选'
        product_dict['tuanzhangAvatar'] = 'https://picsum.photos/80/80?random=20'
        product_dict['tuanzhangDesc'] = '聊高佣·帮申样·响应快'
        
        product_dict['reviewList'] = []
        
        recommendations = SpProductService.get_recommend_products(6)
        product_dict['recommendations'] = recommendations
        
        return product_dict
    
    @staticmethod
    def get_hot_products(limit=10):
        """获取热销商品"""
        products = SpProduct.query.filter_by(status=1, is_hot=1).order_by(SpProduct.sales.desc()).limit(limit).all()
        return [product.to_dict() for product in products]
    
    @staticmethod
    def get_new_products(limit=10):
        """获取新品商品"""
        products = SpProduct.query.filter_by(status=1, is_new=1).order_by(SpProduct.created_at.desc()).limit(limit).all()
        return [product.to_dict() for product in products]
    
    @staticmethod
    def get_recommend_products(limit=10):
        """获取推荐商品"""
        products = SpProduct.query.filter_by(status=1, is_recommend=1).order_by(SpProduct.sort.desc()).limit(limit).all()
        result = []
        for product in products:
            result.append({
                'id': product.id,
                'name': product.product_name,
                'image': product.main_image,
                'price': float(product.price)
            })
        return result
    
    @staticmethod
    def search_products(keyword, page=1, page_size=10):
        """搜索商品"""
        query = SpProduct.query.filter(
            SpProduct.status == 1,
            SpProduct.product_name.like(f'%{keyword}%')
        )
        
        pagination = query.order_by(SpProduct.sort.desc(), SpProduct.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        return {
            'list': [product.to_dict() for product in pagination.items],
            'total': pagination.total,
            'page': page,
            'pageSize': page_size,
            'totalPages': (pagination.total + page_size - 1) // page_size
        }


class SpCartService:
    """购物车服务"""
    
    @staticmethod
    def get_cart_list(user_id):
        """获取用户购物车列表"""
        cart_items = SpCart.query.filter_by(user_id=user_id).all()
        result = []
        for item in cart_items:
            product = SpProduct.query.get(item.product_id)
            if product and product.status == 1:
                sku = SpProductSku.query.get(item.sku_id) if item.sku_id else None
                price = float(sku.price) if sku else float(product.price)
                result.append({
                    'cartId': item.id,
                    'productId': product.id,
                    'productName': product.product_name,
                    'mainImage': product.main_image,
                    'specs': sku.sku_name if sku else None,
                    'price': price,
                    'quantity': item.quantity,
                    'selected': item.selected == 1
                })
        return result
    
    @staticmethod
    def add_to_cart(user_id, product_id, sku_id=None, quantity=1):
        """添加商品到购物车"""
        cart = SpCart.query.filter_by(user_id=user_id, product_id=product_id, sku_id=sku_id).first()
        
        if cart:
            cart.quantity += quantity
            cart.updated_at = datetime.now()
        else:
            cart = SpCart(
                user_id=user_id,
                product_id=product_id,
                sku_id=sku_id,
                quantity=quantity,
                selected=1
            )
            db.session.add(cart)
        
        db.session.commit()
        return cart.to_dict()
    
    @staticmethod
    def update_cart_quantity(cart_id, user_id, quantity):
        """更新购物车商品数量"""
        cart = SpCart.query.filter_by(id=cart_id, user_id=user_id).first()
        
        if not cart:
            return None
        
        if quantity <= 0:
            db.session.delete(cart)
        else:
            cart.quantity = quantity
            cart.updated_at = datetime.now()
        
        db.session.commit()
        return cart.to_dict() if quantity > 0 else None
    
    @staticmethod
    def update_cart_selected(cart_id, user_id, selected):
        """更新购物车商品选中状态"""
        cart = SpCart.query.filter_by(id=cart_id, user_id=user_id).first()
        
        if not cart:
            return None
        
        cart.selected = 1 if selected else 0
        cart.updated_at = datetime.now()
        db.session.commit()
        
        return cart.to_dict()
    
    @staticmethod
    def delete_cart_item(cart_id, user_id):
        """删除购物车商品"""
        cart = SpCart.query.filter_by(id=cart_id, user_id=user_id).first()
        
        if not cart:
            return False
        
        db.session.delete(cart)
        db.session.commit()
        return True
    
    @staticmethod
    def clear_cart(user_id):
        """清空购物车"""
        SpCart.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return True
    
    @staticmethod
    def get_cart_total(user_id):
        """获取购物车选中商品总金额"""
        cart_items = SpCart.query.filter_by(user_id=user_id, selected=1).all()
        total = 0.0
        
        for item in cart_items:
            product = SpProduct.query.get(item.product_id)
            if product:
                sku = SpProductSku.query.get(item.sku_id) if item.sku_id else None
                price = float(sku.price) if sku else float(product.price)
                total += price * item.quantity
        
        return total


class SpOrderService:
    """订单服务"""
    
    @staticmethod
    def _generate_order_no():
        """生成订单编号"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.digits, k=6))
        return f'ORD{timestamp}{random_str}'
    
    @staticmethod
    def create_order(user_id, order_data):
        """创建订单"""
        items = order_data.get('items', [])
        address = order_data.get('address', {})
        remark = order_data.get('remark', '')
        
        if not items:
            return None, '请选择商品'
        
        if not address or not address.get('name'):
            return None, '请选择收货地址'
        
        total_amount = 0.0
        order_items_data = []
        
        for item in items:
            product = SpProduct.query.get(item['productId'])
            if not product or product.status != 1:
                continue
            
            sku = SpProductSku.query.get(item['skuId']) if item.get('skuId') else None
            price = float(sku.price) if sku else float(product.price)
            quantity = item.get('quantity', 1)
            item_total = price * quantity
            total_amount += item_total
            
            order_items_data.append({
                'product_id': product.id,
                'sku_id': item.get('skuId'),
                'product_name': product.product_name,
                'sku_name': sku.sku_name if sku else None,
                'product_image': product.main_image,
                'price': price,
                'member_price': float(sku.member_price) if sku and sku.member_price else float(product.member_price) if product.member_price else None,
                'quantity': quantity,
                'total_amount': item_total
            })
        
        if not order_items_data:
            return None, '购物车中没有有效商品'
        
        freight_amount = 0.0 if total_amount >= 99 else 10.0
        pay_amount = total_amount + freight_amount
        
        order = SpOrder(
            order_no=SpOrderService._generate_order_no(),
            user_id=user_id,
            total_amount=total_amount,
            discount_amount=0.0,
            pay_amount=pay_amount,
            freight_amount=freight_amount,
            receiver_name=address.get('name'),
            receiver_phone=address.get('phone'),
            receiver_province=address.get('province'),
            receiver_city=address.get('city'),
            receiver_district=address.get('district'),
            receiver_address=f"{address.get('province', '')}{address.get('city', '')}{address.get('district', '')}{address.get('detail', '')}",
            status='PENDING_PAY',
            remark=remark
        )
        
        db.session.add(order)
        db.session.flush()
        
        for item_data in order_items_data:
            order_item = SpOrderItem(
                order_id=order.id,
                **item_data
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        return order.to_dict(include_items=True), '下单成功'
    
    @staticmethod
    def get_order_list(user_id, status=None, page=1, page_size=10):
        """获取用户订单列表"""
        query = SpOrder.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        pagination = query.order_by(SpOrder.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        orders = []
        for order in pagination.items:
            order_dict = order.to_dict(include_items=True)
            order_dict['products'] = [{
                'productId': item['productId'],
                'productName': item['productName'],
                'productImage': item['productImage'],
                'price': item['price'],
                'quantity': item['quantity']
            } for item in order_dict.get('items', [])]
            orders.append(order_dict)
        
        return {
            'list': orders,
            'total': pagination.total,
            'page': page,
            'pageSize': page_size,
            'totalPages': (pagination.total + page_size - 1) // page_size
        }
    
    @staticmethod
    def get_order_by_id(order_id, user_id=None):
        """根据ID获取订单详情"""
        query = SpOrder.query.filter_by(id=order_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        order = query.first()
        if order:
            return order.to_dict(include_items=True)
        return None
    
    @staticmethod
    def get_order_by_no(order_no):
        """根据订单编号获取订单详情"""
        order = SpOrder.query.filter_by(order_no=order_no).first()
        if order:
            return order.to_dict(include_items=True)
        return None
    
    @staticmethod
    def cancel_order(order_id, user_id, reason=None):
        """取消订单"""
        order = SpOrder.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return None, '订单不存在'
        
        if order.status != 'PENDING_PAY':
            return None, '只有待支付订单可以取消'
        
        order.status = 'CANCELLED'
        order.cancel_time = datetime.now()
        order.cancel_reason = reason
        order.updated_at = datetime.now()
        
        db.session.commit()
        
        return order.to_dict(include_items=True), '订单已取消'
    
    @staticmethod
    def confirm_receipt(order_id, user_id):
        """确认收货"""
        order = SpOrder.query.filter_by(id=order_id, user_id=user_id).first()
        
        if not order:
            return None, '订单不存在'
        
        if order.status != 'SHIPPED':
            return None, '只有已发货订单可以确认收货'
        
        order.status = 'FINISHED'
        order.finish_time = datetime.now()
        order.updated_at = datetime.now()
        
        db.session.commit()
        
        return order.to_dict(include_items=True), '确认收货成功'
    
    @staticmethod
    def cancel_expired_orders(timeout_minutes=30):
        """取消超时的待支付订单"""
        expired_time = datetime.now() - timedelta(minutes=timeout_minutes)
        
        expired_orders = SpOrder.query.filter(
            SpOrder.status == 'PENDING_PAY',
            SpOrder.created_at < expired_time
        ).all()
        
        cancelled_count = 0
        for order in expired_orders:
            order.status = 'CANCELLED'
            order.cancel_time = datetime.now()
            order.cancel_reason = '支付超时，系统自动取消'
            order.updated_at = datetime.now()
            cancelled_count += 1
        
        if cancelled_count > 0:
            db.session.commit()
        
        return cancelled_count

    @staticmethod
    def get_order_expire_time(order_id):
        """获取订单剩余支付时间（秒）"""
        order = SpOrder.query.get(order_id)
        if not order or order.status != 'PENDING_PAY':
            return 0
        
        timeout_minutes = 30
        expire_time = order.created_at + timedelta(minutes=timeout_minutes)
        remaining_seconds = (expire_time - datetime.now()).total_seconds()
        
        return max(0, int(remaining_seconds))

    @staticmethod
    def update_order_status(order_id, status):
        """更新订单状态（后台使用）"""
        order = SpOrder.query.get(order_id)
        
        if not order:
            return None, '订单不存在'
        
        order.status = status
        order.updated_at = datetime.now()
        
        if status == 'PAID' and not order.pay_time:
            order.pay_time = datetime.now()
        elif status == 'SHIPPED' and not order.ship_time:
            order.ship_time = datetime.now()
        elif status == 'FINISHED' and not order.finish_time:
            order.finish_time = datetime.now()
        
        db.session.commit()
        
        return order.to_dict(include_items=True), '订单状态已更新'


class SpAddressService:
    """地址服务"""
    
    @staticmethod
    def get_address_list(user_id):
        """获取用户地址列表"""
        addresses = SpAddress.query.filter_by(user_id=user_id).order_by(SpAddress.is_default.desc(), SpAddress.updated_at.desc()).all()
        return [address.to_dict() for address in addresses]
    
    @staticmethod
    def get_address_by_id(address_id, user_id=None):
        """根据ID获取地址详情"""
        query = SpAddress.query.filter_by(id=address_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        address = query.first()
        return address.to_dict() if address else None
    
    @staticmethod
    def add_address(user_id, address_data):
        """添加地址"""
        if address_data.get('isDefault'):
            SpAddress.query.filter_by(user_id=user_id, is_default=1).update({'is_default': 0})
        
        address = SpAddress(
            user_id=user_id,
            name=address_data.get('name'),
            phone=address_data.get('phone'),
            province=address_data.get('province'),
            city=address_data.get('city'),
            district=address_data.get('district'),
            detail=address_data.get('detail'),
            postcode=address_data.get('postcode'),
            is_default=1 if address_data.get('isDefault') else 0
        )
        
        db.session.add(address)
        db.session.commit()
        
        return address.to_dict()
    
    @staticmethod
    def update_address(address_id, user_id, address_data):
        """更新地址"""
        address = SpAddress.query.filter_by(id=address_id, user_id=user_id).first()
        
        if not address:
            return None
        
        if address_data.get('isDefault'):
            SpAddress.query.filter_by(user_id=user_id, is_default=1).update({'is_default': 0})
        
        address.name = address_data.get('name', address.name)
        address.phone = address_data.get('phone', address.phone)
        address.province = address_data.get('province', address.province)
        address.city = address_data.get('city', address.city)
        address.district = address_data.get('district', address.district)
        address.detail = address_data.get('detail', address.detail)
        address.postcode = address_data.get('postcode', address.postcode)
        address.is_default = 1 if address_data.get('isDefault') else 0
        address.updated_at = datetime.now()
        
        db.session.commit()
        
        return address.to_dict()
    
    @staticmethod
    def delete_address(address_id, user_id):
        """删除地址"""
        address = SpAddress.query.filter_by(id=address_id, user_id=user_id).first()
        
        if not address:
            return False
        
        db.session.delete(address)
        db.session.commit()
        return True
    
    @staticmethod
    def get_default_address(user_id):
        """获取用户默认地址"""
        address = SpAddress.query.filter_by(user_id=user_id, is_default=1).first()
        return address.to_dict() if address else None
    
    @staticmethod
    def set_default_address(address_id, user_id):
        """设置默认地址"""
        SpAddress.query.filter_by(user_id=user_id, is_default=1).update({'is_default': 0})
        
        address = SpAddress.query.filter_by(id=address_id, user_id=user_id).first()
        if address:
            address.is_default = 1
            address.updated_at = datetime.now()
            db.session.commit()
            return address.to_dict()
        
        return None
