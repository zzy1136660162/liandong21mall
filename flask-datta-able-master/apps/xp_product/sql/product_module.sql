-- 商品商城模块数据库初始化脚本
-- 数据库: MySQL 5.7+
-- 字符集: utf8mb4
-- 创建日期: 2026-03-17
-- 模块负责人: 商品商城模块

-- =====================================================
-- 1. 创建商品分类表 (product_category)
-- 说明: 存储商品分类信息
-- =====================================================
CREATE TABLE IF NOT EXISTS `product_category` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `parent_id` int unsigned NOT NULL DEFAULT '0' COMMENT '父分类ID，0表示顶级分类',
  `category_name` varchar(50) NOT NULL COMMENT '分类名称',
  `category_code` varchar(50) NOT NULL COMMENT '分类编码',
  `icon` varchar(500) DEFAULT NULL COMMENT '分类图标URL',
  `sort` int NOT NULL DEFAULT '0' COMMENT '排序',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态：1启用 0禁用',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_category_code` (`category_code`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_sort` (`sort`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

-- 初始化商品分类数据
INSERT INTO `product_category` (`parent_id`, `category_name`, `category_code`, `icon`, `sort`, `status`) VALUES
(0, '护肤', 'skincare', '/static/images/category/skincare.png', 1, 1),
(0, '彩妆', 'makeup', '/static/images/category/makeup.png', 2, 1),
(0, '个护', 'personal_care', '/static/images/category/personal_care.png', 3, 1),
(0, '食品', 'food', '/static/images/category/food.png', 4, 1),
(0, '家居', 'home', '/static/images/category/home.png', 5, 1);

-- =====================================================
-- 2. 创建商品表 (product)
-- 说明: 存储商品基础信息
-- =====================================================
CREATE TABLE IF NOT EXISTS `product` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '商品ID',
  `category_id` int unsigned NOT NULL COMMENT '分类ID',
  `product_name` varchar(200) NOT NULL COMMENT '商品名称',
  `product_code` varchar(50) NOT NULL COMMENT '商品编码',
  `main_image` varchar(500) NOT NULL COMMENT '主图URL',
  `images` json COMMENT '商品图片列表JSON',
  `price` decimal(10,2) NOT NULL COMMENT '销售价格',
  `original_price` decimal(10,2) DEFAULT NULL COMMENT '原价',
  `member_price` decimal(10,2) DEFAULT NULL COMMENT '会员价',
  `stock` int NOT NULL DEFAULT '0' COMMENT '库存数量',
  `sales` int NOT NULL DEFAULT '0' COMMENT '销量',
  `brief` varchar(500) DEFAULT NULL COMMENT '商品简介',
  `description` text COMMENT '商品详情HTML',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态：1上架 0下架',
  `is_hot` tinyint NOT NULL DEFAULT '0' COMMENT '是否热销：1是 0否',
  `is_new` tinyint NOT NULL DEFAULT '0' COMMENT '是否新品：1是 0否',
  `is_recommend` tinyint NOT NULL DEFAULT '0' COMMENT '是否推荐：1是 0否',
  `sort` int NOT NULL DEFAULT '0' COMMENT '排序',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_product_code` (`product_code`),
  KEY `idx_category_id` (`category_id`),
  KEY `idx_status` (`status`),
  KEY `idx_is_hot` (`is_hot`),
  KEY `idx_is_new` (`is_new`),
  KEY `idx_is_recommend` (`is_recommend`),
  KEY `idx_sort` (`sort`),
  KEY `idx_sales` (`sales`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_product_category` FOREIGN KEY (`category_id`) REFERENCES `product_category` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';

-- =====================================================
-- 3. 创建商品SKU表 (product_sku)
-- 说明: 存储商品SKU信息
-- =====================================================
CREATE TABLE IF NOT EXISTS `product_sku` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'SKU ID',
  `product_id` bigint unsigned NOT NULL COMMENT '商品ID',
  `sku_code` varchar(50) NOT NULL COMMENT 'SKU编码',
  `sku_name` varchar(100) NOT NULL COMMENT 'SKU名称',
  `spec` json COMMENT '规格属性JSON，如{"color":"红色","size":"M"}',
  `price` decimal(10,2) NOT NULL COMMENT 'SKU价格',
  `original_price` decimal(10,2) DEFAULT NULL COMMENT 'SKU原价',
  `member_price` decimal(10,2) DEFAULT NULL COMMENT 'SKU会员价',
  `stock` int NOT NULL DEFAULT '0' COMMENT 'SKU库存',
  `image` varchar(500) DEFAULT NULL COMMENT 'SKU图片',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态：1启用 0禁用',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_sku_code` (`sku_code`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_sku_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品SKU表';

