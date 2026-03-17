-- 清空并重新创建研发需求模块表
-- 用于解决字符集乱码问题

-- 1. 删除旧表（如果存在）
DROP TABLE IF EXISTS `rd_demand_progress`;
DROP TABLE IF EXISTS `rd_demand`;

-- 2. 创建研发需求主表
CREATE TABLE `rd_demand` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `demand_no` VARCHAR(50) NOT NULL COMMENT '需求编号',
  `title` VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '需求标题',
  `functional_appeal` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '功能诉求',
  `target_audience` VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '目标人群',
  `dosage_form_preference` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '剂型偏好',
  `budget_range` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '预算范围',
  `expected_delivery_time` DATE NOT NULL COMMENT '期望交付时间',
  `remark` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
  `submitter_id` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '提交人ID',
  `submitter_name` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '提交人姓名',
  `submitter_phone` VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '提交人电话',
  `status` TINYINT NOT NULL DEFAULT '0' COMMENT '状态: 0-待处理 1-确认中 2-研发中 3-样品制作 4-已完成 5-已取消',
  `status_text` VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '状态文本',
  `admin_remark` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '处理备注',
  `handler_name` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '处理人',
  `submit_time` DATETIME NOT NULL COMMENT '提交时间',
  `update_time` DATETIME NOT NULL COMMENT '更新时间',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_demand_no` (`demand_no`),
  KEY `idx_submitter_id` (`submitter_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='研发需求主表';

-- 3. 创建研发进度记录表
CREATE TABLE `rd_demand_progress` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `demand_id` INT NOT NULL COMMENT '需求ID',
  `status` TINYINT NOT NULL COMMENT '状态值',
  `status_text` VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '状态文本',
  `remark` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '进度备注',
  `operator_name` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '操作人',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_demand_id` (`demand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='研发需求进度记录表';

-- 4. 添加外键约束
ALTER TABLE `rd_demand_progress` 
ADD CONSTRAINT `fk_progress_demand` 
FOREIGN KEY (`demand_id`) REFERENCES `rd_demand` (`id`) ON DELETE CASCADE;
