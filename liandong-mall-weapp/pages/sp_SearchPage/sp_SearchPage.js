// 搜索页面 - sp_SearchPage
const { productApi } = require('../../utils/sp_api.js')

Page({
  data: {
    searchKey: '',
    historyList: [],
    hotList: [],
    suggestions: [],
    showSuggestions: false,
    searching: false
  },

  onLoad() {
    this.loadHistory()
    this.loadHot()
  },

  // 加载历史记录
  loadHistory() {
    const history = wx.getStorageSync('sp_search_history') || []
    this.setData({ historyList: history })
  },

  // 加载热门搜索
  loadHot() {
    const hotList = [
      { keyword: '精华液', hot: true },
      { keyword: '面霜', hot: true },
      { keyword: '口红', hot: true },
      { keyword: '洁面乳', hot: true },
      { keyword: '防晒', hot: true },
      { keyword: '面膜', hot: true },
      { keyword: '眼霜', hot: true },
      { keyword: '化妆水', hot: true },
      { keyword: '气垫', hot: true },
      { keyword: '燕麦片', hot: false },
      { keyword: '洗衣液', hot: false },
      { keyword: '纸巾', hot: false },
      { keyword: '洗发水', hot: false }
    ]
    this.setData({ hotList })
  },

  // 输入框输入
  onInput(e) {
    const value = e.detail.value
    this.setData({ searchKey: value })
    
    if (!value.trim()) {
      this.setData({
        suggestions: [],
        showSuggestions: false
      })
      return
    }

    // 防抖搜索建议
    clearTimeout(this.searchTimer)
    this.searchTimer = setTimeout(() => {
      this.loadSuggestions(value)
    }, 300)
  },

  // 加载搜索建议
  loadSuggestions(keyword) {
    if (!keyword.trim()) return

    this.setData({ searching: true })

    productApi.searchProducts(keyword.trim(), 1, 10)
      .then(res => {
        const list = res.list || []
        this.setData({
          suggestions: list,
          showSuggestions: true,
          searching: false
        })
      })
      .catch(err => {
        console.error('搜索建议失败:', err)
        this.setData({
          suggestions: [],
          searching: false
        })
      })
  },

  // 点击搜索按钮
  onSearch() {
    const keyword = this.data.searchKey.trim()
    if (!keyword) {
      wx.showToast({ title: '请输入搜索关键词', icon: 'none' })
      return
    }
    this.saveHistory(keyword)
    this.navigateToResult(keyword)
  },

  // 键盘确认搜索
  onConfirm(e) {
    const keyword = e.detail.value.trim()
    if (!keyword) {
      wx.showToast({ title: '请输入搜索关键词', icon: 'none' })
      return
    }
    this.saveHistory(keyword)
    this.navigateToResult(keyword)
  },

  // 点击建议项
  onSuggestionTap(e) {
    const { id, name } = e.currentTarget.dataset
    const keyword = name || this.data.searchKey
    this.saveHistory(keyword)
    this.navigateToResult(keyword)
  },

  // 点击热门搜索
  onHotTap(e) {
    const { keyword } = e.currentTarget.dataset
    this.setData({ searchKey: keyword })
    this.saveHistory(keyword)
    this.navigateToResult(keyword)
  },

  // 点击历史记录
  onHistoryTap(e) {
    const { keyword } = e.currentTarget.dataset
    this.setData({ searchKey: keyword })
    this.navigateToResult(keyword)
  },

  // 删除单条历史
  onDeleteHistory(e) {
    const { keyword } = e.currentTarget.dataset
    let list = this.data.historyList
    list = list.filter(item => item !== keyword)
    this.setData({ historyList: list })
    wx.setStorageSync('sp_search_history', list)
  },

  // 清空历史
  onClearHistory() {
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

  // 保存搜索历史
  saveHistory(keyword) {
    if (!keyword.trim()) return
    
    let list = this.data.historyList
    list = list.filter(item => item !== keyword)
    list.unshift(keyword)
    if (list.length > 20) list = list.slice(0, 20)
    
    this.setData({ historyList: list })
    wx.setStorageSync('sp_search_history', list)
  },

  // 跳转到搜索结果
  navigateToResult(keyword) {
    wx.navigateTo({
      url: `/pages/sp_SearchResult/sp_SearchResult?keyword=${encodeURIComponent(keyword)}`
    })
  }
})
