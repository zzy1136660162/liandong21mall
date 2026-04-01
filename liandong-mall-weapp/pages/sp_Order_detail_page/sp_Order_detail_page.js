const orderApi = require('../../utils/sp_api.js').orderApi

// 默认图片
const DEFAULT_PRODUCT_IMAGE = '/static/images/products/product_1_main.jpg'

Page({
  data: {
    orderId: '',
    orderDetail: {
      orderId: '',
      status: '',
      statusText: '',
      statusDesc: '',
      address: {
        name: '',
        phone: '',
        detail: ''
      },
      products: [],
      totalAmount: 0,
      shippingFee: 0,
      discountAmount: 0,
      finalAmount: 0,
      createTime: '',
      payTime: '',
      shipTime: '',
      finishTime: '',
      remark: ''
    },
    statusIcon: '📦',
    useMockData: false,
    remainingSeconds: 0,  // 剩余支付时间（秒）
    countdownText: ''     // 倒计时文本
  },
  
  // 图片加载失败处理
  handleImageError(e) {
    const { index } = e.currentTarget.dataset
    const { orderDetail } = this.data
    
    if (orderDetail.products && orderDetail.products[index]) {
      orderDetail.products[index].productImage = DEFAULT_PRODUCT_IMAGE
      this.setData({ orderDetail })
    }
  },
  
  onLoad(options) {
    console.log('订单详情页 - onLoad options:', options)
    console.log('订单详情页 - options.orderId:', options.orderId)
    
    const { orderId } = options
    
    if (orderId) {
      console.log('订单详情页 - 有效orderId:', orderId)
      this.setData({ orderId: orderId })
      this.loadOrderDetail()
    } else {
      console.error('订单详情页 - orderId无效或为空!')
      wx.showToast({
        title: '订单ID不存在',
        icon: 'none'
      })
      setTimeout(() => {
        wx.navigateBack()
      }, 1500)
    }
  },

  onShow() {
    if (this.data.orderId) {
      this.loadOrderDetail()
    }
  },

  onPullDownRefresh() {
    this.loadOrderDetail().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  async loadOrderDetail() {
    try {
      console.log('开始加载订单详情, orderId:', this.data.orderId)
      
      const { orderId } = this.data
      console.log('调用API: orderApi.getOrderDetail(', orderId, ')')
      
      const res = await orderApi.getOrderDetail(orderId)
      
      console.log('API返回结果:', res)
      console.log('API返回类型:', typeof res)
      console.log('API返回是否为空:', res === null, res === undefined)
      
      if (res) {
        const orderDetail = {
          ...res,
          statusText: this.getStatusText(res.status),
          statusDesc: this.getStatusDesc(res.status)
        }

        this.setData({
          orderDetail,
          statusIcon: this.getStatusIcon(res.status),
          useMockData: false
        })
        
        // 检查订单是否需要设置自动取消定时器
        this.checkAutoCancelOrder(orderDetail)
      } else {
        wx.showToast({
          title: '加载失败',
          icon: 'none'
        })
      }
    } catch (error) {
      console.error('加载订单详情失败:', error)
      this.setData({ useMockData: true })
      this.loadMockData()
    }
  },

  // 检查订单是否需要自动取消
  checkAutoCancelOrder(orderDetail) {
    // 如果是待付款状态，设置30分钟自动取消
    if (orderDetail.status === 'PENDING_PAY') {
      // 清除之前的定时器（如果有）
      if (this.cancelTimer) {
        clearTimeout(this.cancelTimer)
      }
      if (this.countdownTimer) {
        clearInterval(this.countdownTimer)
      }
      
      // 使用后端返回的剩余时间，如果没有则计算
      let remainingTime = 30 * 60 * 1000  // 默认30分钟
      
      if (orderDetail.remainingSeconds) {
        remainingTime = orderDetail.remainingSeconds * 1000
      } else {
        // 计算剩余时间
        const createTime = new Date(orderDetail.createTime)
        const expireTime = new Date(createTime.getTime() + 30 * 60 * 1000) // 30分钟后
        const now = new Date()
        remainingTime = expireTime - now
      }
      
      // 如果还没到过期时间，设置倒计时和定时器
      if (remainingTime > 0) {
        this.setData({
          remainingSeconds: Math.floor(remainingTime / 1000),
          countdownText: this.formatCountdown(Math.floor(remainingTime / 1000))
        })
        
        // 启动倒计时更新（每秒更新一次）
        this.countdownTimer = setInterval(() => {
          const currentRemaining = this.data.remainingSeconds - 1
          if (currentRemaining > 0) {
            this.setData({
              remainingSeconds: currentRemaining,
              countdownText: this.formatCountdown(currentRemaining)
            })
          } else {
            // 时间到，取消订单
            if (this.countdownTimer) {
              clearInterval(this.countdownTimer)
            }
          }
        }, 1000)
        
        // 设置超时取消定时器
        this.cancelTimer = setTimeout(() => {
          this.autoCancelOrder()
        }, remainingTime)
      } else {
        // 已经过期，直接取消订单
        this.autoCancelOrder()
      }
    } else {
      // 非待付款状态，清除定时器
      if (this.cancelTimer) {
        clearTimeout(this.cancelTimer)
        this.cancelTimer = null
      }
      if (this.countdownTimer) {
        clearInterval(this.countdownTimer)
        this.countdownTimer = null
      }
    }
  },
  
  // 格式化倒计时文本
  formatCountdown(seconds) {
    const minutes = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${minutes}分${secs.toString().padStart(2, '0')}秒`
  },

  // 自动取消订单
  async autoCancelOrder() {
    try {
      const { orderId } = this.data
      await orderApi.cancelOrder(orderId, '订单超时自动取消')
      
      // 更新订单状态
      const orderDetail = {
        ...this.data.orderDetail,
        status: 'CANCELLED',
        statusText: '已取消',
        statusDesc: '订单超时自动取消'
      }
      
      this.setData({
        orderDetail,
        statusIcon: this.getStatusIcon('CANCELLED')
      })
      
      // 显示取消通知
      wx.showToast({
        title: '订单已超时自动取消',
        icon: 'none'
      })
    } catch (error) {
      console.error('自动取消订单失败:', error)
    }
  },

  loadMockData() {
    const { orderId } = this.data
    const mockOrderDetail = {
      orderId: orderId || 'ORD20240320001',
      status: 'SHIPPED',
      statusText: '待收货',
      statusDesc: '商品正在配送中',
      address: {
        name: '张三',
        phone: '138****8888',
        detail: '北京市朝阳区xxx街道xxx号xxx小区xxx号楼xxx室'
      },
      products: [
        {
          productId: 42,
          productName: '焕颜修护精华液',
          productImage: DEFAULT_PRODUCT_IMAGE,
          specs: '30ml',
          price: 299.00,
          quantity: 2
        },
        {
          productId: 43,
          productName: '深层清洁洁面乳',
          productImage: DEFAULT_PRODUCT_IMAGE,
          specs: '100ml',
          price: 158.00,
          quantity: 1
        }
      ],
      totalAmount: 756.00,
      shippingFee: 0,
      discountAmount: 0,
      finalAmount: 756.00,
      createTime: '2024-03-20 10:30:00',
      payTime: '2024-03-20 10:35:00',
      shipTime: '2024-03-21 09:00:00',
      finishTime: '',
      remark: '请尽快发货，谢谢'
    }

    this.setData({
      orderDetail: mockOrderDetail,
      statusIcon: this.getStatusIcon(mockOrderDetail.status)
    })
  },

  getStatusText(status) {
    const statusMap = {
      'PENDING_PAY': '待付款',
      'PAID': '待发货',
      'SHIPPED': '待收货',
      'FINISHED': '已完成',
      'CANCELLED': '已取消'
    }
    return statusMap[status] || '未知状态'
  },

  getStatusDesc(status) {
    const descMap = {
      'PENDING_PAY': '请在30分钟内完成支付',
      'PAID': '商家正在准备发货',
      'SHIPPED': '商品正在配送中',
      'FINISHED': '订单已完成',
      'CANCELLED': '订单已取消'
    }
    return descMap[status] || ''
  },

  getStatusIcon(status) {
    const iconMap = {
      'PENDING_PAY': '💳',
      'PAID': '📦',
      'SHIPPED': '🚚',
      'FINISHED': '✅',
      'CANCELLED': '❌'
    }
    return iconMap[status] || '📦'
  },

  copyOrderId() {
    const { orderId } = this.data
    wx.setClipboardData({
      data: orderId,
      success: () => {
        wx.showToast({
          title: '复制成功',
          icon: 'success'
        })
      }
    })
  },

  goToProductDetail(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/sp_Details/sp_Details?id=${id}`
    })
  },

  async cancelOrder() {
    const { orderId } = this.data
    wx.showModal({
      title: '提示',
      content: '确定要取消该订单吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            wx.showLoading({ title: '取消中...' })
            await orderApi.cancelOrder(orderId)
            wx.hideLoading()
            
            wx.showToast({
              title: '取消成功',
              icon: 'success'
            })
            
            this.loadOrderDetail()
          } catch (error) {
            wx.hideLoading()
            console.error('取消订单失败:', error)
            wx.showToast({
              title: '取消失败',
              icon: 'none'
            })
          }
        }
      }
    })
  },

  // 支付订单
  async payOrder() {
    const { orderId, orderDetail } = this.data
    
    try {
      wx.showLoading({
        title: '正在发起支付...',
        mask: true
      })
      
      // 调用后端支付API
      const userId = wx.getStorageSync('userId') || 1
      
      const payResult = await new Promise((resolve, reject) => {
        wx.request({
          url: `http://localhost:5000/api/sp/order/pay/${orderId}`,
          method: 'POST',
          data: {
            paymentMethod: 'WECHAT_PAY'
          },
          header: {
            'Content-Type': 'application/json',
            'X-User-Id': userId
          },
          success: (res) => {
            if (res.data.code === 200) {
              resolve(res.data.data)
            } else {
              reject(new Error(res.data.message || '支付失败'))
            }
          },
          fail: (err) => {
            reject(err)
          }
        })
      })
      
      wx.hideLoading()
      
      console.log('支付成功，返回数据:', payResult)
      
      // 显示支付成功弹窗
      this.showPaySuccessModal()
      
      // 重新加载订单详情，获取最新状态
      await this.loadOrderDetail()
      
    } catch (error) {
      console.error('支付失败:', error)
      wx.hideLoading()
      
      // 如果是用户取消支付
      if (error.errMsg && error.errMsg.includes('cancel')) {
        wx.showToast({
          title: '已取消支付',
          icon: 'none'
        })
      } else {
        wx.showToast({
          title: error.message || '支付失败，请重试',
          icon: 'none'
        })
      }
    }
  },

  // 显示支付成功弹窗
  showPaySuccessModal() {
    wx.showModal({
      title: '支付成功',
      content: '您的订单已支付成功，商家正在准备发货',
      showCancel: false,
      confirmText: '查看订单',
      success: (res) => {
        if (res.confirm) {
          // 可以跳转到订单列表或其他页面
        }
      }
    })
  },

  contactService() {
    wx.showToast({
      title: '联系客服功能开发中',
      icon: 'none'
    })
  },

  async confirmReceipt() {
    const { orderId } = this.data
    wx.showModal({
      title: '提示',
      content: '确定要确认收货吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            wx.showLoading({ title: '确认中...' })
            await orderApi.confirmReceipt(orderId)
            wx.hideLoading()
            
            wx.showToast({
              title: '确认成功',
              icon: 'success'
            })
            
            this.loadOrderDetail()
          } catch (error) {
            wx.hideLoading()
            console.error('确认收货失败:', error)
            wx.showToast({
              title: '确认失败',
              icon: 'none'
            })
          }
        }
      }
    })
  }
})
