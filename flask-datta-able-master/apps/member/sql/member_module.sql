-- 会员达人模块数据库初始化脚本
-- 数据库: MySQL 5.7+
-- 字符集: utf8mb4
-- 创建日期: 2026-03-13
-- 模块负责人: 李爱博

-- =====================================================
-- 1. 创建会员等级表 (member_level)
-- 说明: 存储会员等级配置信息
-- =====================================================
CREATE TABLE IF NOT EXISTS `member_level` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '等级ID',
  `level_code` varchar(20) NOT NULL COMMENT '等级编码：normal/vip/partner',
  `level_name` varchar(50) NOT NULL COMMENT '等级名称',
  `discount` decimal(3,2) NOT NULL DEFAULT '1.00' COMMENT '折扣率，0.95表示95折',
  `upgrade_condition` text COMMENT '升级条件描述',
  `benefits` json COMMENT '权益配置JSON',
  `sort` int NOT NULL DEFAULT '0' COMMENT '排序',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_level_code` (`level_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员等级表';

-- 初始化会员等级数据
INSERT INTO `member_level` (`level_code`, `level_name`, `discount`, `upgrade_condition`, `benefits`) VALUES
('normal', '普通用户', 1.00, '注册即成为普通用户', '[{"type":"base","name":"基础购物"}]'),
('vip', 'VIP会员', 0.95, '完成首单自动升级', '[{"type":"discount","name":"全场95折"},{"type":"points","name":"积分翻倍"}]'),
('partner', '合伙人', 0.90, '推广业绩达标', '[{"type":"discount","name":"全场9折"},{"type":"commission","name":"分销佣金"},{"type":"team","name":"团队管理奖"}]');

-- =====================================================
-- 2. 创建用户主表 (user)
-- 说明: 存储用户基础信息，由会员达人模块维护
-- =====================================================
CREATE TABLE IF NOT EXISTS `user` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `openid` varchar(100) NOT NULL COMMENT '微信openid',
  `unionid` varchar(100) DEFAULT NULL COMMENT '微信unionid',
  `nickname` varchar(100) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(500) DEFAULT NULL COMMENT '头像URL',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态：1正常 0禁用',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_openid` (`openid`),
  KEY `idx_phone` (`phone`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户主表';

-- =====================================================
-- 3. 创建用户会员关系表 (user_member)
-- 说明: 存储用户与会员等级的关联关系
-- =====================================================
CREATE TABLE IF NOT EXISTS `user_member` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `level_id` int unsigned NOT NULL COMMENT '等级ID',
  `level_code` varchar(20) NOT NULL COMMENT '等级编码',
  `upgrade_type` tinyint NOT NULL DEFAULT '1' COMMENT '升级方式：1首单自动 2手动 3后台',
  `upgrade_time` datetime DEFAULT NULL COMMENT '升级时间',
  `first_order_id` bigint unsigned DEFAULT NULL COMMENT '首单订单ID',
  `valid_start` datetime NOT NULL COMMENT '有效期开始',
  `valid_end` datetime DEFAULT NULL COMMENT '有效期结束，null表示永久',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_id` (`user_id`),
  KEY `idx_level_code` (`level_code`),
  CONSTRAINT `fk_user_member_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_user_member_level` FOREIGN KEY (`level_id`) REFERENCES `member_level` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户会员关系表';

-- =====================================================
-- 4. 创建达人申请表 (talent_apply)
-- 说明: 存储达人申请记录
-- =====================================================
CREATE TABLE IF NOT EXISTS `talent_apply` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '申请ID',
  `user_id` bigint unsigned NOT NULL COMMENT '申请人ID',
  `real_name` varchar(50) NOT NULL COMMENT '真实姓名',
  `phone` varchar(20) NOT NULL COMMENT '手机号',
  `region` varchar(100) DEFAULT NULL COMMENT '所在地区',
  `apply_reason` text COMMENT '申请理由',
  `intro` text COMMENT '个人简介',
  `status` varchar(20) NOT NULL DEFAULT 'PENDING' COMMENT '状态：PENDING/APPROVED/REJECTED',
  `reject_reason` varchar(500) DEFAULT NULL COMMENT '拒绝原因',
  `audit_time` datetime DEFAULT NULL COMMENT '审核时间',
  `audit_by` bigint unsigned DEFAULT NULL COMMENT '审核人ID',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_talent_apply_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='达人申请表';

-- =====================================================
-- 5. 创建用户地址表 (user_address)
-- 说明: 存储用户收货地址
-- =====================================================
CREATE TABLE IF NOT EXISTS `user_address` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '地址ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `name` varchar(50) NOT NULL COMMENT '收货人姓名',
  `phone` varchar(20) NOT NULL COMMENT '收货人手机号',
  `province` varchar(50) NOT NULL COMMENT '省份',
  `city` varchar(50) NOT NULL COMMENT '城市',
  `district` varchar(50) NOT NULL COMMENT '区县',
  `detail` varchar(200) NOT NULL COMMENT '详细地址',
  `is_default` tinyint NOT NULL DEFAULT '0' COMMENT '是否默认：1是 0否',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  CONSTRAINT `fk_user_address_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户地址表';

-- =====================================================
-- 6. 创建索引优化
-- =====================================================

-- 用户表索引
ALTER TABLE `user` ADD INDEX `idx_status` (`status`);

-- 达人申请表索引
ALTER TABLE `talent_apply` ADD INDEX `idx_audit_by` (`audit_by`);

-- 用户地址表索引
ALTER TABLE `user_address` ADD INDEX `idx_is_default` (`is_default`);

-- =====================================================
-- 完成
-- =====================================================
