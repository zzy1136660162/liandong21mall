#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql

conn = pymysql.connect(
    host='101.126.90.255',
    port=63306,
    user='root',
    password='Gesoft9919.',
    database='liandong21mall',
    charset='utf8mb4'
)

try:
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, demand_no, title, submitter_id, submitter_name, status_text, submit_time FROM rd_demand ORDER BY id DESC")
        results = cursor.fetchall()
        print(f"共 {len(results)} 条数据:\n")
        for row in results:
            print(f"ID:{row[0]} | 编号:{row[1]} | 标题:{row[2]} | 提交人ID:{row[3]} | 姓名:{row[4]} | 状态:{row[5]} | 时间:{row[6]}")
finally:
    conn.close()
