-- ========================================
-- 商品商城后台管理模块SQL
-- 用于补充 sp_product_category 和 sp_product 表的测试数据
-- ========================================

-- 插入商品分类
INSERT INTO `sp_product_category` (`parent_id`, `category_name`, `category_code`, `icon`, `sort`, `status`) VALUES
(0, '数码电子', 'ELECTRONICS', '', 1, 1),
(0, '服装鞋包', 'CLOTHING', '', 2, 1),
(0, '食品生鲜', 'FOOD', '', 3, 1),
(0, '家居生活', 'HOME', '', 4, 1),
(0, '美妆护肤', 'COSMETICS', '', 5, 1),
(0, '运动户外', 'SPORTS', '', 6, 1),
(0, '图书文具', 'BOOKS', '', 7, 1),
(0, '其他商品', 'OTHER', '', 8, 1);

-- 插入示例商品（请根据实际情况调整分类ID）
INSERT INTO `sp_product` (`category_id`, `product_name`, `product_code`, `main_image`, `images`, `price`, `original_price`, `member_price`, `stock`, `sales`, `brief`, `description`, `status`, `is_hot`, `is_new`, `is_recommend`, `sort`) VALUES
(1, 'iPhone 15 Pro Max 256GB', 'ELEC001', 'https://via.placeholder.com/400x400/333333/FFFFFF?text=iPhone+15', '["https://via.placeholder.com/400x400/333333/FFFFFF?text=iPhone+15-1"]', 9999.00, 10999.00, 9499.00, 100, 50, '全新iPhone 15 Pro Max，钛金属设计，A17 Pro芯片', '<p>产品详情</p>', 1, 1, 1, 1, 1),
(1, 'AirPods Pro 2', 'ELEC002', 'https://via.placeholder.com/400x400/333333/FFFFFF?text=AirPods', '["https://via.placeholder.com/400x400/333333/FFFFFF?text=AirPods-1"]', 1899.00, 1999.00, 1799.00, 200, 120, '全新升级的主动降噪功能', '<p>产品详情</p>', 1, 1, 0, 1, 2),
(2, '男士纯棉休闲T恤', 'CLOTH001', 'https://via.placeholder.com/400x400/4A90E2/FFFFFF?text=T-Shirt', '["https://via.placeholder.com/400x400/4A90E2/FFFFFF?text=T-Shirt-1"]', 99.00, 199.00, 89.00, 500, 300, '舒适纯棉面料，多色可选', '<p>产品详情</p>', 1, 0, 1, 0, 1),
(3, '新鲜有机红富士苹果 5斤装', 'FOOD001', 'https://via.placeholder.com/400x400/E24A4A/FFFFFF?text=Apple', '["https://via.placeholder.com/400x400/E24A4A/FFFFFF?text=Apple-1"]', 49.90, 69.90, 39.90, 1000, 800, '产自甘肃静宁的有机红富士，口感脆甜', '<p>产品详情</p>', 1, 1, 0, 1, 1),
(4, '北欧风格台灯', 'HOME001', 'https://via.placeholder.com/400x400/7B68EE/FFFFFF?text=Lamp', '["https://via.placeholder.com/400x400/7B68EE/FFFFFF?text=Lamp-1"]', 199.00, 299.00, 179.00, 150, 80, '简约北欧风格，适合书房和卧室', '<p>产品详情</p>', 1, 0, 1, 1, 1),
(5, '补水保湿面膜 10片装', 'COS001', 'https://via.placeholder.com/400x400/FF69B4/FFFFFF?text=Face+Mask', '["https://via.placeholder.com/400x400/FF69B4/FFFFFF?text=Face+Mask-1"]', 89.00, 129.00, 79.00, 300, 200, '深层补水，温和不刺激', '<p>产品详情</p>', 1, 1, 1, 1, 1),
(6, '瑜伽垫 加厚防滑', 'SPORT001', 'https://via.placeholder.com/400x400/00CED1/FFFFFF?text=Yoga+Mat', '["https://via.placeholder.com/400x400/00CED1/FFFFFF?text=Yoga+Mat-1"]', 79.00, 99.00, 69.00, 400, 250, '加厚10mm，防滑抗菌', '<p>产品详情</p>', 1, 1, 0, 1, 1),
(7, '精装版《活着》', 'BOOK001', 'https://via.placeholder.com/400x400/8B4513/FFFFFF?text=Book', '["https://via.placeholder.com/400x400/8B4513/FFFFFF?text=Book-1"]', 39.00, 49.00, 35.00, 200, 150, '余华代表作精装版', '<p>产品详情</p>', 1, 0, 1, 0, 1);

-- 插入示例订单
INSERT INTO `sp_order` (`order_no`, `user_id`, `total_amount`, `discount_amount`, `pay_amount`, `freight_amount`, `receiver_name`, `receiver_phone`, `receiver_province`, `receiver_city`, `receiver_district`, `receiver_address`, `status`, `created_at`) VALUES
('SP202401010001', 1001, 199.00, 10.00, 189.00, 0.00, '张三', '13800000001', '北京市', '北京市', '朝阳区', '建国路1号', 'FINISHED', DATE_SUB(NOW(), INTERVAL 15 DAY)),
('SP202401010002', 1002, 299.00, 20.00, 279.00, 0.00, '李四', '13800000002', '上海市', '上海市', '浦东新区', '世纪大道2号', 'SHIPPED', DATE_SUB(NOW(), INTERVAL 10 DAY)),
('SP202401010003', 1003, 499.00, 30.00, 469.00, 0.00, '王五', '13800000003', '广东省', '深圳市', '南山区', '科技路3号', 'PAID', DATE_SUB(NOW(), INTERVAL 5 DAY)),
('SP202401010004', 1004, 99.00, 5.00, 94.00, 0.00, '赵六', '13800000004', '浙江省', '杭州市', '西湖区', '文一路4号', 'PENDING_PAY', DATE_SUB(NOW(), INTERVAL 2 DAY)),
('SP202401010005', 1005, 1999.00, 100.00, 1899.00, 0.00, '钱七', '13800000005', '江苏省', '南京市', '鼓楼区', '中山路5号', 'CANCELLED', DATE_SUB(NOW(), INTERVAL 7 DAY));

-- 插入订单明细
INSERT INTO `sp_order_item` (`order_id`, `product_id`, `product_name`, `product_image`, `price`, `member_price`, `quantity`, `total_amount`) VALUES
(1, 1, 'iPhone 15 Pro Max 256GB', 'https://via.placeholder.com/400x400/333333/FFFFFF?text=iPhone+15', 9999.00, 9499.00, 1, 9999.00),
(2, 2, 'AirPods Pro 2', 'https://via.placeholder.com/400x400/333333/FFFFFF?text=AirPods', 1899.00, 1799.00, 1, 1899.00),
(3, 3, '男士纯棉休闲T恤', 'https://via.placeholder.com/400x400/4A90E2/FFFFFF?text=T-Shirt', 99.00, 89.00, 3, 297.00),
(4, 4, '新鲜有机红富士苹果 5斤装', 'https://via.placeholder.com/400x400/E24A4A/FFFFFF?text=Apple', 49.90, 39.90, 2, 99.00),
(5, 5, '北欧风格台灯', 'https://via.placeholder.com/400x400/7B68EE/FFFFFF?text=Lamp', 199.00, 179.00, 1, 199.00);
