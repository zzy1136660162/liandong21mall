// 搜索结果页面 - sp_SearchResult（单列卡片布局）
const { productApi, cartApi } = require('../../utils/sp_api.js')
const { getLoginStatus } = require('../../utils/sp_auth.js')

Page({
  data: {
    keyword: '',
    products: [],
    page: 1,
    pageSize: 10,
    hasMore: true,
    loading: false,
    isLoggedIn: false,
    cartCount: 0
  },

  onLoad(options) {
    const keyword = decodeURIComponent(options.keyword || '')
    this.setData({ keyword })
    
    const loginStatus = getLoginStatus()
    this.setData({ isLoggedIn: loginStatus.isLoggedIn })
    
    this.searchProducts()
    this.loadCartCount()
  },

  onShow() {
    const loginStatus = getLoginStatus()
    this.setData({ isLoggedIn: loginStatus.isLoggedIn })
    
    if (loginStatus.isLoggedIn) {
      this.loadCartCount()
    }
  },

  onPullDownRefresh() {
    this.refreshProducts()
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.loading) {
      this.loadMoreProducts()
    }
  },

  // 搜索商品
  searchProducts() {
    if (!this.data.keyword) return
    
    this.setData({ loading: true })
    
    productApi.searchProducts(this.data.keyword, this.data.page, this.data.pageSize)
      .then(res => {
        const products = res.list || []
        this.setData({
          products: this.data.page === 1 ? products : [...this.data.products, ...products],
          hasMore: products.length >= this.data.pageSize,
          loading: false
        })
      })
      .catch(err => {
        console.error('搜索失败:', err)
        wx.showToast({
          title: '搜索失败',
          icon: 'none'
        })
        this.setData({ loading: false })
      })
  },

  // 加载更多
  loadMoreProducts() {
    if (!this.data.hasMore || this.data.loading) return
    
    this.setData({ page: this.data.page + 1 })
    this.searchProducts()
  },

  // 刷新
  refreshProducts() {
    this.setData({
      products: [],
      page: 1,
      hasMore: true
    })
    this.searchProducts()
    wx.stopPullDownRefresh()
  },

  // 二次搜索
  onSearch(e) {
    const keyword = e.detail.value.trim()
    if (!keyword) {
      wx.showToast({ title: '请输入搜索关键词', icon: 'none' })
      return
    }
    
    this.setData({
      keyword,
      products: [],
      page: 1,
      hasMore: true
    })
    this.searchProducts()
  },

  // 加载购物车数量
  async loadCartCount() {
    try {
      const cartList = await cartApi.getCartList()
      this.setData({ cartCount: (cartList || []).length })
    } catch (error) {
      console.error('加载购物车失败:', error)
    }
  },

  // 跳转商品详情
  goToDetail(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/sp_Details/sp_Details?id=${id}`
    })
  },

  // 加入购物车
  async addToCart(e) {
    if (!this.data.isLoggedIn) {
      wx.showModal({
        title: '提示',
        content: '请先登录',
        confirmText: '去登录',
        success: (res) => {
          if (res.confirm) {
            wx.navigateTo({
              url: '/pages/login/index'
            })
          }
        }
      })
      return
    }

    const { id } = e.currentTarget.dataset
    try {
      await cartApi.addToCart(id, null, 1)
      wx.showToast({
        title: '加入成功',
        icon: 'success'
      })
      this.loadCartCount()
    } catch (error) {
      console.error('加入购物车失败:', error)
      wx.showToast({
        title: '加入失败',
        icon: 'none'
      })
    }
  },

  // 返回搜索页
  goBack() {
    wx.navigateBack()
  }
})