-- =====================================================
-- 4. 创建购物车表 (cart)
-- 说明: 存储用户购物车信息
-- =====================================================
CREATE TABLE IF NOT EXISTS `cart` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '购物车ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `product_id` bigint unsigned NOT NULL COMMENT '商品ID',
  `sku_id` bigint unsigned DEFAULT NULL COMMENT 'SKU ID',
  `quantity` int NOT NULL DEFAULT '1' COMMENT '数量',
  `selected` tinyint NOT NULL DEFAULT '1' COMMENT '是否选中：1是 0否',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_product` (`user_id`, `product_id`, `sku_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_sku_id` (`sku_id`),
  CONSTRAINT `fk_cart_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_cart_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_cart_sku` FOREIGN KEY (`sku_id`) REFERENCES `product_sku` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='购物车表';

-- =====================================================
-- 5. 创建订单表 (order)
-- 说明: 存储订单基础信息
-- =====================================================
CREATE TABLE IF NOT EXISTS `order` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `order_no` varchar(50) NOT NULL COMMENT '订单编号',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `total_amount` decimal(10,2) NOT NULL COMMENT '订单总金额',
  `discount_amount` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '优惠金额',
  `pay_amount` decimal(10,2) NOT NULL COMMENT '实付金额',
  `freight_amount` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '运费',
  `receiver_name` varchar(50) NOT NULL COMMENT '收货人姓名',
  `receiver_phone` varchar(20) NOT NULL COMMENT '收货人手机号',
  `receiver_address` varchar(500) NOT NULL COMMENT '收货地址',
  `status` varchar(20) NOT NULL DEFAULT 'PENDING_PAY' COMMENT '订单状态：PENDING_PAY/PAID/SHIPPED/FINISHED/CANCELLED',
  `pay_time` datetime DEFAULT NULL COMMENT '支付时间',
  `ship_time` datetime DEFAULT NULL COMMENT '发货时间',
  `finish_time` datetime DEFAULT NULL COMMENT '完成时间',
  `cancel_time` datetime DEFAULT NULL COMMENT '取消时间',
  `cancel_reason` varchar(500) DEFAULT NULL COMMENT '取消原因',
  `remark` varchar(500) DEFAULT NULL COMMENT '订单备注',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_order_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- =====================================================
-- 6. 创建订单明细表 (order_item)
-- 说明: 存储订单商品明细
-- =====================================================
CREATE TABLE IF NOT EXISTS `order_item` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '订单明细ID',
  `order_id` bigint unsigned NOT NULL COMMENT '订单ID',
  `product_id` bigint unsigned NOT NULL COMMENT '商品ID',
  `sku_id` bigint unsigned DEFAULT NULL COMMENT 'SKU ID',
  `product_name` varchar(200) NOT NULL COMMENT '商品名称',
  `sku_name` varchar(100) DEFAULT NULL COMMENT 'SKU名称',
  `product_image` varchar(500) NOT NULL COMMENT '商品图片',
  `price` decimal(10,2) NOT NULL COMMENT '商品单价',
  `member_price` decimal(10,2) DEFAULT NULL COMMENT '会员价',
  `quantity` int NOT NULL COMMENT '购买数量',
  `total_amount` decimal(10,2) NOT NULL COMMENT '小计金额',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_sku_id` (`sku_id`),
  CONSTRAINT `fk_order_item_order` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_order_item_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `fk_order_item_sku` FOREIGN KEY (`sku_id`) REFERENCES `product_sku` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单明细表';

-- =====================================================
-- 7. 创建索引优化
-- =====================================================

-- 商品表索引
ALTER TABLE `product` ADD INDEX `idx_price` (`price`);

-- 订单表索引
ALTER TABLE `order` ADD INDEX `idx_pay_time` (`pay_time`);
ALTER TABLE `order` ADD INDEX `idx_ship_time` (`ship_time`);

-- =====================================================
-- 完成
-- =====================================================
