// 商城首页 - sp_Mall（整合搜索框）
const { productApi, cartApi } = require('../../utils/sp_api.js')
const { getLoginStatus } = require('../../utils/sp_auth.js')

Page({
  data: {
    isLoggedIn: false,
    cartCount: 0,
    categories: [],
    hotProducts: [],
    newProducts: [],
    recommendProducts: [],
    loading: true
  },

  onLoad() {
    const loginStatus = getLoginStatus()
    this.setData({ isLoggedIn: loginStatus.isLoggedIn })
    
    this.loadData()
  },

  onShow() {
    const loginStatus = getLoginStatus()
    this.setData({ isLoggedIn: loginStatus.isLoggedIn })
    
    if (loginStatus.isLoggedIn) {
      this.loadCartCount()
    }
  },

  // 加载数据
  async loadData() {
    this.setData({ loading: true })
    
    try {
      await Promise.all([
        this.loadCategories(),
        this.loadHotProducts(),
        this.loadNewProducts(),
        this.loadRecommendProducts()
      ])
      
      if (this.data.isLoggedIn) {
        await this.loadCartCount()
      }
      
      this.setData({ loading: false })
    } catch (error) {
      console.error('加载数据失败:', error)
      this.setData({ loading: false })
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
    }
  },

  // 加载分类
  async loadCategories() {
    try {
      const categories = await productApi.getCategories()
      this.setData({ categories })
    } catch (error) {
      console.error('加载分类失败:', error)
    }
  },

  // 加载热销商品
  async loadHotProducts() {
    try {
      const products = await productApi.getHotProducts(10)
      this.setData({ hotProducts: products })
    } catch (error) {
      console.error('加载热销商品失败:', error)
    }
  },

  // 加载新品
  async loadNewProducts() {
    try {
      const products = await productApi.getNewProducts(10)
      this.setData({ newProducts: products })
    } catch (error) {
      console.error('加载新品失败:', error)
    }
  },

  // 加载推荐商品
  async loadRecommendProducts() {
    try {
      const products = await productApi.getRecommendProducts(10)
      this.setData({ recommendProducts: products })
    } catch (error) {
      console.error('加载推荐商品失败:', error)
    }
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

  // 跳转搜索页面
  goToSearch() {
    wx.navigateTo({
      url: '/pages/sp_SearchPage/sp_SearchPage'
    })
  },

  // 跳转商品详情
  goToDetail(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/sp_Details/sp_Details?id=${id}`
    })
  },

  // 跳转商品列表
  goToProductList(e) {
    const { type } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/sp_Product_list/sp_Product_list?type=${type || 'all'}`
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

  // 跳转购物车
  goToCart() {
    wx.switchTab({
      url: '/pages/sp_Cart_page/sp_Cart_page'
    })
  }
})
