# 自定义 Tab 组件使用说明

## 组件位置
`/components/custom-tab/`

## 功能特性
- ✅ 五个标签页：首页、商城、选品、研发、我的
- ✅ 自定义图标（选中/未选中状态）
- ✅ 支持角标显示（购物车数量等）
- ✅ 点击反馈动画
- ✅ 适配安全区域（iPhone X+）
- ✅ 极简设计风格

## 快速开始

### 1. 在页面 JSON 中引入组件

```json
{
  "usingComponents": {
    "custom-tab": "/components/custom-tab/custom-tab"
  }
}
```

### 2. 在页面 WXML 中使用组件

```xml
<custom-tab 
  activeTab="{{activeTab}}" 
  bindtabchange="onTabChange"
/>
```

### 3. 在页面 JS 中处理逻辑

```javascript
Page({
  data: {
    activeTab: 0
  },

  onLoad(options) {
    const pages = getCurrentPages()
    const currentPage = pages[pages.length - 1]
    const route = currentPage.route

    const tabMap = {
      'pages/index/index': 0,
      'pages/Product_list_page/Product_list_page': 1,
      'pages/selection/selection': 2,
      'pages/rd/rd': 3,
      'pages/Profile_page/Profile_page': 4
    }

    this.setData({
      activeTab: tabMap[route] || 0
    })
  },

  onTabChange(e) {
    const { activeTab } = e.detail
    this.setData({ activeTab })
  }
})
```

## 组件属性

| 属性名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| activeTab | Number | 0 | 当前选中的标签页索引 |

## 组件事件

| 事件名 | 说明 | 返回参数 |
|--------|------|----------|
| tabchange | 标签页切换时触发 | { activeTab: Number } |

## 组件方法

### updateBadge(tabId, count)
更新指定标签页的角标数量

```javascript
const tabComponent = this.selectComponent('#customTab')
tabComponent.updateBadge(1, 5) // 更新商城标签的角标为 5
```

### setActiveTab(tabId)
设置当前选中的标签页

```javascript
const tabComponent = this.selectComponent('#customTab')
tabComponent.setActiveTab(0) // 设置首页为选中状态
```

## 标签页配置

| 索引 | 名称 | 路径 |
|------|------|------|
| 0 | 首页 | /pages/index/index |
| 1 | 商城 | /pages/Product_list_page/Product_list_page |
| 2 | 选品 | /pages/selection/selection |
| 3 | 研发 | /pages/rd/rd |
| 4 | 我的 | /pages/Profile_page/Profile_page |

## 图标配置

图标文件位于 `/images/tab/` 目录下：

- 首页：`首页（未选中）.png` / `首页 (选中).png`
- 商城：`商城 (未选中).png` / `商城（选中）.png`
- 选品：`选品 (未选中).png` / `选品（选中）.png`
- 研发：`研发 (未选中).png` / `研发（选中）.png`
- 我的：`我的 (未选中).png` / `我的 (选中).png`

## 样式自定义

组件使用极简设计风格，主要样式包括：

- **背景色**：#FFFFFF
- **选中文字**：#1A1A1A，font-weight: 600
- **未选中文字**：#999999，font-weight: 400
- **角标颜色**：#FF6B6B
- **高度**：100rpx + 安全区域

如需自定义样式，可以修改 `custom-tab.wxss` 文件。

## 注意事项

1. 确保图标文件路径正确
2. 建议在 app.json 中配置 tabBar，使用 switchTab 进行页面切换
3. 组件会自动适配 iPhone X+ 的安全区域
4. 角标数量超过 99 时会显示为 "99+"

## 示例页面

完整示例请参考：`/pages/demo-tab/demo-tab`
