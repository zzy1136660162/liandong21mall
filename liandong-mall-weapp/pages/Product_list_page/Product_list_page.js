const { productApi, cartApi, favoriteApi } = require('../../utils/sp_api.js')
const bannerService = require('../../services/bannerService.js')

Page({
  data: {
    filterTabs: [],
    currentFilter: 0,
    products: [],
    loading: false,
    noMore: false,
    page: 1,
    pageSize: 10,
    cartCount: 0,
    searchKeyword: '',
    productScrollTop: 0,
    refreshing: false,
    banners: [],
    bannerCurrent: 0,
    bannerAutoplay: true,
    bannerInterval: 3000,
    bannerDuration: 500,
    bannerCircular: true,
    bannerIndicatorDots: true,
    bannerLoading: true,
    bannerError: false,
    cartProductIds: []
  },

  lastScrollTime: 0,
  scrollThrottle: 50,

  async onLoad(options) {
    await this.loadFilterCategories()
    this.loadBanners()
    this.loadProducts()
    this.loadCartInfo()
  },

  onShow() {
    this.loadCartInfo()
  },

  async loadFilterCategories() {
    try {
      const categories = await productApi.getFilterCategories()
      if (categories && categories.length > 0) {
        const filterTabs = [
          { id: 0, name: '全部', code: 'all' },
          ...categories.map(cat => ({
            id: cat.id,
            name: cat.name,
            code: cat.code
          }))
        ]
        this.setData({ filterTabs })
      }
    } catch (error) {
      console.error('加载筛选类别失败:', error)
      this.setData({
        filterTabs: [
          { id: 0, name: '全部', code: 'all' }
        ]
      })
    }
  },

  async loadBanners() {
    this.setData({
      bannerLoading: true,
      bannerError: false
    })

    try {
      const banners = await bannerService.getMallBanners(true)

      if (banners && banners.length > 0) {
        this.setData({
          banners: banners,
          bannerLoading: false,
          bannerAutoplay: banners.length > 1
        })

        bannerService.preloadImages(banners)
      } else {
        const defaultBanners = bannerService.getDefaultBanners()
        this.setData({
          banners: defaultBanners,
          bannerLoading: false,
          bannerAutoplay: true
        })

        bannerService.preloadImages(defaultBanners)
      }
    } catch (error) {
      console.error('加载轮播图失败:', error)
      const defaultBanners = bannerService.getDefaultBanners()
      this.setData({
        banners: defaultBanners,
        bannerLoading: false,
        bannerError: true,
        bannerAutoplay: true
      })

      wx.showToast({
        title: '轮播图加载失败，已使用默认图',
        icon: 'none',
        duration: 2000
      })
    }
  },

  onBannerImageLoad(e) {
    const index = e.currentTarget.dataset.index
    const banners = this.data.banners
    if (banners[index]) {
      banners[index].isLoaded = true
      this.setData({ banners })
    }
  },

  onBannerImageError(e) {
    const index = e.currentTarget.dataset.index
    const banners = this.data.banners
    if (banners[index]) {
      banners[index].loadFailed = true
      banners[index].image = 'https://picsum.photos/750/400?random=error'
      this.setData({ banners })
    }
  },

  onBannerChange(e) {
    if (e.detail.source) {
      this.setData({
        bannerCurrent: e.detail.current
      })
    }
  },

  onBannerTap(e) {
    const index = e.currentTarget.dataset.index
    const banner = this.data.banners[index]

    if (!banner) {
      return
    }

    bannerService.handleBannerClick(banner, getApp())
  },

  refreshBanners() {
    bannerService.clearCache()
    this.loadBanners()
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

  // 跳转到搜索页面
  goToSearchPage() {
    wx.navigateTo({
      url: '/pages/sp_SearchPage/sp_SearchPage',
      success: () => {
        console.log('跳转到搜索页成功')
      },
      fail: (err) => {
        console.error('跳转搜索页失败:', err)
        wx.showToast({
          title: '页面跳转失败',
          icon: 'none',
          duration: 2000
        })
      }
    })
  },

  goToDetail(e) {
    const productId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/sp_Details/sp_Details?id=${productId}`,
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

  async toggleFavorite(e) {
    const productId = e.currentTarget.dataset.id
    
    try {
      const product = this.data.products.find(p => p.productId === productId)
      
      if (product.favorite) {
        await favoriteApi.removeFavorite(productId)
      } else {
        await favoriteApi.addFavorite(productId)
      }
      
      const products = this.data.products.map(p => {
        if (p.productId === productId) {
          return { ...p, favorite: !p.favorite }
        }
        return p
      })
      
      this.setData({ products })
      
      const updatedProduct = products.find(p => p.productId === productId)
      wx.showToast({
        title: updatedProduct.favorite ? '已收藏' : '已取消收藏',
        icon: updatedProduct.favorite ? 'success' : 'none',
        duration: 1500
      })
    } catch (error) {
      console.error('收藏操作失败:', error)
      wx.showToast({
        title: '操作失败',
        icon: 'none',
        duration: 1500
      })
    }
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
      
      this.loadCartCount()
    } catch (error) {
      console.error('加入购物车失败:', error)
    }
  },

  async loadCartInfo() {
    try {
      const cartList = await cartApi.getCartList()
      const cartCount = cartList ? cartList.length : 0
      const cartProductIds = cartList ? cartList.map(item => item.productId) : []
      this.setData({ cartCount, cartProductIds })
    } catch (error) {
      console.error('获取购物车信息失败:', error)
    }
  },

  async addToCart(e) {
    const productId = e.currentTarget.dataset.id
    
    if (this.data.cartProductIds.includes(productId)) {
      wx.showToast({
        title: '已在购物车中',
        icon: 'none',
        duration: 1500
      })
      return
    }
    
    try {
      await cartApi.addToCart(productId, null, 1)
      
      const cartProductIds = [...this.data.cartProductIds, productId]
      this.setData({ cartProductIds })
      
      wx.showToast({
        title: '已加入购物车',
        icon: 'success',
        duration: 1500
      })
      
      this.loadCartInfo()
    } catch (error) {
      console.error('加入购物车失败:', error)
      wx.showToast({
        title: '加入失败',
        icon: 'none',
        duration: 2000
      })
    }
  },

  goToCart() {
    wx.navigateTo({
      url: '/pages/sp_Cart_page/sp_Cart_page'
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
