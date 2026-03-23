const cartApi = require('../../utils/sp_api.js').cartApi

Page({
  data: {
    productId: '',
    product: {
      id: '',
      name: '',
      subtitle: '',
      price: '0',
      originalPrice: '',
      discount: '',
      memberPrice: '',
      saveAmount: '',
      stock: 0,
      sales: 0,
      reviews: 0,
      tags: [],
      images: [],
      specs: [],
      description: '',
      reviewList: [],
      recommendations: []
    },
    currentIndex: 0,
    selectedSpecs: {},
    isFavorite: false,
    isInCart: false,
    cartCount: 0,
    loading: false,
    addingToCart: false
  },

  onLoad(options) {
    if (options.id) {
      this.setData({
        productId: options.id
      })
      this.loadProductDetail()
    }
  },

  onShow() {
    this.loadCartCount()
    this.checkInCart()
    this.checkFavoriteStatus()
  },

  async loadProductDetail() {
    this.setData({ loading: true })

    try {
      const product = await this.getProductDetail(this.data.productId)
      this.setData({
        product: product,
        currentIndex: 0
      })
    } catch (error) {
      console.error('加载商品详情失败:', error)
      wx.showToast({
        title: '加载失败',
        icon: 'none',
        duration: 2000
      })
    } finally {
      this.setData({ loading: false })
    }
  },

  getProductDetail(productId) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: 'http://localhost:5000/api/sp_product_detail/detail',
        method: 'GET',
        data: { productId },
        success: (res) => {
          if (res.data.code === 200) {
            resolve(res.data.data)
          } else {
            reject(new Error(res.data.message))
          }
        },
        fail: (err) => {
          reject(err)
        }
      })
    })
  },

  onSwiperChange(e) {
    this.setData({
      currentIndex: e.detail.current
    })
  },

  previewImage(e) {
    const url = e.currentTarget.dataset.url
    const images = this.data.product.images
    wx.previewImage({
      current: url,
      urls: images
    })
  },

  selectSpec(e) {
    const name = e.currentTarget.dataset.name
    const value = e.currentTarget.dataset.value
    const selectedSpecs = { ...this.data.selectedSpecs }
    selectedSpecs[name] = value
    this.setData({ selectedSpecs })
  },

  toggleFavorite() {
    const isFavorite = !this.data.isFavorite
    this.setData({ isFavorite })

    if (isFavorite) {
      this.addToFavorites()
      wx.showToast({
        title: '已收藏',
        icon: 'success',
        duration: 1500
      })
    } else {
      this.removeFromFavorites()
      wx.showToast({
        title: '已取消收藏',
        icon: 'none',
        duration: 1500
      })
    }
  },

  addToFavorites() {
    wx.request({
      url: 'http://localhost:5000/api/sp_product_detail/favorite/add',
      method: 'POST',
      data: {
        productId: this.data.productId
      },
      success: (res) => {
        console.log('添加收藏成功')
      },
      fail: (err) => {
        console.error('添加收藏失败:', err)
      }
    })
  },

  removeFromFavorites() {
    wx.request({
      url: 'http://localhost:5000/api/sp_product_detail/favorite/remove',
      method: 'POST',
      data: {
        productId: this.data.productId
      },
      success: (res) => {
        console.log('取消收藏成功')
      },
      fail: (err) => {
        console.error('取消收藏失败:', err)
      }
    })
  },

  checkFavoriteStatus() {
    wx.request({
      url: 'http://localhost:5000/api/sp_product_detail/favorite/check',
      method: 'GET',
      data: {
        productId: this.data.productId
      },
      success: (res) => {
        if (res.data.code === 200) {
          this.setData({
            isFavorite: res.data.data.isFavorite
          })
        }
      },
      fail: (err) => {
        console.error('检查收藏状态失败:', err)
      }
    })
  },

  shareProduct() {
    wx.showShareMenu({
      withShareTicket: true
    })
  },

  onShareAppMessage() {
    return {
      title: this.data.product.name,
      path: `/pages/sp_Details/sp_Details?id=${this.data.productId}`,
      imageUrl: this.data.product.images[0]
    }
  },

  async addToCart() {
    if (this.data.addingToCart) return
    
    this.setData({ addingToCart: true })
    
    try {
      await cartApi.addToCart(this.data.productId, null, 1)
      
      this.setData({ isInCart: true })
      
      wx.showToast({
        title: '已加入购物车',
        icon: 'success',
        duration: 1500
      })
      
      this.loadCartCount()
    } catch (error) {
      console.error('加入购物车失败:', error)
      wx.showToast({
        title: '加入失败',
        icon: 'none',
        duration: 2000
      })
    } finally {
      setTimeout(() => {
        this.setData({ addingToCart: false })
      }, 500)
    }
  },

  buyNow() {
    this.addToCart().then(() => {
      wx.navigateTo({
        url: '/pages/sp_Cart_page/sp_Cart_page'
      })
    }).catch((error) => {
      console.error('立即购买失败:', error)
    })
  },

  goToCart() {
    wx.navigateTo({
      url: '/pages/sp_Cart_page/sp_Cart_page'
    })
  },

  async loadCartCount() {
    try {
      const cartList = await cartApi.getCartList()
      const cartCount = cartList ? cartList.length : 0
      this.setData({ cartCount })
    } catch (error) {
      console.error('获取购物车数量失败:', error)
    }
  },

  async checkInCart() {
    try {
      const cartList = await cartApi.getCartList()
      const isInCart = cartList && cartList.some(item => item.productId === parseInt(this.data.productId))
      this.setData({ isInCart })
    } catch (error) {
      console.error('检查购物车状态失败:', error)
    }
  },

  viewAllReviews() {
    wx.showToast({
      title: '查看全部评价',
      icon: 'none',
      duration: 1500
    })
  },

  goToRecommendation(e) {
    const productId = e.currentTarget.dataset.id
    wx.redirectTo({
      url: `/pages/sp_Details/sp_Details?id=${productId}`
    })
  },

  goBack() {
    wx.navigateBack({
      delta: 1
    })
  }
})
