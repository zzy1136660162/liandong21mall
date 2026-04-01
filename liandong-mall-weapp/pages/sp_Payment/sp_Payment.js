const { checkLogin, getLoginStatus } = require('../../utils/sp_auth.js')

Page({
  data: {
    productId: '',
    skuId: '',
    quantity: 1,
    price: 0,
    totalPrice: 0,
    product: {},
    selectedSpecs: {},
    address: null,
    remark: '',
    selectedPayment: 'wechat',
    submitting: false,
    isLoggedIn: false
  },

  onLoad(options) {
    const loginStatus = getLoginStatus()
    this.setData({ isLoggedIn: loginStatus.isLoggedIn })
    
    if (!loginStatus.isLoggedIn) {
      checkLogin({ showToast: false })
      setTimeout(() => {
        checkLogin({ showToast: true })
      }, 100)
      return
    }
    
    if (options.productId) {
      this.setData({
        productId: parseInt(options.productId) || 0,
        skuId: options.skuId ? parseInt(options.skuId) : null,
        quantity: parseInt(options.quantity) || 1,
        price: parseFloat(options.price) || 0,
        totalPrice: parseFloat(options.totalPrice) || 0
      })
      this.loadProductDetail()
    }
    this.loadDefaultAddress()
  },

  onShow() {
    const loginStatus = getLoginStatus()
    this.setData({ isLoggedIn: loginStatus.isLoggedIn })
  },

  async loadDefaultAddress() {
    try {
      const address = await this.getDefaultAddress()
      if (address) {
        this.setData({ address })
      }
    } catch (error) {
      console.error('加载默认地址失败:', error)
    }
  },

  getDefaultAddress() {
    return new Promise((resolve, reject) => {
      wx.request({
        url: 'http://localhost:5000/api/sp/address/default',
        method: 'GET',
        success: (res) => {
          if (res.data.code === 200) {
            resolve(res.data.data)
          } else {
            resolve(null)
          }
        },
        fail: (err) => {
          reject(err)
        }
      })
    })
  },

  async loadProductDetail() {
    try {
      const product = await this.getProductDetail(this.data.productId)
      this.setData({ product })
      
      if (this.data.skuId) {
        this.loadSkuSpecs()
      }
    } catch (error) {
      console.error('加载商品详情失败:', error)
      wx.showToast({
        title: '加载失败',
        icon: 'none',
        duration: 2000
      })
    }
  },

  getProductDetail(productId) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `http://localhost:5000/api/sp/product/${productId}`,
        method: 'GET',
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

  loadSkuSpecs() {
    const product = this.data.product
    if (!product.skus || product.skus.length === 0) return

    const skuId = parseInt(this.data.skuId)
    const matchedSku = product.skus.find(sku => sku.skuId === skuId)
    
    if (matchedSku && matchedSku.spec) {
      this.setData({ selectedSpecs: matchedSku.spec })
    }
  },

  selectAddress() {
    wx.navigateTo({
      url: '/pages/sp_Address_page/sp_Address_page?fromOrder=true'
    })
  },

  onShow() {
    const pages = getCurrentPages()
    const currentPage = pages[pages.length - 1]
    
    if (currentPage.data.selectedAddress) {
      this.setData({
        address: currentPage.data.selectedAddress
      })
      currentPage.setData({ selectedAddress: null })
    }
  },

  onRemarkInput(e) {
    this.setData({
      remark: e.detail.value
    })
  },

  selectPayment(e) {
    const method = e.currentTarget.dataset.method
    this.setData({
      selectedPayment: method
    })
  },

  async submitOrder() {
    if (this.data.submitting) return

    if (!this.data.address) {
      wx.showToast({
        title: '请选择收货地址',
        icon: 'none',
        duration: 2000
      })
      return
    }

    this.setData({ submitting: true })

    try {
      const orderData = {
        items: [{
          productId: parseInt(this.data.productId),
          skuId: this.data.skuId ? parseInt(this.data.skuId) : null,
          quantity: parseInt(this.data.quantity)
        }],
        address: this.data.address,
        remark: this.data.remark
      }

      const order = await this.createOrder(orderData)
      
      wx.showToast({
        title: '订单创建成功',
        icon: 'success',
        duration: 1500
      })

      setTimeout(() => {
        wx.redirectTo({
          url: `/pages/sp_Order_detail_page/sp_Order_detail_page?orderId=${order.orderId}`
        })
      }, 1500)

    } catch (error) {
      console.error('提交订单失败:', error)
      wx.showToast({
        title: error.message || '提交失败',
        icon: 'none',
        duration: 2000
      })
    } finally {
      setTimeout(() => {
        this.setData({ submitting: false })
      }, 2000)
    }
  },

  createOrder(orderData) {
    return new Promise((resolve, reject) => {
      const userId = wx.getStorageSync('userId') || 1
      
      console.log('创建订单 - 用户ID:', userId)
      console.log('创建订单 - 数据:', JSON.stringify(orderData, null, 2))
      
      wx.request({
        url: 'http://localhost:5000/api/sp/order/create',
        method: 'POST',
        data: orderData,
        header: {
          'Content-Type': 'application/json',
          'X-User-Id': userId
        },
        success: (res) => {
          console.log('创建订单 - 响应:', JSON.stringify(res.data, null, 2))
          
          if (res.data.code === 200) {
            resolve(res.data.data)
          } else {
            reject(new Error(res.data.message || '创建订单失败'))
          }
        },
        fail: (err) => {
          console.error('创建订单 - 请求失败:', err)
          reject(err)
        }
      })
    })
  },

  goBack() {
    wx.navigateBack({
      delta: 1
    })
  }
})
