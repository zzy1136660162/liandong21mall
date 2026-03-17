Page({
  data: {
    categories: [
      { id: 1, name: '全部', count: 0 },
      { id: 2, name: '护肤', count: 0 },
      { id: 3, name: '彩妆', count: 0 },
      { id: 4, name: '个护', count: 0 },
      { id: 5, name: '香水', count: 0 },
      { id: 6, name: '工具', count: 0 },
      { id: 7, name: '套装', count: 0 },
      { id: 8, name: '新品', count: 0 }
    ],
    currentCategory: 1,
    products: [],
    loading: false,
    noMore: false,
    page: 1,
    pageSize: 10,
    scrollTop: 0,
    showBackToTop: false,
    scrollThreshold: 500,
    cartCount: 0,
    showQuickActions: true,
    searchKeyword: ''
  },

  lastScrollTime: 0,
  scrollThrottle: 100,

  onLoad(options) {
    this.loadProducts()
    this.loadCartCount()
  },

  onShow() {
    this.setData({
      scrollTop: 0
    })
    this.loadCartCount()
  },

  switchCategory(e) {
    const categoryId = e.currentTarget.dataset.id
    if (categoryId === this.data.currentCategory) return

    this.setData({
      currentCategory: categoryId,
      products: [],
      page: 1,
      noMore: false
    })

    this.loadProducts()
  },

  async loadProducts() {
    if (this.data.loading || this.data.noMore) return

    this.setData({ loading: true })

    try {
      const products = await this.fetchProducts()
      
      if (products.length === 0) {
        this.setData({ noMore: true })
      } else {
        this.setData({
          products: [...this.data.products, ...products],
          page: this.data.page + 1
        })
      }
      
      this.updateCategoryCounts()
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

  fetchProducts() {
    return new Promise((resolve) => {
      setTimeout(() => {
        const mockProducts = this.generateMockProducts()
        resolve(mockProducts)
      }, 400)
    })
  },

  generateMockProducts() {
    const categoryNames = ['护肤', '彩妆', '个护', '香水', '工具', '套装', '新品']
    const productNames = [
      '精华液', '面膜', '洁面乳', '爽肤水', '乳液', '面霜', '眼霜', '防晒霜',
      '口红', '粉底液', '眼影盘', '眉笔', '睫毛膏', '腮红', '散粉', '修容',
      '洗发水', '护发素', '沐浴露', '身体乳', '护手霜', '唇膏', '指甲油', '香水'
    ]
    
    const badges = ['热销', '新品', '特价', '限量', '推荐']
    const tags = [['包邮'], ['正品'], ['热卖'], ['新品'], ['特价'], ['包邮', '正品']]

    return Array.from({ length: 6 }, (_, i) => {
      const randomIndex = Math.floor(Math.random() * productNames.length)
      const randomBadge = Math.random() > 0.6 ? badges[Math.floor(Math.random() * badges.length)] : ''
      const randomTags = tags[Math.floor(Math.random() * tags.length)]
      const randomSales = Math.floor(Math.random() * 10000)
      
      return {
        id: this.data.products.length + i + 1,
        name: `${categoryNames[Math.floor(Math.random() * categoryNames.length)]}${productNames[randomIndex]}`,
        desc: '精选优质原料，温和配方，适合各种肌肤类型',
        price: (Math.random() * 500 + 50).toFixed(2),
        originalPrice: Math.random() > 0.5 ? (Math.random() * 600 + 100).toFixed(2) : '',
        image: `https://via.placeholder.com/300x300/FFF9E6/FFB300?text=Product${this.data.products.length + i + 1}`,
        badge: randomBadge,
        tags: randomTags,
        sales: randomSales,
        favorite: false
      }
    })
  },

  updateCategoryCounts() {
    const categories = this.data.categories.map(cat => {
      if (cat.id === 1) {
        return { ...cat, count: this.data.products.length }
      }
      const count = this.data.products.filter(p => p.name.includes(cat.name)).length
      return { ...cat, count }
    })
    this.setData({ categories })
  },

  loadMore() {
    this.loadProducts()
  },

  onScroll(e) {
    const now = Date.now()
    if (now - this.lastScrollTime < this.scrollThrottle) {
      return
    }
    this.lastScrollTime = now
    
    const scrollTop = e.detail.scrollTop
    const showBackToTop = scrollTop > this.data.scrollThreshold
    
    if (showBackToTop !== this.data.showBackToTop) {
      this.setData({ showBackToTop })
    }
  },

  scrollToTop() {
    this.setData({
      scrollTop: 0
    })
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
      if (p.id === productId) {
        return { ...p, favorite: !p.favorite }
      }
      return p
    })
    
    this.setData({ products })
    
    const product = products.find(p => p.id === productId)
    wx.showToast({
      title: product.favorite ? '已收藏' : '已取消收藏',
      icon: product.favorite ? 'success' : 'none',
      duration: 1500
    })
  },

  addToCart(e) {
    const productId = e.currentTarget.dataset.id
    
    wx.showToast({
      title: '已加入购物车',
      icon: 'success',
      duration: 1500
    })
    
    this.setData({
      cartCount: this.data.cartCount + 1
    })
  },

  loadCartCount() {
    this.setData({
      cartCount: Math.floor(Math.random() * 10)
    })
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

  goToHome() {
    wx.switchTab({
      url: '/pages/index/index',
      fail: () => {
        wx.navigateBack({
          delta: 1
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
    
    wx.showLoading({
      title: '搜索中...'
    })
    
    setTimeout(() => {
      wx.hideLoading()
      this.loadProducts()
    }, 400)
  },

  onPullDownRefresh() {
    this.setData({
      products: [],
      page: 1,
      noMore: false
    })
    
    this.loadProducts().then(() => {
      wx.stopPullDownRefresh()
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

  onShareTimeline() {
    return {
      title: '精选好物，等你来选',
      imageUrl: ''
    }
  }
})