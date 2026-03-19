const { productApi, cartApi } = require('../../utils/api.js')

Page({
  data: {
    filterTabs: [
      { id: 0, name: '全部' },
      { id: 1, name: '护肤' },
      { id: 2, name: '彩妆' },
      { id: 3, name: '个护' },
      { id: 4, name: '食品' },
      { id: 5, name: '家居' }
    ],
    currentFilter: 0,
    products: [],
    loading: false,
    noMore: false,
    page: 1,
    pageSize: 10,
    cartCount: 0,
    searchKeyword: '',
    productScrollTop: 0,
    refreshing: false
  },

  lastScrollTime: 0,
  scrollThrottle: 50,

  async onLoad(options) {
    this.loadProducts()
    this.loadCartCount()
  },

  async loadProducts() {
    if (this.data.loading || this.data.noMore) return

    this.setData({ loading: true })

    try {
      let result
      const { currentFilter, page, pageSize, searchKeyword } = this.data

      if (searchKeyword) {
        result = await productApi.searchProducts(searchKeyword, page, pageSize)
      } else if (currentFilter === 0) {
        result = await productApi.getProducts({ page, pageSize })
      } else {
        result = await productApi.getProducts({ categoryId: currentFilter, page, pageSize })
      }
      
      const products = result.list || []
      
      if (products.length === 0) {
        this.setData({ noMore: true })
      } else {
        const newProducts = [...this.data.products, ...products]
        this.setData({
          products: newProducts,
          page: this.data.page + 1
        })
      }
    } catch (error) {
      console.error('加载商品失败:', error)
      wx.showToast({
        title: '加载失败',
        icon: 'none',
        duration: 2000
      })
    } finally {
      this.setData({ loading: false })
    }
  },

  switchFilter(e) {
    const filterId = e.currentTarget.dataset.id
    if (filterId === this.data.currentFilter) return

    this.setData({
      currentFilter: filterId,
      products: [],
      page: 1,
      noMore: false
    })

    this.loadProducts()
  },

  loadMore() {
    if (this.data.loading || this.data.noMore) return
    this.loadProducts()
  },

  goToDetail(e) {
    const productId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/Product_detail_page/Product_detail_page?id=${productId}`,
      success: () => {
        console.log('跳转到商品详情页成功')
      },
      fail: (err) => {
        console.error('跳转失败:', err)
        wx.showToast({
          title: '页面跳转失败',
          icon: 'none',
          duration: 2000
        })
      }
    })
  },

  toggleFavorite(e) {
    const productId = e.currentTarget.dataset.id
    const products = this.data.products.map(p => {
      if (p.productId === productId) {
        return { ...p, favorite: !p.favorite }
      }
      return p
    })
    
    this.setData({ products })
    
    const product = products.find(p => p.productId === productId)
    wx.showToast({
      title: product.favorite ? '已收藏' : '已取消收藏',
      icon: product.favorite ? 'success' : 'none',
      duration: 1500
    })
  },

  async addToCart(e) {
    const productId = e.currentTarget.dataset.id
    
    try {
      await cartApi.addToCart(productId, null, 1)
      wx.showToast({
        title: '已加入购物车',
        icon: 'success',
        duration: 1500
      })
      
      this.setData({
        cartCount: this.data.cartCount + 1
      })
    } catch (error) {
      console.error('加入购物车失败:', error)
    }
  },

  async loadCartCount() {
    try {
      const total = await cartApi.getCartTotal()
      this.setData({
        cartCount: Math.floor(total.total || 0)
      })
    } catch (error) {
      console.error('获取购物车数量失败:', error)
    }
  },

  goToCart() {
    wx.switchTab({
      url: '/pages/Cart_page/Cart_page',
      fail: () => {
        wx.navigateTo({
          url: '/pages/Cart_page/Cart_page'
        })
      }
    })
  },

  onSearch(e) {
    const keyword = e.detail.value
    this.setData({
      searchKeyword: keyword
    })
  },

  onSearchConfirm() {
    if (!this.data.searchKeyword.trim()) {
      wx.showToast({
        title: '请输入搜索关键词',
        icon: 'none',
        duration: 2000
      })
      return
    }
    
    this.setData({
      products: [],
      page: 1,
      noMore: false
    })
    
    this.loadProducts()
  },

  onPullDownRefresh() {
    this.setData({ refreshing: true })
    
    this.setData({
      products: [],
      page: 1,
      noMore: false
    })
    
    this.loadProducts().then(() => {
      this.setData({ refreshing: false })
    })
  },

  onReachBottom() {
    if (!this.data.noMore && !this.data.loading) {
      this.loadProducts()
    }
  },

  onShareAppMessage() {
    return {
      title: '精选好物，等你来选',
      path: '/pages/Product_list_page/Product_list_page',
      imageUrl: ''
    }
  },

  onTabChange(e) {
    const { activeTab } = e.detail
    const tabPaths = [
      '/pages/index/index',
      '/pages/Product_list_page/Product_list_page',
      '/pages/selection/selection',
      '/pages/rd/rd',
      '/pages/Profile_page/Profile_page'
    ]

    if (activeTab !== 1) {
      wx.switchTab({
        url: tabPaths[activeTab]
      })
    }
  },

  onShareTimeline() {
    return {
      title: '精选好物，等你来选',
      imageUrl: ''
    }
  }
})
