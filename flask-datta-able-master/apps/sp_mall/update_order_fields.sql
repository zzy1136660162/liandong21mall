-- 为sp_order表添加缺失的字段
-- 执行前请先备份数据库

USE liandong21mall;

-- 检查并添加 payment_method 字段
ALTER TABLE sp_order ADD COLUMN IF NOT EXISTS payment_method VARCHAR(50) DEFAULT 'WECHAT_PAY' COMMENT '支付方式' AFTER pay_time;

-- 检查并添加 logistics_company 字段
ALTER TABLE sp_order ADD COLUMN IF NOT EXISTS logistics_company VARCHAR(100) COMMENT '物流公司' AFTER payment_method;

-- 检查并添加 logistics_no 字段
ALTER TABLE sp_order ADD COLUMN IF NOT EXISTS logistics_no VARCHAR(100) COMMENT '物流单号' AFTER logistics_company;

-- 检查并添加 invoice_type 字段
ALTER TABLE sp_order ADD COLUMN IF NOT EXISTS invoice_type VARCHAR(20) DEFAULT 'NONE' COMMENT '发票类型' AFTER logistics_no;

-- 检查并添加 invoice_title 字段
ALTER TABLE sp_order ADD COLUMN IF NOT EXISTS invoice_title VARCHAR(200) COMMENT '发票抬头' AFTER invoice_type;

-- 检查并添加 order_source 字段
ALTER TABLE sp_order ADD COLUMN IF NOT EXISTS order_source VARCHAR(20) DEFAULT 'MINIPROGRAM' COMMENT '订单来源' AFTER invoice_title;

-- 检查并添加 coupon_id 字段
ALTER TABLE sp_order ADD COLUMN IF NOT EXISTS coupon_id INT COMMENT '优惠券ID' AFTER order_source;

-- 检查并添加 coupon_amount 字段
ALTER TABLE sp_order ADD COLUMN IF NOT EXISTS coupon_amount DECIMAL(10,2) DEFAULT 0.00 COMMENT '优惠券金额' AFTER coupon_id;

-- 添加索引
ALTER TABLE sp_order ADD INDEX idx_user_id (user_id);
ALTER TABLE sp_order ADD INDEX idx_status (status);
ALTER TABLE sp_order ADD INDEX idx_order_no (order_no);
ALTER TABLE sp_order ADD INDEX idx_user_status (user_id, status);

SELECT '订单表字段更新完成!' AS result;
