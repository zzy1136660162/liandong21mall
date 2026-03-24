-- 商品收藏表创建脚本
-- 数据库: MySQL 5.7+
-- 字符集: utf8mb4
-- 创建日期: 2026-03-19
-- 模块负责人: 商品商城模块

-- =====================================================
-- 创建商品收藏表 (product_favorite)
-- 说明: 存储用户商品收藏信息
-- =====================================================
CREATE TABLE IF NOT EXISTS `product_favorite` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '收藏ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `product_id` bigint unsigned NOT NULL COMMENT '商品ID',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_product` (`user_id`, `product_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_product_id` (`product_id`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_favorite_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_favorite_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品收藏表';

-- =====================================================
-- 完成
-- =====================================================
