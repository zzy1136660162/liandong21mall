-- 研发需求模块数据库表
-- 创建时间: 2024-03-16

-- 研发需求主表
CREATE TABLE IF NOT EXISTS `rd_demand` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `demand_no` VARCHAR(50) NOT NULL COMMENT '需求编号',
  `title` VARCHAR(200) NOT NULL COMMENT '需求标题',
  `functional_appeal` TEXT NOT NULL COMMENT '功能诉求',
  `target_audience` VARCHAR(200) NOT NULL COMMENT '目标人群',
  `dosage_form_preference` VARCHAR(100) DEFAULT NULL COMMENT '剂型偏好',
  `budget_range` VARCHAR(50) NOT NULL COMMENT '预算范围',
  `expected_delivery_time` DATE NOT NULL COMMENT '期望交付时间',
  `remark` TEXT DEFAULT NULL COMMENT '备注',
  `submitter_id` VARCHAR(50) NOT NULL COMMENT '提交人ID',
  `submitter_name` VARCHAR(50) DEFAULT NULL COMMENT '提交人姓名',
  `submitter_phone` VARCHAR(20) DEFAULT NULL COMMENT '提交人电话',
  `status` TINYINT NOT NULL DEFAULT '0' COMMENT '状态: 0-待处理 1-确认中 2-研发中 3-样品制作 4-已完成 5-已取消',
  `status_text` VARCHAR(20) NOT NULL COMMENT '状态文本',
  `admin_remark` TEXT DEFAULT NULL COMMENT '处理备注',
  `handler_name` VARCHAR(50) DEFAULT NULL COMMENT '处理人',
  `submit_time` DATETIME NOT NULL COMMENT '提交时间',
  `update_time` DATETIME NOT NULL COMMENT '更新时间',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_demand_no` (`demand_no`),
  KEY `idx_submitter_id` (`submitter_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='研发需求主表';

-- 研发进度记录表
CREATE TABLE IF NOT EXISTS `rd_demand_progress` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `demand_id` INT NOT NULL COMMENT '需求ID',
  `status` TINYINT NOT NULL COMMENT '状态值',
  `status_text` VARCHAR(20) NOT NULL COMMENT '状态文本',
  `remark` TEXT DEFAULT NULL COMMENT '进度备注',
  `operator_name` VARCHAR(50) DEFAULT NULL COMMENT '操作人',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_demand_id` (`demand_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='研发需求进度记录表';

-- 初始化数据：插入一条测试需求
INSERT INTO `rd_demand` (
  `demand_no`, `title`, `functional_appeal`, `target_audience`,
  `dosage_form_preference`, `budget_range`, `expected_delivery_time`,
  `remark`, `submitter_id`, `submitter_name`, `submitter_phone`,
  `status`, `status_text`, `submit_time`, `update_time`
) VALUES (
  'RD202403160001', '测试需求', '希望开发一款女性护肤产品', '25-40岁女性',
  '精华液', '100000-200000', '2024-06-01',
  '这是一个测试需求', 'USER_TEST001', '张三', '13800138000',
  0, '待处理', NOW(), NOW()
);

-- 初始化进度记录
INSERT INTO `rd_demand_progress` (
  `demand_id`, `status`, `status_text`, `remark`, `operator_name`, `create_time`
) VALUES (
  1, 0, '待处理', '需求已提交', '系统', NOW()
);
