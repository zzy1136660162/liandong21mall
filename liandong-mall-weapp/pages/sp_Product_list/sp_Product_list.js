// 商品商城页面 - 淘宝风格搜索
const { productApi, cartApi } = require('../../utils/sp_api.js')
const { getLoginStatus } = require('../../utils/sp_auth.js')

Page({
  data: {
    // 搜索相关
    searchKeyword: '',
    
    // 分类
    categories: [],
    currentCategoryId: 0,
    
    // 筛选排序
    filters: [
      { id: 0, name: '综合' },
      { id: 1, name: '销量' },
      { id: 2, name: '价格升' },
      { id: 3, name: '价格降' }
    ],
    currentFilterId: 0,
    
    // 商品列表
    products: [],
    page: 1,
    pageSize: 20,
    hasMore: true,
    loading: false,
    
    // 购物车
    cartCount: 0,
    
    // 登录状态
    isLoggedIn: false,
    
    // 搜索页面
    showSearch: false
  },

  onLoad(options) {
    const loginStatus = getLoginStatus()
    this.setData({ isLoggedIn: loginStatus.isLoggedIn })
    
    // 如果有搜索关键词
    if (options.keyword) {
      this.setData({ searchKeyword: options.keyword })
      this.searchProducts(options.keyword)
    } else {
      this.loadCategories()
      this.loadProducts()
    }
    
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

  // 搜索处理
  onSearch(e) {
    const keyword = e.detail.keyword
    if (!keyword) return
    
    this.setData({
      searchKeyword: keyword,
      showSearch: false,
      products: [],
      page: 1,
      hasMore: true
    })
    
    this.searchProducts(keyword)
  },

  // 搜索商品
  searchProducts(keyword) {
    if (!keyword) return
    
    this.setData({ loading: true })
    
    productApi.searchProducts(keyword, this.data.page, this.data.pageSize)
      .then(res => {
        const products = res.list || []
        
        // 应用筛选排序
        const sortedProducts = this.applyFilters(products)
        
        this.setData({
          products: this.data.page === 1 ? sortedProducts : [...this.data.products, ...sortedProducts],
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

  // 加载分类
  async loadCategories() {
    try {
      const categories = await productApi.getCategories()
      const formattedCategories = [
        { id: 0, name: '全部' },
        ...(categories || []).map(cat => ({
          id: cat.categoryId,
          name: cat.categoryName
        }))
      ]
      this.setData({ categories: formattedCategories })
    } catch (error) {
      console.error('加载分类失败:', error)
    }
  },

  // 加载商品
  async loadProducts() {
    if (this.data.loading) return

    this.setData({ loading: true })

    try {
      const { currentCategoryId, currentFilterId, page, pageSize } = this.data
      
      let result
      if (currentCategoryId === 0) {
        result = await productApi.getProducts({ page, pageSize })
      } else {
        result = await productApi.getProducts({ 
          categoryId: currentCategoryId, 
          page, 
          pageSize 
        })
      }

      let products = result.list || []
      const sortedProducts = this.applyFilters(products)

      this.setData({
        products: page === 1 ? sortedProducts : [...this.data.products, ...sortedProducts],
        hasMore: products.length >= pageSize,
        loading: false
      })
    } catch (error) {
      console.error('加载商品失败:', error)
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
      this.setData({ loading: false })
    }
  },

  // 应用筛选排序
  applyFilters(products) {
    const { currentFilterId } = this.data
    
    if (currentFilterId === 1) {
      // 销量优先
      return [...products].sort((a, b) => (b.sales || 0) - (a.sales || 0))
    } else if (currentFilterId === 2) {
      // 价格升
      return [...products].sort((a, b) => 
        (a.memberPrice || a.price) - (b.memberPrice || b.price)
      )
    } else if (currentFilterId === 3) {
      // 价格降
      return [...products].sort((a, b) => 
        (b.memberPrice || b.price) - (a.memberPrice || a.price)
      )
    }
    
    return products
  },

  // 加载更多
  loadMoreProducts() {
    if (!this.data.hasMore || this.data.loading) return
    
    this.setData({ page: this.data.page + 1 })
    
    if (this.data.searchKeyword) {
      this.searchProducts(this.data.searchKeyword)
    } else {
      this.loadProducts()
    }
  },

  // 刷新
  refreshProducts() {
    this.setData({
      page: 1,
      hasMore: true
    })
    
    if (this.data.searchKeyword) {
      this.searchProducts(this.data.searchKeyword)
    } else {
      this.loadProducts()
    }
  },

  // 选择分类
  onCategoryChange(e) {
    const categoryId = e.currentTarget.dataset.id
    if (categoryId === this.data.currentCategoryId) return

    this.setData({
      currentCategoryId: categoryId,
      products: [],
      page: 1,
      hasMore: true,
      searchKeyword: ''
    })
    
    this.loadProducts()
  },

  // 选择筛选
  onFilterChange(e) {
    const filterId = e.currentTarget.dataset.id
    if (filterId === this.data.currentFilterId) return

    this.setData({
      currentFilterId: filterId,
      products: [],
      page: 1,
      hasMore: true
    })
    
    if (this.data.searchKeyword) {
      this.searchProducts(this.data.searchKeyword)
    } else {
      this.loadProducts()
    }
  },

  // 加载购物车数量
  async loadCartCount() {
    try {
      const cartList = await cartApi.getCartList()
      this.setData({
        cartCount: (cartList || []).length
      })
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

  // 打开搜索
  openSearch() {
    this.setData({ showSearch: true })
  },

  // 关闭搜索
  closeSearch() {
    this.setData({ showSearch: false })
  },

  // 跳转购物车
  goToCart() {
    wx.switchTab({
      url: '/pages/sp_Cart_page/sp_Cart_page'
    })
  }
})
