-- 商品详情模块数据库初始化脚本
-- 数据库: MySQL 5.7+
-- 字符集: utf8mb4
-- 创建日期: 2026-03-19
-- 模块负责人: 商品商城模块
-- 注意: 所有表名以sp_开头，避免与其他模块冲突

-- =====================================================
-- 1. 创建商品详情扩展表 (sp_product_detail)
-- 说明: 存储商品详情的扩展信息，包括标签、规格等
-- =====================================================
CREATE TABLE IF NOT EXISTS `sp_product_detail` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '详情ID',
  `product_id` bigint unsigned NOT NULL COMMENT '商品ID，关联product表',
  `subtitle` varchar(500) DEFAULT NULL COMMENT '商品副标题',
  `tags` json DEFAULT NULL COMMENT '商品标签JSON数组，如["新品","热销","包邮"]',
  `specs` json DEFAULT NULL COMMENT '商品规格JSON，如[{"name":"颜色","values":["红色","蓝色"]},{"name":"尺寸","values":["S","M","L"]}]',
  `description` text COMMENT '商品详情HTML',
  `video_url` varchar(500) DEFAULT NULL COMMENT '商品视频URL',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_product_id` (`product_id`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_sp_detail_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品详情扩展表';

-- =====================================================
-- 2. 创建商品评价表 (sp_product_review)
-- 说明: 存储商品用户评价信息
-- =====================================================
CREATE TABLE IF NOT EXISTS `sp_product_review` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '评价ID',
  `product_id` bigint unsigned NOT NULL COMMENT '商品ID，关联product表',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID，关联user表',
  `order_id` bigint unsigned DEFAULT NULL COMMENT '订单ID，关联order表',
  `rating` tinyint NOT NULL DEFAULT '5' COMMENT '评分：1-5星',
  `content` text COMMENT '评价内容',
  `images` json DEFAULT NULL COMMENT '评价图片JSON数组',
  `is_anonymous` tinyint NOT NULL DEFAULT '0' COMMENT '是否匿名：1是 0否',
  `reply_content` text COMMENT '商家回复内容',
  `reply_time` datetime DEFAULT NULL COMMENT '商家回复时间',
  `is_show` tinyint NOT NULL DEFAULT '1' COMMENT '是否显示：1是 0否',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_order_id` (`order_id`),
  KEY `idx_rating` (`rating`),
  KEY `idx_is_show` (`is_show`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_sp_review_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_sp_review_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_sp_review_order` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品评价表';

-- =====================================================
-- 3. 创建商品收藏表 (sp_product_favorite)
-- 说明: 存储用户商品收藏信息
-- =====================================================
CREATE TABLE IF NOT EXISTS `sp_product_favorite` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '收藏ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID，关联user表',
  `product_id` bigint unsigned NOT NULL COMMENT '商品ID，关联product表',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_product` (`user_id`, `product_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_sp_favorite_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_sp_favorite_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品收藏表';

-- =====================================================
-- 4. 创建商品推荐表 (sp_product_recommendation)
-- 说明: 存储商品推荐关系
-- =====================================================
CREATE TABLE IF NOT EXISTS `sp_product_recommendation` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '推荐ID',
  `product_id` bigint unsigned NOT NULL COMMENT '商品ID，关联product表',
  `recommend_product_id` bigint unsigned NOT NULL COMMENT '推荐商品ID，关联product表',
  `sort` int NOT NULL DEFAULT '0' COMMENT '排序',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_recommend_product_id` (`recommend_product_id`),
  KEY `idx_sort` (`sort`),
  CONSTRAINT `fk_sp_recommend_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_sp_recommend_product_ref` FOREIGN KEY (`recommend_product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品推荐表';

-- =====================================================
-- 5. 创建商品浏览记录表 (sp_product_view)
-- 说明: 存储用户商品浏览记录
-- =====================================================
CREATE TABLE IF NOT EXISTS `sp_product_view` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '浏览ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID，关联user表',
  `product_id` bigint unsigned NOT NULL COMMENT '商品ID，关联product表',
  `view_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '浏览时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_view_time` (`view_time`),
  CONSTRAINT `fk_sp_view_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_sp_view_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品浏览记录表';

-- =====================================================
-- 完成
-- =====================================================
