-- 联动21商城数据库表结构
-- 生成时间: 2026-03-16
-- 表前缀: xp_

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for xp_products (商品表)
-- ----------------------------
DROP TABLE IF EXISTS `xp_products`;
CREATE TABLE `xp_products` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '商品ID',
  `product_no` varchar(50) NOT NULL COMMENT '商品编号',
  `name` varchar(200) NOT NULL COMMENT '商品名称',
  `subtitle` varchar(500) DEFAULT NULL COMMENT '副标题',
  `category_id` bigint unsigned NOT NULL COMMENT '分类ID',
  `main_image` varchar(500) NOT NULL COMMENT '主图',
  `images` json DEFAULT NULL COMMENT '商品图片列表',
  `price` decimal(10,2) NOT NULL COMMENT '售价',
  `original_price` decimal(10,2) DEFAULT NULL COMMENT '原价',
  `supply_price` decimal(10,2) NOT NULL COMMENT '供货价',
  `stock` int DEFAULT '0' COMMENT '库存',
  `sales` int DEFAULT '0' COMMENT '销量',
  `unit` varchar(20) DEFAULT '件' COMMENT '单位',
  `weight` decimal(8,2) DEFAULT NULL COMMENT '重量(kg)',
  `description` text COMMENT '商品详情',
  `specifications` json DEFAULT NULL COMMENT '规格参数',
  `shop_id` bigint unsigned NOT NULL COMMENT '店铺ID',
  `is_brand` tinyint DEFAULT '0' COMMENT '是否品牌：0-否，1-是',
  `is_cashback` tinyint DEFAULT '0' COMMENT '是否返现：0-否，1-是',
  `is_trust` tinyint DEFAULT '0' COMMENT '是否信任购：0-否，1-是',
  `status` tinyint DEFAULT '1' COMMENT '状态：0-下架，1-上架',
  `sort` int DEFAULT '0' COMMENT '排序',
  `is_hot` tinyint DEFAULT '0' COMMENT '是否热门：0-否，1-是',
  `is_new` tinyint DEFAULT '0' COMMENT '是否新品：0-否，1-是',
  `is_recommend` tinyint DEFAULT '0' COMMENT '是否推荐：0-否，1-是',
  `commission_rate` decimal(4,2) DEFAULT '10.00' COMMENT '基础佣金比例',
  `normal_rate` decimal(4,2) DEFAULT '10.00' COMMENT '普通达人佣金比例',
  `premium_rate` decimal(4,2) DEFAULT '15.00' COMMENT '优质达人佣金比例',
  `top_rate` decimal(4,2) DEFAULT '20.00' COMMENT '头部达人佣金比例',
  `settlement_type` tinyint DEFAULT '1' COMMENT '结算类型：1-月结，2-周结，3-实时',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_product_no` (`product_no`),
  KEY `idx_category_id` (`category_id`),
  KEY `idx_shop_id` (`shop_id`),
  KEY `idx_status` (`status`),
  KEY `idx_sort` (`sort`),
  KEY `idx_is_hot` (`is_hot`),
  KEY `idx_is_new` (`is_new`),
  KEY `idx_is_recommend` (`is_recommend`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表';

-- ----------------------------
-- Table structure for xp_sample_application_products (样品申请商品关联表)
-- ----------------------------
DROP TABLE IF EXISTS `xp_sample_application_products`;
CREATE TABLE `xp_sample_application_products` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `application_id` bigint unsigned NOT NULL COMMENT '申请ID',
  `product_id` bigint unsigned NOT NULL COMMENT '商品ID',
  `product_name` varchar(200) NOT NULL COMMENT '商品名称（快照）',
  `product_image` varchar(500) NOT NULL COMMENT '商品图片（快照）',
  `product_price` decimal(10,2) NOT NULL COMMENT '商品价格（快照）',
  `commission_rate` decimal(4,2) DEFAULT NULL COMMENT '佣金比例（快照）',
  `quantity` int DEFAULT '1' COMMENT '申请数量',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_application_product` (`application_id`,`product_id`),
  KEY `idx_application_id` (`application_id`),
  KEY `idx_product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='样品申请商品关联表';

-- ----------------------------
-- Table structure for xp_search_history (搜索历史表)
-- ----------------------------
DROP TABLE IF EXISTS `xp_search_history`;
CREATE TABLE `xp_search_history` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_id` bigint unsigned DEFAULT NULL COMMENT '用户ID，null表示热门搜索',
  `keyword` varchar(100) NOT NULL COMMENT '搜索关键词',
  `search_count` int DEFAULT '1' COMMENT '搜索次数',
  `last_search_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后搜索时间',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_keyword` (`user_id`,`keyword`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_keyword` (`keyword`),
  KEY `idx_search_count` (`search_count`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='搜索历史表';

-- ----------------------------
-- Table structure for xp_categories (商品分类表)
-- ----------------------------
DROP TABLE IF EXISTS `xp_categories`;
CREATE TABLE `xp_categories` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `name` varchar(50) NOT NULL COMMENT '分类名称',
  `parent_id` bigint unsigned DEFAULT '0' COMMENT '父分类ID，0表示一级分类',
  `level` tinyint DEFAULT '1' COMMENT '层级：1-一级分类，2-二级分类，3-三级分类',
  `icon` varchar(500) DEFAULT NULL COMMENT '分类图标',
  `sort` int DEFAULT '0' COMMENT '排序',
  `status` tinyint DEFAULT '1' COMMENT '状态：0-禁用，1-启用',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_parent_id` (`parent_id`),
  KEY `idx_level` (`level`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品分类表';

-- ----------------------------
-- Table structure for xp_banners (轮播图表)
-- ----------------------------
DROP TABLE IF EXISTS `xp_banners`;
CREATE TABLE `xp_banners` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '轮播图ID',
  `title` varchar(100) NOT NULL COMMENT '标题',
  `image` varchar(500) NOT NULL COMMENT '图片URL',
  `link` varchar(500) DEFAULT NULL COMMENT '跳转链接',
  `link_type` varchar(20) DEFAULT NULL COMMENT '链接类型：product-商品，category-分类，url-网页',
  `sort` int DEFAULT '0' COMMENT '排序',
  `status` tinyint DEFAULT '1' COMMENT '状态：0-禁用，1-启用',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`),
  KEY `idx_sort` (`sort`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='轮播图表';

-- ----------------------------
-- 初始化数据
-- ----------------------------

-- 一级分类
INSERT INTO `xp_categories` (`name`, `parent_id`, `level`, `sort`) VALUES
('零食饮料', 0, 1, 1),
('家居百货', 0, 1, 2),
('女装女鞋', 0, 1, 3),
('美妆护肤', 0, 1, 4),
('个护清洁', 0, 1, 5),
('医疗保健', 0, 1, 6),
('母婴玩具', 0, 1, 7),
('生鲜食品', 0, 1, 8),
('男装男鞋', 0, 1, 9),
('运动户外', 0, 1, 10),
('数码家电', 0, 1, 11),
('珠宝奢品', 0, 1, 12),
('茶叶酒水', 0, 1, 13);

-- 二级分类（零食饮料）
INSERT INTO `xp_categories` (`name`, `parent_id`, `level`, `sort`) VALUES
('休闲零食', 1, 2, 1),
('饮料冲调', 1, 2, 2),
('方便速食', 1, 2, 3),
('粮油调味', 1, 2, 4);

-- 二级分类（家居百货）
INSERT INTO `xp_categories` (`name`, `parent_id`, `level`, `sort`) VALUES
('家具', 2, 2, 1),
('家居家纺', 2, 2, 2),
('家用清洁', 2, 2, 3),
('床上用品', 2, 2, 4),
('生活日用', 2, 2, 5),
('纸品湿巾', 2, 2, 6),
('餐厨用具', 2, 2, 7);

-- 二级分类（女装女鞋）
INSERT INTO `xp_categories` (`name`, `parent_id`, `level`, `sort`) VALUES
('上装', 3, 2, 1),
('下装', 3, 2, 2),
('裙装', 3, 2, 3),
('内衣裤袜', 3, 2, 4),
('女士包袋', 3, 2, 5),
('女鞋', 3, 2, 6),
('家居服', 3, 2, 7);

-- 二级分类（美妆护肤）
INSERT INTO `xp_categories` (`name`, `parent_id`, `level`, `sort`) VALUES
('女士彩妆', 4, 2, 1),
('女士护肤', 4, 2, 2),
('男士彩妆', 4, 2, 3),
('男士护肤', 4, 2, 4),
('美发用品', 4, 2, 5),
('美妆工具', 4, 2, 6);

-- 热门搜索
INSERT INTO `xp_search_history` (`user_id`, `keyword`, `search_count`) VALUES
(NULL, '洗衣液', 100),
(NULL, '抽纸', 95),
(NULL, '面膜', 90),
(NULL, '口红', 85),
(NULL, '零食', 80),
(NULL, '洗发水', 75),
(NULL, '牙膏', 70),
(NULL, '洗衣粉', 65);

-- 轮播图初始数据
INSERT INTO `xp_banners` (`title`, `image`, `link`, `link_type`, `sort`, `status`) VALUES
('新人高佣专场', 'https://picsum.photos/750/280?random=101', '/pages/rank/rank', 'url', 1, 1),
('春日爆品计划', 'https://picsum.photos/750/280?random=102', '', 'product', 2, 1),
('正品保障', 'https://picsum.photos/750/280?random=103', '', 'brand', 3, 1),
('申请样品攻略', 'https://picsum.photos/750/280?random=104', '', 'guide', 4, 1);

SET FOREIGN_KEY_CHECKS = 1;
