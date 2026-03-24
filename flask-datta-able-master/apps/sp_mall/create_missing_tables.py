# -*- encoding: utf-8 -*-
"""
检查并创建缺失的数据库表
"""

import pymysql

# 数据库配置
DB_CONFIG = {
    'host': '101.126.90.255',
    'port': 63306,
    'user': 'root',
    'password': 'Gesoft9919.',
    'database': 'liandong21mall',
    'charset': 'utf8mb4'
}

def check_and_create_tables():
    """检查并创建缺失的表"""
    
    connection = pymysql.connect(**DB_CONFIG)
    
    try:
        with connection.cursor() as cursor:
            # 检查 sp_product 表是否存在
            cursor.execute("SHOW TABLES LIKE 'sp_product'")
            if not cursor.fetchone():
                print('创建 sp_product 表...')
                create_product_table = """
                CREATE TABLE `sp_product` (
                  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '商品ID',
                  `category_id` int(11) NOT NULL COMMENT '分类ID',
                  `product_name` varchar(200) NOT NULL COMMENT '商品名称',
                  `product_code` varchar(50) NOT NULL COMMENT '商品编码',
                  `main_image` varchar(500) NOT NULL COMMENT '主图URL',
                  `images` json DEFAULT NULL COMMENT '商品图片列表JSON',
                  `price` decimal(10,2) NOT NULL COMMENT '销售价格',
                  `original_price` decimal(10,2) DEFAULT NULL COMMENT '原价',
                  `member_price` decimal(10,2) DEFAULT NULL COMMENT '会员价',
                  `stock` int(11) NOT NULL DEFAULT '0' COMMENT '库存数量',
                  `sales` int(11) NOT NULL DEFAULT '0' COMMENT '销量',
                  `brief` varchar(500) DEFAULT NULL COMMENT '商品简介',
                  `description` text COMMENT '商品详情HTML',
                  `status` smallint(6) NOT NULL DEFAULT '1' COMMENT '状态：1上架 0下架',
                  `is_hot` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否热销：1是 0否',
                  `is_new` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否新品：1是 0否',
                  `is_recommend` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否推荐：1是 0否',
                  `sort` int(11) NOT NULL DEFAULT '0' COMMENT '排序',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                  PRIMARY KEY (`id`),
                  UNIQUE KEY `uk_product_code` (`product_code`),
                  KEY `idx_category_id` (`category_id`),
                  KEY `idx_status` (`status`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品表'
                """
                cursor.execute(create_product_table)
                print('✓ sp_product 表创建成功')
            else:
                print('✓ sp_product 表已存在')
            
            # 检查 sp_product_sku 表是否存在
            cursor.execute("SHOW TABLES LIKE 'sp_product_sku'")
            if not cursor.fetchone():
                print('创建 sp_product_sku 表...')
                create_sku_table = """
                CREATE TABLE `sp_product_sku` (
                  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'SKU ID',
                  `product_id` bigint(20) NOT NULL COMMENT '商品ID',
                  `sku_code` varchar(50) NOT NULL COMMENT 'SKU编码',
                  `sku_name` varchar(100) NOT NULL COMMENT 'SKU名称',
                  `spec` json DEFAULT NULL COMMENT '规格属性JSON',
                  `price` decimal(10,2) NOT NULL COMMENT 'SKU价格',
                  `original_price` decimal(10,2) DEFAULT NULL COMMENT 'SKU原价',
                  `member_price` decimal(10,2) DEFAULT NULL COMMENT 'SKU会员价',
                  `stock` int(11) NOT NULL DEFAULT '0' COMMENT 'SKU库存',
                  `image` varchar(500) DEFAULT NULL COMMENT 'SKU图片',
                  `status` smallint(6) NOT NULL DEFAULT '1' COMMENT '状态：1启用 0禁用',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                  PRIMARY KEY (`id`),
                  UNIQUE KEY `uk_sku_code` (`sku_code`),
                  KEY `idx_product_id` (`product_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品SKU表'
                """
                cursor.execute(create_sku_table)
                print('✓ sp_product_sku 表创建成功')
            else:
                print('✓ sp_product_sku 表已存在')
            
            # 检查 sp_cart 表是否存在
            cursor.execute("SHOW TABLES LIKE 'sp_cart'")
            if not cursor.fetchone():
                print('创建 sp_cart 表...')
                create_cart_table = """
                CREATE TABLE `sp_cart` (
                  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '购物车ID',
                  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
                  `product_id` bigint(20) NOT NULL COMMENT '商品ID',
                  `sku_id` bigint(20) DEFAULT NULL COMMENT 'SKU ID',
                  `quantity` int(11) NOT NULL DEFAULT '1' COMMENT '数量',
                  `selected` smallint(6) NOT NULL DEFAULT '1' COMMENT '是否选中：1是 0否',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                  PRIMARY KEY (`id`),
                  KEY `idx_user_id` (`user_id`),
                  KEY `idx_product_id` (`product_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='购物车表'
                """
                cursor.execute(create_cart_table)
                print('✓ sp_cart 表创建成功')
            else:
                print('✓ sp_cart 表已存在')
            
            connection.commit()
            print('\n✓ 所有表检查完成！')
            
    except Exception as e:
        print(f'✗ 操作失败: {e}')
        connection.rollback()
    finally:
        connection.close()

if __name__ == '__main__':
    check_and_create_tables()
