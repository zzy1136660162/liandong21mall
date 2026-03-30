// 商品商城搜索组件 - 淘宝风格
const { productApi } = require('../../utils/sp_api.js')

Component({
  properties: {
    placeholder: {
      type: String,
      value: '搜索商品'
    },
    showHistory: {
      type: Boolean,
      value: true
    },
    showHot: {
      type: Boolean,
      value: true
    }
  },

  data: {
    searchKey: '',
    suggestions: [],
    showSuggestions: false,
    showSearchPage: false,
    historyList: [],
    hotList: [],
    searching: false,
    isFocus: false
  },

  lifetimes: {
    attached() {
      this.loadHistory()
      this.loadHot()
    }
  },

  methods: {
    // 防抖搜索
    debounce: function(func, wait = 300) {
      let timeout = null
      return function(...args) {
        if (timeout) clearTimeout(timeout)
        timeout = setTimeout(() => {
          func.apply(this, args)
        }, wait)
      }
    },

    // 输入时触发
    onInput: function(e) {
      const value = e.detail.value
      this.setData({ searchKey: value })
      
      if (!value.trim()) {
        this.setData({
          suggestions: [],
          showSuggestions: false
        })
        return
      }
      
      // 防抖搜索
      this.debounceSearch(value)
    },

    // 执行搜索
    debounceSearch: function debounceSearch(value) {
      this.setData({
        showSuggestions: true,
        searching: true
      })

      productApi.searchProducts(value.trim(), 1, 10)
        .then(res => {
          const list = res.list || []
          this.setData({
            suggestions: list,
            searching: false
          })
        })
        .catch(err => {
          console.error('搜索失败:', err)
          this.setData({
            suggestions: [],
            searching: false
          })
        })
    },

    // 获取焦点
    onFocus: function(e) {
      this.setData({ isFocus: true })
      
      if (this.data.searchKey.trim()) {
        this.setData({ showSuggestions: true })
      } else {
        this.setData({ showSearchPage: true })
      }
    },

    // 失去焦点
    onBlur: function() {
      // 延迟关闭，给点击事件留出时间
      setTimeout(() => {
        this.setData({ isFocus: false })
      }, 200)
    },

    // 点击取消
    onCancel: function() {
      this.setData({
        searchKey: '',
        suggestions: [],
        showSuggestions: false,
        showSearchPage: false
      })
      this.triggerEvent('cancel')
    },

    // 点击清除
    onClear: function() {
      this.setData({
        searchKey: '',
        suggestions: [],
        showSuggestions: false
      })
    },

    // 确认搜索
    onConfirm: function(e) {
      const keyword = e.detail.value || this.data.searchKey
      if (!keyword.trim()) {
        wx.showToast({ title: '请输入关键词', icon: 'none' })
        return
      }
      
      this.saveHistory(keyword)
      this.setData({ showSuggestions: false, showSearchPage: false })
      this.triggerEvent('search', { keyword: keyword.trim() })
    },

    // 点击搜索按钮
    onSearchTap: function() {
      const keyword = this.data.searchKey.trim()
      if (!keyword) {
        wx.showToast({ title: '请输入关键词', icon: 'none' })
        return
      }
      
      this.saveHistory(keyword)
      this.setData({ showSuggestions: false, showSearchPage: false })
      this.triggerEvent('search', { keyword })
    },

    // 点击搜索建议
    onSuggestionTap: function(e) {
      const { id, name } = e.currentTarget.dataset
      const keyword = name || this.data.searchKey
      
      this.saveHistory(keyword)
      this.setData({ showSuggestions: false, showSearchPage: false })
      this.triggerEvent('select', { id, keyword })
      
      // 跳转到商品详情
      wx.navigateTo({
        url: `/pages/sp_Details/sp_Details?id=${id}`
      })
    },

    // 点击热门搜索
    onHotTap: function(e) {
      const { keyword } = e.currentTarget.dataset
      this.setData({
        searchKey: keyword,
        showSearchPage: false
      })
      this.saveHistory(keyword)
      this.triggerEvent('search', { keyword })
    },

    // 点击历史记录
    onHistoryTap: function(e) {
      const { keyword } = e.currentTarget.dataset
      this.setData({
        searchKey: keyword,
        showSearchPage: false
      })
      this.triggerEvent('search', { keyword })
    },

    // 删除单条历史
    onDeleteHistory: function(e) {
      const { keyword } = e.currentTarget.dataset
      let list = this.data.historyList
      list = list.filter(item => item !== keyword)
      this.setData({ historyList: list })
      wx.setStorageSync('sp_search_history', list)
    },

    // 清空历史
    onClearHistory: function() {
      wx.showModal({
        title: '提示',
        content: '确定清空搜索历史？',
        success: (res) => {
          if (res.confirm) {
            this.setData({ historyList: [] })
            wx.removeStorageSync('sp_search_history')
          }
        }
      })
    },

    // 保存到历史
    saveHistory: function(keyword) {
      if (!keyword.trim()) return
      
      let list = this.data.historyList
      // 去重
      list = list.filter(item => item !== keyword)
      // 头部插入
      list.unshift(keyword)
      // 限制数量
      if (list.length > 20) {
        list = list.slice(0, 20)
      }
      
      this.setData({ historyList: list })
      wx.setStorageSync('sp_search_history', list)
    },

    // 加载历史
    loadHistory: function() {
      const list = wx.getStorageSync('sp_search_history') || []
      this.setData({ historyList: list })
    },

    // 加载热门搜索
    loadHot: function() {
      const hotList = [
        '精华液', '面霜', '口红', '洁面乳', '防晒',
        '面膜', '眼霜', '化妆水', '气垫', '睫毛膏',
        '燕麦片', '洗衣液', '纸巾', '洗发水', '沐浴露'
      ]
      this.setData({ hotList })
    },

    // 关闭搜索页
    closeSearchPage: function() {
      this.setData({
        showSearchPage: false,
        showSuggestions: false
      })
    }
  }
})
