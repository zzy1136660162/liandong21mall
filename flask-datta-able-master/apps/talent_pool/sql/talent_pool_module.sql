-- 人才库模块建表SQL
-- 执行方式: mysql -u username -p database_name < talent_pool_module.sql

-- 创建人才库表
CREATE TABLE IF NOT EXISTS `talent_pool` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` VARCHAR(50) NOT NULL COMMENT '姓名',
  `avatar` VARCHAR(500) DEFAULT NULL COMMENT '头像URL',
  `title` VARCHAR(100) NOT NULL COMMENT '职称/职位',
  `region` VARCHAR(100) DEFAULT NULL COMMENT '所在地区',
  `expertise_areas` TEXT COMMENT '专长领域（JSON数组）',
  `skills` TEXT COMMENT '专业技能（JSON数组）',
  `experience_years` INT DEFAULT NULL COMMENT '从业年限',
  `education` VARCHAR(50) DEFAULT NULL COMMENT '学历',
  `intro` TEXT COMMENT '个人简介',
  `project_experience` TEXT COMMENT '项目经验（JSON数组）',
  `achievements` TEXT COMMENT '成果荣誉（JSON数组）',
  `status` TINYINT NOT NULL DEFAULT 1 COMMENT '状态：0-隐藏 1-显示',
  `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序权重',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`),
  KEY `idx_sort_order` (`sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='人才库表';
