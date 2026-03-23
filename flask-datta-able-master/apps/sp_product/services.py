# -*- encoding: utf-8 -*-
"""
商品商城模块 - 业务逻辑层
"""

from apps import db
from apps.product.models import (
    ProductCategory, Product, ProductSku, 
    Cart, Order, OrderItem
)
from datetime import datetime
import random
import string


class ProductService:
    """商品服务"""
    
    @staticmethod
    def get_categories():
        """获取所有商品分类"""
        categories = ProductCategory.query.filter_by(status=1).order_by(ProductCategory.sort).all()
        return [category.to_dict() for category in categories]
    
    @staticmethod
    def get_category_by_id(category_id):
        """根据ID获取分类"""
        category = ProductCategory.query.get(category_id)
        return category.to_dict() if category else None
    
    @staticmethod
    def get_products(category_id=None, page=1, page_size=10, keyword=None):
        """获取商品列表"""
        query = Product.query.filter_by(status=1)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if keyword:
            query = query.filter(Product.product_name.like(f'%{keyword}%'))
        
        pagination = query.order_by(Product.sort.desc(), Product.created_at.desc()).paginate(
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
        product = Product.query.get(product_id)
        if product and product.status == 1:
            return product.to_dict(include_detail=True)
        return None
    
    @staticmethod
    def get_hot_products(limit=10):
        """获取热销商品"""
        products = Product.query.filter_by(status=1, is_hot=1).order_by(Product.sales.desc()).limit(limit).all()
        return [product.to_dict() for product in products]
    
    @staticmethod
    def get_new_products(limit=10):
        """获取新品商品"""
        products = Product.query.filter_by(status=1, is_new=1).order_by(Product.created_at.desc()).limit(limit).all()
        return [product.to_dict() for product in products]
    
    @staticmethod
    def get_recommend_products(limit=10):
        """获取推荐商品"""
        products = Product.query.filter_by(status=1, is_recommend=1).order_by(Product.sort.desc()).limit(limit).all()
        return [product.to_dict() for product in products]
    
    @staticmethod
    def search_products(keyword, page=1, page_size=10):
        """搜索商品"""
        query = Product.query.filter(
            Product.status == 1,
            Product.product_name.like(f'%{keyword}%')
        )
        
        pagination = query.order_by(Product.sort.desc(), Product.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        return {
            'list': [product.to_dict() for product in pagination.items],
            'total': pagination.total,
            'page': page,
            'pageSize': page_size,
            'totalPages': (pagination.total + page_size - 1) // page_size
        }


class CartService:
    """购物车服务"""
    
    @staticmethod
    def get_cart_list(user_id):
        """获取用户购物车列表"""
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        return [item.to_dict() for item in cart_items]
    
    @staticmethod
    def add_to_cart(user_id, product_id, sku_id=None, quantity=1):
        """添加商品到购物车"""
        cart = Cart.query.filter_by(user_id=user_id, product_id=product_id, sku_id=sku_id).first()
        
        if cart:
            cart.quantity += quantity
            cart.updated_at = datetime.now()
        else:
            cart = Cart(
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
        cart = Cart.query.filter_by(id=cart_id, user_id=user_id).first()
        
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
        cart = Cart.query.filter_by(id=cart_id, user_id=user_id).first()
        
        if not cart:
            return None
        
        cart.selected = 1 if selected else 0
        cart.updated_at = datetime.now()
        db.session.commit()
        
        return cart.to_dict()
    
    @staticmethod
    def delete_cart_item(cart_id, user_id):
        """删除购物车商品"""
        cart = Cart.query.filter_by(id=cart_id, user_id=user_id).first()
        
        if not cart:
            return False
        
        db.session.delete(cart)
        db.session.commit()
        return True
    
    @staticmethod
    def clear_cart(user_id):
        """清空购物车"""
        Cart.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return True
    
    @staticmethod
    def get_cart_total(user_id):
        """获取购物车选中商品总金额"""
        cart_items = Cart.query.filter_by(user_id=user_id, selected=1).all()
        total = 0.0
        
        for item in cart_items:
            product = Product.query.get(item.product_id)
            if product:
                sku = ProductSku.query.get(item.sku_id) if item.sku_id else None
                price = sku.price if sku else product.price
                total += float(price) * item.quantity
        
        return total


class OrderService:
    """订单服务"""
    
    @staticmethod
    def _generate_order_no():
        """生成订单编号"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.digits, k=6))
        return f'ORD{timestamp}{random_str}'
    
    @staticmethod
    def submit_order(user_id, cart_items, address_info, remark=None):
        """提交订单"""
        from apps.member.models import UserMember
        
        total_amount = 0.0
        discount_amount = 0.0
        order_items_data = []
        
        for item in cart_items:
            product = Product.query.get(item['productId'])
            if not product or product.status != 1:
                continue
            
            sku = ProductSku.query.get(item['skuId']) if item.get('skuId') else None
            
            price = sku.price if sku else product.price
            member_price = sku.member_price if sku else product.member_price
            
            user_member = UserMember.query.filter_by(user_id=user_id).first()
            if user_member and member_price:
                final_price = member_price
                discount_amount += (float(price) - float(member_price)) * item['quantity']
            else:
                final_price = price
            
            item_total = float(final_price) * item['quantity']
            total_amount += item_total
            
            order_items_data.append({
                'product_id': product.id,
                'sku_id': item.get('skuId'),
                'product_name': product.product_name,
                'sku_name': sku.sku_name if sku else None,
                'product_image': product.main_image,
                'price': price,
                'member_price': member_price,
                'quantity': item['quantity'],
                'total_amount': item_total
            })
        
        if not order_items_data:
            return None, '购物车中没有有效商品'
        
        pay_amount = total_amount
        freight_amount = 0.0
        
        order = Order(
            order_no=OrderService._generate_order_no(),
            user_id=user_id,
            total_amount=total_amount,
            discount_amount=discount_amount,
            pay_amount=pay_amount,
            freight_amount=freight_amount,
            receiver_name=address_info['name'],
            receiver_phone=address_info['phone'],
            receiver_address=address_info['fullAddress'],
            status='PENDING_PAY',
            remark=remark
        )
        
        db.session.add(order)
        db.session.flush()
        
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                **item_data
            )
            db.session.add(order_item)
        
        for item in cart_items:
            Cart.query.filter_by(id=item['cartId']).delete()
        
        db.session.commit()
        
        return order.to_dict(include_items=True), '下单成功'
    
    @staticmethod
    def get_order_list(user_id, status=None, page=1, page_size=10):
        """获取用户订单列表"""
        query = Order.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        pagination = query.order_by(Order.created_at.desc()).paginate(
            page=page, per_page=page_size, error_out=False
        )
        
        return {
            'list': [order.to_dict(include_items=True) for order in pagination.items],
            'total': pagination.total,
            'page': page,
            'pageSize': page_size,
            'totalPages': (pagination.total + page_size - 1) // page_size
        }
    
    @staticmethod
    def get_order_by_id(order_id, user_id):
        """根据ID获取订单详情"""
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if order:
            return order.to_dict(include_items=True)
        return None
    
    @staticmethod
    def get_order_by_no(order_no):
        """根据订单编号获取订单详情"""
        order = Order.query.filter_by(order_no=order_no).first()
        if order:
            return order.to_dict(include_items=True)
        return None
    
    @staticmethod
    def cancel_order(order_id, user_id, reason=None):
        """取消订单"""
        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        
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
    def update_order_status(order_id, status):
        """更新订单状态"""
        order = Order.query.get(order_id)
        
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
