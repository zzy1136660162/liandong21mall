Page({
  data: {
    categoryId: '',
    categoryName: '',
    searchKeyword: '',
    sortType: '',
    sortOrder: '',
    products: [],
    loading: false,
    hasMore: true,
    page: 1,
    pageSize: 10
  },

  onLoad(options) {
    const { categoryId, categoryName } = options
    this.setData({
      categoryId,
      categoryName
    })
    if (categoryName) {
      wx.setNavigationBarTitle({
        title: categoryName
      })
    }
    this.loadProducts()
  },

  onSearchInput(e) {
    this.setData({
      searchKeyword: e.detail.value
    })
  },

  onSearch() {
    this.setData({
      page: 1,
      products: []
    })
    this.loadProducts()
  },

  onSortChange(e) {
    const { type } = e.currentTarget.dataset
    let { sortType, sortOrder } = this.data
    
    if (sortType === type) {
      sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'
    } else {
      sortType = type
      sortOrder = 'desc'
    }
    
    this.setData({
      sortType,
      sortOrder,
      page: 1,
      products: []
    })
    this.loadProducts()
  },

  async loadProducts() {
    if (this.data.loading || !this.data.hasMore) return
    
    this.setData({ loading: true })
    
    try {
      // 模拟加载商品数据
      const mockProducts = this.getMockProducts()
      
      this.setData({
        products: [...this.data.products, ...mockProducts],
        page: this.data.page + 1,
        hasMore: mockProducts.length === this.data.pageSize,
        loading: false
      })
    } catch (error) {
      this.setData({ loading: false })
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
    }
  },

  getMockProducts() {
    // 模拟商品数据
    const baseProducts = [
      { id: 1, name: '陀谷堂·酸枣仁小丸子（新老包装随机发）', price: '59.90', image: 'https://picsum.photos/300/300?random=1' },
      { id: 2, name: '龍耀·肚脐丸', price: '29.90', image: 'https://picsum.photos/300/300?random=2' },
      { id: 3, name: '龍耀·植物硒蛋白肽', price: '99.00', image: 'https://picsum.photos/300/300?random=3' },
      { id: 4, name: '陀谷堂·赶黄草', price: '98.00', image: 'https://picsum.photos/300/300?random=4' },
      { id: 5, name: '养生堂·维生素C', price: '45.00', image: 'https://picsum.photos/300/300?random=5' },
      { id: 6, name: '同仁堂·阿胶糕', price: '128.00', image: 'https://picsum.photos/300/300?random=6' }
    ]
    return baseProducts
  },

  onReachBottom() {
    this.loadProducts()
  },

  goToProductDetail(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/product-detail/product-detail?id=${id}`
    })
  },

  goBack() {
    wx.navigateBack()
  }
})