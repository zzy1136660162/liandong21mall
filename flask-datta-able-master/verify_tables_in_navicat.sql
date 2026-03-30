-- 在Navicat中执行此SQL来验证表的存在
-- 请确保连接到 liandong21mall 数据库

-- 查看所有表
SHOW TABLES;

-- 查看成员1负责的表
SELECT 
    TABLE_NAME as '表名',
    TABLE_ROWS as '记录数',
    CREATE_TIME as '创建时间',
    UPDATE_TIME as '更新时间'
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'liandong21mall' 
AND TABLE_NAME IN (
    'sp_product_category',
    'sp_product', 
    'sp_product_sku',
    'sp_cart',
    'sp_order',
    'sp_order_item',
    'sp_address'
)
ORDER BY TABLE_NAME;

-- 查看商品分类表的数据
SELECT * FROM sp_product_category;

-- 查看商品表的数据（前5条）
SELECT id, product_name, price, stock, status FROM sp_product LIMIT 5;

-- 查看订单表的数据
SELECT id, order_no, user_id, total_amount, status, created_at FROM sp_order;