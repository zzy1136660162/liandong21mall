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
      const result = await this.getCategoryProducts()
      
      if (result && result.products) {
        this.setData({
          products: [...this.data.products, ...result.products],
          page: this.data.page + 1,
          hasMore: result.products.length === this.data.pageSize,
          loading: false
        })
      } else {
        this.setData({
          loading: false,
          hasMore: false
        })
      }
    } catch (error) {
      this.setData({ loading: false })
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
    }
  },

  getCategoryProducts() {
    return new Promise((resolve, reject) => {
      wx.request({
        url: 'http://localhost:5000/api/sp/category/products',
        method: 'GET',
        data: {
          categoryId: this.data.categoryId,
          keyword: this.data.searchKeyword,
          sortType: this.data.sortType,
          sortOrder: this.data.sortOrder,
          page: this.data.page,
          pageSize: this.data.pageSize
        },
        success: (res) => {
          if (res.data.code === 200) {
            resolve(res.data.data)
          } else {
            wx.showToast({
              title: res.data.message || '获取商品失败',
              icon: 'none'
            })
            reject(res.data)
          }
        },
        fail: (err) => {
          wx.showToast({
            title: '网络请求失败',
            icon: 'none'
          })
          reject(err)
        }
      })
    })
  },

  onReachBottom() {
    this.loadProducts()
  },

  goToProductDetail(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/sp_Details/sp_Details?id=${id}`
    })
  },

  goBack() {
    wx.navigateBack()
  }
})