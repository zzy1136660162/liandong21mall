import pymysql

conn = pymysql.connect(
    host='101.126.90.255',
    port=63306,
    user='root',
    password='Gesoft9919.',
    database='liandong21mall',
    charset='utf8mb4'
)

cursor = conn.cursor()

sql = """
CREATE TABLE IF NOT EXISTS product_favorite (
  id bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '收藏ID',
  user_id bigint unsigned NOT NULL COMMENT '用户ID',
  product_id bigint unsigned NOT NULL COMMENT '商品ID',
  created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (id),
  UNIQUE KEY uk_user_product (user_id, product_id),
  KEY idx_user_id (user_id),
  KEY idx_product_id (product_id),
  KEY idx_created_at (created_at),
  CONSTRAINT fk_favorite_user FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE,
  CONSTRAINT fk_favorite_product FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品收藏表'
"""

cursor.execute(sql)
conn.commit()

print('Table product_favorite created successfully')

conn.close()
