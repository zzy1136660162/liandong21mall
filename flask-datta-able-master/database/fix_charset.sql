-- 修复数据库字符集问题
-- 执行此脚本前请备份数据

-- 1. 修改数据库字符集
ALTER DATABASE liandong21mall CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. 修改表字符集
ALTER TABLE rd_demand CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE rd_demand_progress CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 3. 修改各字段字符集
ALTER TABLE rd_demand 
    MODIFY title VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '需求标题',
    MODIFY functional_appeal TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '功能诉求',
    MODIFY target_audience VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '目标人群',
    MODIFY dosage_form_preference VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '剂型偏好',
    MODIFY budget_range VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '预算范围',
    MODIFY remark TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '备注',
    MODIFY submitter_id VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '提交人ID',
    MODIFY submitter_name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '提交人姓名',
    MODIFY status_text VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '状态文本',
    MODIFY admin_remark TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '处理备注',
    MODIFY handler_name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '处理人';

ALTER TABLE rd_demand_progress
    MODIFY status_text VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '状态文本',
    MODIFY remark TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '进度备注',
    MODIFY operator_name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '操作人';

-- 4. 清空已有乱码数据（可选）
-- DELETE FROM rd_demand_progress;
-- DELETE FROM rd_demand;
