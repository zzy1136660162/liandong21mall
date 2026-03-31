# 商品商城搜索组件 - 使用说明

## 📦 组件概览

`sp_SearchBar` 是一个带防抖功能的商品搜索组件，专门为商品商城页面设计。

## ✨ 功能特点

1. **防抖搜索**
   - 300ms 防抖延迟
   - 减少不必要的 API 请求
   - 提升性能和用户体验

2. **实时搜索建议**
   - 输入时显示搜索建议
   - 显示商品名称和价格
   - 点击直接跳转到商品详情

3. **搜索历史**
   - 自动保存搜索历史
   - 本地存储，最长保存10条
   - 支持单条删除和全部清除

4. **事件触发**
   - `searchtap` - 点击搜索按钮
   - `confirm` - 键盘确认搜索
   - `suggestiontap` - 点击搜索建议
   - `historytap` - 点击历史记录
   - `clear` - 清除搜索内容
   - `cancel` - 取消搜索

## 📁 文件结构

```
liandong21mall/
└── liandong-mall-weapp/
    └── components/
        └── sp_SearchBar/                    # 搜索组件
            ├── sp_SearchBar.js            # 组件逻辑
            ├── sp_SearchBar.wxml           # 组件模板
            ├── sp_SearchBar.wxss          # 组件样式
            └── sp_SearchBar.json           # 组件配置
    
    └── pages/
        └── sp_Product_list/                # 商城页面
            ├── sp_Product_list.js          # 页面逻辑
            ├── sp_Product_list.wxml         # 页面模板
            ├── sp_Product_list.wxss         # 页面样式
            └── sp_Product_list.json         # 页面配置
```

## 🚀 快速使用

### 1. 在页面中使用搜索组件

```json
{
  "usingComponents": {
    "sp-searchbar": "/components/sp_SearchBar/sp_SearchBar"
  }
}
```

```xml
<sp-searchbar
  placeholder="搜索商品"
  historyKey="productSearchHistory"
  bind:searchtap="onSearch"
  bind:confirm="onSearchConfirm"
  bind:suggestiontap="onSuggestionTap"
  bind:historytap="onHistoryTap"
/>
```

### 2. 在页面中处理搜索事件

```javascript
Page({
  // 防抖搜索
  onSearch(e) {
    const keyword = e.detail.keyword
    // 执行搜索
    this.doSearch(keyword)
  },

  // 键盘确认
  onSearchConfirm(e) {
    const keyword = e.detail.keyword
    // 执行搜索
    this.doSearch(keyword)
  },

  // 点击建议项
  onSuggestionTap(e) {
    const { id, name } = e.detail
    wx.navigateTo({
      url: `/pages/sp_Details/sp_Details?id=${id}`
    })
  },

  // 点击历史记录
  onHistoryTap(e) {
    const { keyword } = e.detail
    this.doSearch(keyword)
  }
})
```

## 🔧 组件属性

| 属性名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| placeholder | String | '搜索商品' | 输入框占位文本 |
| searchKey | String | '' | 搜索关键词 |
| showHistory | Boolean | true | 是否显示历史记录 |
| historyKey | String | 'searchHistory' | 历史记录存储键名 |
| maxHistory | Number | 10 | 最大历史记录数 |

## 🎯 事件说明

| 事件名 | 参数 | 说明 |
|--------|------|------|
| searchtap | { keyword } | 点击搜索按钮 |
| confirm | { keyword } | 键盘确认搜索 |
| suggestiontap | { id, name } | 点击搜索建议项 |
| historytap | { keyword } | 点击历史记录项 |
| clear | - | 点击清除按钮 |
| cancel | - | 点击取消按钮 |

## 📝 防抖实现原理

```javascript
// 防抖函数
debounceSearch: function(func, wait = 300) {
  let timeout
  return function(...args) {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      func.apply(this, args)
    }, wait)
  }
},

// 使用防抖
onSearchInput: function(e) {
  const value = e.detail.value
  this.debounceSearch(this.doSearch, 300)()
}
```

## 🎨 样式定制

组件样式使用 BEM 命名规范，主要类名：

- `.sp-search-bar` - 根容器
- `.search-container` - 搜索框容器
- `.search-input-wrapper` - 输入框包装
- `.search-input` - 输入框
- `.suggestions-wrapper` - 建议列表容器
- `.suggestion-item` - 建议项
- `.history-wrapper` - 历史记录容器
- `.history-tag` - 历史标签

可以通过覆盖样式来自定义外观：

```css
/* 自定义搜索框样式 */
.search-input-wrapper {
  background-color: #f0f0f0;
  border-radius: 40rpx;
}

/* 自定义建议项样式 */
.suggestion-item {
  padding: 30rpx 0;
  border-bottom: 2rpx solid #eee;
}
```

## 📱 新建页面使用

如果需要在新的页面中使用搜索组件，可以按照以下步骤：

1. 创建页面文件（参考 `sp_Product_list` 目录）
2. 在页面的 `json` 配置中注册组件
3. 在 `wxml` 中使用组件
4. 在 `js` 中处理搜索事件

## 🔗 相关文件

- 组件文件：`components/sp_SearchBar/sp_SearchBar.*`
- 示例页面：`pages/sp_Product_list/sp_Product_list.*`
- API 接口：`utils/sp_api.js`

## ⚙️ 注意事项

1. **防抖时间**：默认 300ms，可根据实际需求调整
2. **历史记录**：存储在本地，使用 `wx.setStorageSync`
3. **API 调用**：需要配合搜索 API 使用
4. **样式覆盖**：避免使用 `!important`，使用更具体的选择器

## 🎉 示例效果

- 用户输入"精华"
- 300ms 后自动调用搜索 API
- 显示搜索建议列表
- 用户点击建议项或按确认键
- 保存到搜索历史
- 执行搜索并显示结果

## 📞 技术支持

如有问题，请查看：
- API 接口文档：`utils/sp_api.js`
- 商品列表页面示例：`pages/sp_Product_list/`
- 搜索组件源码：`components/sp_SearchBar/`

---

**版本**: 1.0.0  
**更新日期**: 2026-03-26  
**作者**: 商品商城模块
