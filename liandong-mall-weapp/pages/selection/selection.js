Page({
  data: {
    currentFilter: 0,
    filterTabs: [
      { id: 0, name: '全部' },
      { id: 1, name: '热门' },
      { id: 2, name: '新品' },
      { id: 3, name: '推荐' }
    ],
    currentFilterName: '全部',
    products: [],
    loading: false,
    noMore: false,
    page: 1,
    pageSize: 10
  },

  onLoad(options) {
    this.loadProducts()
  },

  switchFilter(e) {
    const filterId = e.currentTarget.dataset.id
    if (filterId === this.data.currentFilter) return

    const filterName = this.data.filterTabs.find(tab => tab.id === filterId).name

    this.setData({
      currentFilter: filterId,
      currentFilterName: filterName,
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
      const mockProducts = this.getMockProducts()
      
      if (mockProducts.length === 0) {
        this.setData({ noMore: true })
      } else {
        const newProducts = [...this.data.products, ...mockProducts]
        this.setData({
          products: newProducts,
          page: this.data.page + 1
        })
      }
    } catch (error) {
      console.error('加载商品失败:', error)
    } finally {
      this.setData({ loading: false })
    }
  },

  getMockProducts() {
    const products = []
    for (let i = 0; i < 10; i++) {
      products.push({
        id: Date.now() + i,
        name: `精选优质商品示例 ${this.data.products.length + i + 1}`,
        price: (Math.random() * 500 + 50).toFixed(2),
        image: '/images/placeholder.png',
        sales: Math.floor(Math.random() * 1000),
        stock: Math.floor(Math.random() * 100),
        isHot: Math.random() > 0.7,
        isNew: Math.random() > 0.8,
        favorite: false
      })
    }
    return products
  },

  goToDetail(e) {
    const productId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/sp_Details/sp_Details?id=${productId}`,
      fail: () => {
        wx.showToast({
          title: '页面跳转失败',
          icon: 'none'
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
  },

  viewMore() {
    wx.showToast({
      title: '查看全部',
      icon: 'none'
    })
  },

  onReachBottom() {
    if (!this.data.noMore && !this.data.loading) {
      this.loadProducts()
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

    if (activeTab !== 2) {
      wx.switchTab({
        url: tabPaths[activeTab]
      })
    }
  }
})
