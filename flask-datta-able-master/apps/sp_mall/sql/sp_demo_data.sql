-- ========================================
-- 商品商城模块测试数据 (sp_前缀)
-- 成员1负责：商品、购物车、订单、地址
-- ========================================

-- ========================================
-- 1. 商品分类测试数据
-- ========================================
INSERT INTO `sp_product_category` (`id`, `parent_id`, `category_name`, `category_code`, `icon`, `sort`, `status`) VALUES
(1, 0, '护肤', 'skincare', '/static/images/category/skincare.png', 1, 1),
(2, 0, '彩妆', 'makeup', '/static/images/category/makeup.png', 2, 1),
(3, 0, '个护', 'personal_care', '/static/images/category/personal_care.png', 3, 1),
(4, 0, '食品', 'food', '/static/images/category/food.png', 4, 1),
(5, 0, '家居', 'home', '/static/images/category/home.png', 5, 1);

-- ========================================
-- 2. 商品测试数据
-- ========================================
INSERT INTO `sp_product` (`id`, `category_id`, `product_name`, `product_code`, `main_image`, `images`, `price`, `original_price`, `member_price`, `stock`, `sales`, `brief`, `description`, `status`, `is_hot`, `is_new`, `is_recommend`, `sort`) VALUES
(1, 1, '焕颜修护精华液', 'P001', 'https://images.unsplash.com/photo-1522335789203-aabd016d8d3?w=400&h=400&fit=crop', '["https://images.unsplash.com/photo-1522335789203-aabd016d8d3?w=800"]', 299.00, 399.00, 259.00, 1000, 5280, '焕颜修护，深层滋养肌肤', '<p>产品详情介绍...</p>', 1, 1, 1, 1, 10),
(2, 1, '深层清洁洁面乳', 'P002', 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop', '["https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800"]', 158.00, 198.00, 138.00, 2000, 8560, '温和深层清洁，洁面不紧绷', '<p>产品详情介绍...</p>', 1, 1, 0, 1, 9),
(3, 1, '保湿修护面霜', 'P003', 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=400&h=400&fit=crop', '["https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=800"]', 358.00, 458.00, 318.00, 800, 3250, '保湿修护，深层滋养肌肤', '<p>产品详情介绍...</p>', 1, 1, 1, 1, 8),
(4, 1, '舒缓修护精华水', 'P004', 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400&h=400&fit=crop', '["https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800"]', 228.00, 298.00, 198.00, 1500, 4120, '舒缓修护，肌肤水润光滑', '<p>产品详情介绍...</p>', 1, 0, 1, 1, 7),
(5, 1, '紧致抗皱眼霜', 'P005', 'https://images.unsplash.com/photo-1570194065650-d99fb4b38b15?w=400&h=400&fit=crop', '["https://images.unsplash.com/photo-1570194065650-d99fb4b38b15?w=800"]', 268.00, 368.00, 238.00, 600, 2150, '紧致抗皱，淡化黑眼圈', '<p>产品详情介绍...</p>', 1, 1, 0, 1, 6),
(6, 1, '氨基酸温和洁面泡沫', 'P006', 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop', '["https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800"]', 128.00, 168.00, 108.00, 3000, 9850, '氨基酸温和配方，敏感肌适用', '<p>产品详情介绍...</p>', 1, 1, 1, 1, 5),
(7, 1, '烟酰胺美白精华', 'P007', 'https://images.unsplash.com/photo-1615397349754-cfa2066a298e?w=400&h=400&fit=crop', '["https://images.unsplash.com/photo-1615397349754-cfa2066a298e?w=800"]', 388.00, 488.00, 358.00, 500, 1580, '烟酰胺美白，淡化色斑', '<p>产品详情介绍...</p>', 1, 0, 1, 1, 4),
(8, 1, '玻尿酸补水喷雾', 'P008', 'https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=400&h=400&fit=crop', '["https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=800"]', 88.00, 128.00, 68.00, 5000, 15600, '随时补水，一喷锁水', '<p>产品详情介绍...</p>', 1, 1, 1, 1, 3),
(9, 2, '水润唇釉', 'P009', 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400&h=400&fit=crop', '["https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=800"]', 129.00, 169.00, 99.00, 2000, 6850, '水润不干，持久显色', '<p>产品详情介绍...</p>', 1, 1, 1, 1, 2),
(10, 2, '气垫BB霜', 'P010', 'https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=400&h=400&fit=crop', '["https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=800"]', 268.00, 358.00, 238.00, 1200, 4250, '轻薄遮瑕，自然服帖', '<p>产品详情介绍...</p>', 1, 1, 0, 1, 1);

-- ========================================
-- 3. 商品SKU测试数据
-- ========================================
INSERT INTO `sp_product_sku` (`id`, `product_id`, `sku_code`, `sku_name`, `spec`, `price`, `original_price`, `member_price`, `stock`, `image`, `status`) VALUES
(1, 1, 'SKU001-30ML', '焕颜修护精华液 30ml', '{"规格": "30ml"}', 299.00, 399.00, 259.00, 500, 'https://images.unsplash.com/photo-1522335789203-aabd016d8d3?w=400&h=400&fit=crop', 1),
(2, 1, 'SKU001-50ML', '焕颜修护精华液 50ml', '{"规格": "50ml"}', 459.00, 599.00, 399.00, 500, 'https://images.unsplash.com/photo-1522335789203-aabd016d8d3?w=400&h=400&fit=crop', 1),
(3, 2, 'SKU002-100ML', '深层清洁洁面乳 100ml', '{"规格": "100ml"}', 158.00, 198.00, 138.00, 1000, 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop', 1),
(4, 2, 'SKU002-200ML', '深层清洁洁面乳 200ml', '{"规格": "200ml"}', 258.00, 328.00, 228.00, 1000, 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop', 1),
(5, 3, 'SKU003-50G', '保湿修护面霜 50g', '{"规格": "50g"}', 358.00, 458.00, 318.00, 800, 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=400&h=400&fit=crop', 1);

-- ========================================
-- 4. 收货地址测试数据
-- ========================================
INSERT INTO `sp_address` (`id`, `user_id`, `name`, `phone`, `province`, `city`, `district`, `detail`, `postcode`, `is_default`) VALUES
(1, 1, '张三', '13800138000', '北京市', '北京市', '朝阳区', 'xxx街道xxx号xxx小区xxx号楼xxx室', '100000', 1),
(2, 1, '李四', '13900139000', '上海市', '上海市', '浦东新区', 'xxx路xxx号xxx大厦xxx楼xxx室', '200000', 0),
(3, 1, '王五', '13700137000', '广东省', '深圳市', '南山区', 'xxx大道xxx号xxx科技园xxx栋xxx室', '518000', 0);

-- ========================================
-- 5. 购物车测试数据
-- ========================================
INSERT INTO `sp_cart` (`id`, `user_id`, `product_id`, `sku_id`, `quantity`, `selected`) VALUES
(1, 1, 1, 1, 2, 1),
(2, 1, 2, 3, 1, 1),
(3, 1, 3, 5, 1, 0),
(4, 1, 4, NULL, 3, 1),
(5, 1, 5, NULL, 1, 0);

-- ========================================
-- 6. 订单测试数据
-- ========================================
INSERT INTO `sp_order` (`id`, `order_no`, `user_id`, `total_amount`, `discount_amount`, `pay_amount`, `freight_amount`, `receiver_name`, `receiver_phone`, `receiver_province`, `receiver_city`, `receiver_district`, `receiver_address`, `status`, `remark`) VALUES
(1, 'ORD20240320001', 1, 598.00, 0.00, 598.00, 0.00, '张三', '13800138000', '北京市', '北京市', '朝阳区', '北京市北京市朝阳区xxx街道xxx号xxx小区xxx号楼xxx室', 'PENDING_PAY', '请尽快发货'),
(2, 'ORD20240319001', 1, 516.00, 0.00, 516.00, 0.00, '李四', '13900139000', '上海市', '上海市', '浦东新区', '上海市上海市浦东新区xxx路xxx号xxx大厦xxx楼xxx室', 'PAID', NULL),
(3, 'ORD20240318001', 1, 456.00, 0.00, 456.00, 0.00, '张三', '13800138000', '北京市', '北京市', '朝阳区', '北京市北京市朝阳区xxx街道xxx号xxx小区xxx号楼xxx室', 'SHIPPED', NULL),
(4, 'ORD20240315001', 1, 268.00, 0.00, 268.00, 0.00, '王五', '13700137000', '广东省', '深圳市', '南山区', '广东省深圳市南山区xxx大道xxx号xxx科技园xxx栋xxx室', 'FINISHED', NULL);

-- ========================================
-- 7. 订单明细测试数据
-- ========================================
INSERT INTO `sp_order_item` (`id`, `order_id`, `product_id`, `sku_id`, `product_name`, `sku_name`, `product_image`, `price`, `member_price`, `quantity`, `total_amount`) VALUES
(1, 1, 1, 1, '焕颜修护精华液', '焕颜修护精华液 30ml', 'https://images.unsplash.com/photo-1522335789203-aabd016d8d3?w=400&h=400&fit=crop', 299.00, 259.00, 2, 598.00),
(2, 2, 2, 3, '深层清洁洁面乳', '深层清洁洁面乳 100ml', 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop', 158.00, 138.00, 1, 158.00),
(3, 2, 3, 5, '保湿修护面霜', '保湿修护面霜 50g', 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=400&h=400&fit=crop', 358.00, 318.00, 1, 358.00),
(4, 3, 4, NULL, '舒缓修护精华水', NULL, 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400&h=400&fit=crop', 228.00, 198.00, 2, 456.00),
(5, 4, 5, NULL, '紧致抗皱眼霜', NULL, 'https://images.unsplash.com/photo-1570194065650-d99fb4b38b15?w=400&h=400&fit=crop', 268.00, 238.00, 1, 268.00);
