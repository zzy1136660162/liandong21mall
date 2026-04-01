# 商品订单管理模块 (sp_mall_admin)

## 模块概述

本模块负责商品商城的后台管理功能，包括：
- 商品分类管理
- 商品管理（增删改查、上下架）
- 订单管理（查看、处理、发货）

## 文件结构

```
apps/sp_mall_admin/
├── __init__.py                 # 蓝图初始化
├── routes.py                   # 后台管理路由
├── init_data.py                # 数据初始化脚本
└── sql/
    └── sp_admin_module.sql     # SQL测试数据
```

## 模板文件

```
apps/templates/sp_mall_admin/
├── sp_category_list.html       # 分类管理页面
├── sp_product_list.html       # 商品管理页面
├── sp_order_list.html         # 订单列表页面
└── sp_order_detail.html       # 订单详情页面
```

## 路由说明

| 路由 | 方法 | 功能 |
|------|------|------|
| /admin/sp/category | GET | 分类列表页 |
| /admin/sp/category/add | POST | 添加分类 |
| /admin/sp/category/<id> | GET | 获取分类详情 |
| /admin/sp/category/<id> | PUT | 更新分类 |
| /admin/sp/category/<id> | DELETE | 删除分类 |
| /admin/sp/product | GET | 商品列表页 |
| /admin/sp/product/add | POST | 添加商品 |
| /admin/sp/product/<id> | GET | 获取商品详情 |
| /admin/sp/product/<id> | PUT | 更新商品 |
| /admin/sp/product/<id> | DELETE | 删除商品 |
| /admin/sp/product/toggle-status/<id> | POST | 切换商品上下架状态 |
| /admin/sp/order | GET | 订单列表页 |
| /admin/sp/order/<id> | GET | 订单详情页 |
| /admin/sp/order/<id>/ship | POST | 订单发货 |
| /admin/sp/order/<id>/finish | POST | 订单完成 |
| /admin/sp/order/<id>/cancel | POST | 取消订单 |

## 数据表

本模块使用以下数据表（已存在于 sp_mall 模块）：
- `sp_product_category` - 商品分类表
- `sp_product` - 商品表
- `sp_product_sku` - 商品SKU表
- `sp_order` - 订单表
- `sp_order_item` - 订单明细表

## 初始化数据

### 方法1：使用Python脚本（推荐）

```bash
cd d:\develop\小程序文件\实战项目\电商小程序\liandong21mall\flask-datta-able-master
python apps/sp_mall_admin/init_data.py
```

### 方法2：执行SQL文件

```bash
mysql -u username -p database_name < apps/sp_mall_admin/sql/sp_admin_module.sql
```

## 使用说明

### 1. 启动应用

```bash
cd d:\develop\小程序文件\实战项目\电商小程序\liandong21mall\flask-datta-able-master
python run.py
```

### 2. 访问后台管理

在浏览器中访问：
- 商品分类管理：http://localhost:5000/admin/sp/category
- 商品管理：http://localhost:5000/admin/sp/product
- 订单管理：http://localhost:5000/admin/sp/order

## 功能特性

### 商品分类管理
- 查看所有分类
- 添加新分类
- 编辑分类信息
- 启用/禁用分类
- 删除分类（需确保无关联商品）

### 商品管理
- 商品列表展示（支持分页、筛选）
- 按分类、状态、关键词搜索
- 添加新商品
- 编辑商品信息
- 上下架切换
- 删除商品
- 支持商品标签（热销、新品、推荐）

### 订单管理
- 订单列表展示（支持状态筛选、关键词搜索）
- 查看订单详情
- 订单发货（填写物流信息）
- 订单完成
- 订单取消（自动退还库存）

## 注意事项

1. **数据库依赖**：确保 `sp_product_category`、`sp_product`、`sp_order`、`sp_order_item` 表已创建
2. **数据隔离**：本模块使用 `sp_` 前缀的表，与其他模块隔离
3. **文件命名**：所有新文件使用 `sp_` 前缀，避免与原文件冲突
4. **模板继承**：使用独立的 `sp_base.html` 基础模板，不影响原有页面

## 更新日志

### 2024-01-01
- 初始版本
- 实现商品分类管理
- 实现商品管理（CRUD + 上下架）
- 实现订单管理（列表、详情、发货）
