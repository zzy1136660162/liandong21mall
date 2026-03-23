-- ========================================
-- 商品商城模块数据库表结构 (sp_前缀)
-- 成员1负责：商品、购物车、订单、地址
-- ========================================

-- ========================================
-- 1. 商品分类表
-- ========================================
DROP TABLE IF EXISTS `sp_product_category`;
CREATE TABLE `sp_product_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `parent_id` int(11) NOT NULL DEFAULT '0' COMMENT '父分类ID',
  `category_name` varchar(50) NOT NULL COMMENT '分类名称',
  `category_code` varchar(50) NOT NULL COMMENT '分类编码',
  `icon` varchar(500) DEFAULT NULL COMMENT '分类图标URL',
  `sort` int(11) NOT NULL DEFAULT '0' COMMENT '排序',
  `status` smallint(6) NOT NULL DEFAULT '1' COMMENT '状态：1启用 0禁用',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_category_code` (`category_code`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

-- ========================================
-- 2. 商品表
-- ========================================
DROP TABLE IF EXISTS `sp_product`;
CREATE TABLE `sp_product` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '商品ID',
  `category_id` int(11) NOT NULL COMMENT '分类ID',
  `product_name` varchar(200) NOT NULL COMMENT '商品名称',
  `product_code` varchar(50) NOT NULL COMMENT '商品编码',
  `main_image` varchar(500) NOT NULL COMMENT '主图URL',
  `images` json DEFAULT NULL COMMENT '商品图片列表JSON',
  `price` decimal(10,2) NOT NULL COMMENT '销售价格',
  `original_price` decimal(10,2) DEFAULT NULL COMMENT '原价',
  `member_price` decimal(10,2) DEFAULT NULL COMMENT '会员价',
  `stock` int(11) NOT NULL DEFAULT '0' COMMENT '库存数量',
  `sales` int(11) NOT NULL DEFAULT '0' COMMENT '销量',
  `brief` varchar(500) DEFAULT NULL COMMENT '商品简介',
  `description` text COMMENT '商品详情HTML',
  `status` smallint(6) NOT NULL DEFAULT '1' COMMENT '状态：1上架 0下架',
  `is_hot` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否热销：1是 0否',
  `is_new` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否新品：1是 0否',
  `is_recommend` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否推荐：1是 0否',
  `sort` int(11) NOT NULL DEFAULT '0' COMMENT '排序',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_product_code` (`product_code`),
  KEY `idx_category_id` (`category_id`),
  KEY `idx_status` (`status`),
  KEY `idx_is_hot` (`is_hot`),
  KEY `idx_is_new` (`is_new`),
  KEY `idx_is_recommend` (`is_recommend`),
  KEY `idx_sales` (`sales`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_product_category` FOREIGN KEY (`category_id`) REFERENCES `sp_product_category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';

-- ========================================
-- 3. 商品SKU表
-- ========================================
DROP TABLE IF EXISTS `sp_product_sku`;
CREATE TABLE `sp_product_sku` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'SKU ID',
  `product_id` bigint(20) NOT NULL COMMENT '商品ID',
  `sku_code` varchar(50) NOT NULL COMMENT 'SKU编码',
  `sku_name` varchar(100) NOT NULL COMMENT 'SKU名称',
  `spec` json DEFAULT NULL COMMENT '规格属性JSON',
  `price` decimal(10,2) NOT NULL COMMENT 'SKU价格',
  `original_price` decimal(10,2) DEFAULT NULL COMMENT 'SKU原价',
  `member_price` decimal(10,2) DEFAULT NULL COMMENT 'SKU会员价',
  `stock` int(11) NOT NULL DEFAULT '0' COMMENT 'SKU库存',
  `image` varchar(500) DEFAULT NULL COMMENT 'SKU图片',
  `status` smallint(6) NOT NULL DEFAULT '1' COMMENT '状态：1启用 0禁用',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_sku_code` (`sku_code`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_sku_product` FOREIGN KEY (`product_id`) REFERENCES `sp_product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品SKU表';

-- ========================================
-- 4. 购物车表
-- ========================================
DROP TABLE IF EXISTS `sp_cart`;
CREATE TABLE `sp_cart` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '购物车ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `product_id` bigint(20) NOT NULL COMMENT '商品ID',
  `sku_id` bigint(20) DEFAULT NULL COMMENT 'SKU ID',
  `quantity` int(11) NOT NULL DEFAULT '1' COMMENT '数量',
  `selected` smallint(6) NOT NULL DEFAULT '1' COMMENT '是否选中：1是 0否',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_sku_id` (`sku_id`),
  CONSTRAINT `fk_cart_product` FOREIGN KEY (`product_id`) REFERENCES `sp_product` (`id`),
  CONSTRAINT `fk_cart_sku` FOREIGN KEY (`sku_id`) REFERENCES `sp_product_sku` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='购物车表';

-- ========================================
-- 5. 订单表
-- ========================================
DROP TABLE IF EXISTS `sp_order`;
CREATE TABLE `sp_order` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '订单ID',
  `order_no` varchar(50) NOT NULL COMMENT '订单编号',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `total_amount` decimal(10,2) NOT NULL COMMENT '订单总金额',
  `discount_amount` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '优惠金额',
  `pay_amount` decimal(10,2) NOT NULL COMMENT '实付金额',
  `freight_amount` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '运费',
  `receiver_name` varchar(50) NOT NULL COMMENT '收货人姓名',
  `receiver_phone` varchar(20) NOT NULL COMMENT '收货人手机号',
  `receiver_province` varchar(50) DEFAULT NULL COMMENT '省',
  `receiver_city` varchar(50) DEFAULT NULL COMMENT '市',
  `receiver_district` varchar(50) DEFAULT NULL COMMENT '区',
  `receiver_address` varchar(500) NOT NULL COMMENT '收货地址',
  `status` varchar(20) NOT NULL DEFAULT 'PENDING_PAY' COMMENT '订单状态',
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
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- ========================================
-- 6. 订单明细表
-- ========================================
DROP TABLE IF EXISTS `sp_order_item`;
CREATE TABLE `sp_order_item` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '订单明细ID',
  `order_id` bigint(20) NOT NULL COMMENT '订单ID',
  `product_id` bigint(20) NOT NULL COMMENT '商品ID',
  `sku_id` bigint(20) DEFAULT NULL COMMENT 'SKU ID',
  `product_name` varchar(200) NOT NULL COMMENT '商品名称',
  `sku_name` varchar(100) DEFAULT NULL COMMENT 'SKU名称',
  `product_image` varchar(500) NOT NULL COMMENT '商品图片',
  `price` decimal(10,2) NOT NULL COMMENT '商品单价',
  `member_price` decimal(10,2) DEFAULT NULL COMMENT '会员价',
  `quantity` int(11) NOT NULL COMMENT '购买数量',
  `total_amount` decimal(10,2) NOT NULL COMMENT '小计金额',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_sku_id` (`sku_id`),
  CONSTRAINT `fk_order_item_order` FOREIGN KEY (`order_id`) REFERENCES `sp_order` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_order_item_product` FOREIGN KEY (`product_id`) REFERENCES `sp_product` (`id`),
  CONSTRAINT `fk_order_item_sku` FOREIGN KEY (`sku_id`) REFERENCES `sp_product_sku` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单明细表';

-- ========================================
-- 7. 收货地址表
-- ========================================
DROP TABLE IF EXISTS `sp_address`;
CREATE TABLE `sp_address` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '地址ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `name` varchar(50) NOT NULL COMMENT '收货人姓名',
  `phone` varchar(20) NOT NULL COMMENT '手机号码',
  `province` varchar(50) NOT NULL COMMENT '省',
  `city` varchar(50) NOT NULL COMMENT '市',
  `district` varchar(50) NOT NULL COMMENT '区',
  `detail` varchar(500) NOT NULL COMMENT '详细地址',
  `postcode` varchar(10) DEFAULT NULL COMMENT '邮政编码',
  `is_default` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否默认：1是 0否',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_is_default` (`is_default`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收货地址表';
