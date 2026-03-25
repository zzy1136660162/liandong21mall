
const orderApi = require('../../utils/sp_api.js').orderApi

Page({
  data: {
    tabs: [
      { key: 'all', label: '全部' },
      { key: 'PENDING_PAY', label: '待付款' },
      { key: 'PAID', label: '待发货' },
      { key: 'SHIPPED', label: '待收货' },
      { key: 'FINISHED', label: '已完成' },
      { key: 'CANCELLED', label: '已取消' }
    ],
    currentTab: 'all',
    orderList: [],
    page: 1,
    pageSize: 10,
    hasMore: true,
    useMockData: false
  },

  onLoad(options) {
    const { tab } = options
    if (tab) {
      this.setData({ currentTab: tab })
    }
    this.loadOrders()
  },

  onShow() {
    this.loadOrders()
  },

  onPullDownRefresh() {
    this.setData({ page:1, hasMore: true })
    this.loadOrders().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  onReachBottom() {
    if (this.data.hasMore) {
      this.loadMoreOrders()
    }
  },

  async loadOrders() {
    try {
      const { currentTab, page, pageSize } = this.data
      const status = currentTab === 'all' ? null : currentTab
      const res = await orderApi.getOrderList(status, page, pageSize)
      
      const orderList = (res || []).map(order => ({
        ...order,
        statusText: this.getStatusText(order.status)
      }))

      this.setData({
        orderList,
        hasMore: orderList.length >= pageSize,
        useMockData: false
      })
    } catch (error) {
      console.error('加载订单列表失败:', error)
      this.setData({ useMockData: true })
      this.loadMockData()
    }
  },

  loadMockData() {
    const { currentTab } = this.data
    let mockOrders = []

    if (currentTab === 'all' || currentTab === 'PENDING_PAY') {
      mockOrders.push({
        orderId: 1,
        status: 'PENDING_PAY',
        statusText: '待付款',
        createTime: '2024-03-20 10:30:00',
        products: [
          {
            productId: 42,
            productName: '焕颜修护精华液',
            mainImage: 'https://images.unsplash.com/photo-1522335789203-aabd016d8d3?w=400&h=400&fit=crop',
            specs: '30ml',
            price: 299.00,
            quantity: 2
          }
        ],
        finalAmount: 598.00
      })
    }

    if (currentTab === 'all' || currentTab === 'PAID') {
      mockOrders.push({
        orderId: 2,
        status: 'PAID',
        statusText: '待发货',
        createTime: '2024-03-19 15:20:00',
        products: [
          {
            productId: 43,
            productName: '水感透白面霜',
            mainImage: 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc8?w=400&h=400&fit=crop',
            specs: '50g',
            price: 199.00,
            quantity: 1
          }
        ],
        finalAmount: 199.00
      })
    }

    if (currentTab === 'all' || currentTab === 'SHIPPED') {
      mockOrders.push({
        orderId: 3,
        status: 'SHIPPED',
        statusText: '待收货',
        createTime: '2024-03-18 09:15:00',
        products: [
          {
            productId: 44,
            productName: '紧致眼霜',
            mainImage: 'https://images.unsplash.com/photo-1617897903246-719242758050?w=400&h=400&fit=crop',
            specs: '15ml',
            price: 159.00,
            quantity: 1
          }
        ],
        finalAmount: 159.00
      })
    }

    if (currentTab === 'all' || currentTab === 'FINISHED') {
      mockOrders.push({
        orderId: 4,
        status: 'FINISHED',
        statusText: '已完成',
        createTime: '2024-03-15 14:45:00',
        products: [
          {
            productId: 45,
            productName: '温和洁面乳',
            mainImage: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop',
            specs: '100ml',
            price: 89.00,
            quantity: 2
          }
        ],
        finalAmount: 178.00
      })
    }

    if (currentTab === 'all' || currentTab === 'CANCELLED') {
      mockOrders.push({
        orderId: 5,
        status: 'CANCELLED',
        statusText: '已取消',
        createTime: '2024-03-21 09:30:00',
        products: [
          {
            productId: 46,
            productName: '补水面膜',
            mainImage: 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=400&h=400&fit=crop',
            specs: '5片装',
            price: 69.00,
            quantity: 1
          }
        ],
        finalAmount: 69.00
      })
    }

    this.setData({
      orderList: mockOrders,
      hasMore: false,
      useMockData: true
    })
  },

  switchTab(e) {
    const { key } = e.currentTarget.dataset
    if (key === this.data.currentTab) return

    this.setData({
      currentTab: key,
      page: 1,
      hasMore: true
    })
    this.loadOrders()
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

  goToDetail(e) {
    const { orderid } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/sp_Order_detail_page/sp_Order_detail_page?orderId=${orderid}`
    })
  },

  async cancelOrder(e) {
    const { orderid } = e.currentTarget.dataset
    wx.showModal({
      title: '提示',
      content: '确定要取消该订单吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            wx.showLoading({ title: '取消中...' })
            await orderApi.cancelOrder(orderid)
            wx.hideLoading()
            
            wx.showToast({
              title: '取消成功',
              icon: 'success'
            })
            
            this.loadOrders()
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

  async payOrder(e) {
    const { orderid } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/sp_Payment/sp_Payment?orderId=${orderid}`
    })
  },

  async confirmReceipt(e) {
    const { orderid } = e.currentTarget.dataset
    wx.showModal({
      title: '提示',
      content: '确定要确认收货吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            wx.showLoading({ title: '确认中...' })
            await orderApi.confirmReceipt(orderid)
            wx.hideLoading()
            
            wx.showToast({
              title: '确认成功',
              icon: 'success'
            })
            
            this.loadOrders()
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
  },

  buyAgain(e) {
    const { orderid } = e.currentTarget.dataset
    wx.showToast({
      title: '再次购买功能开发中',
      icon: 'none'
    })
  },

  goToShopping() {
    wx.switchTab({
      url: '/pages/Product_list_page/Product_list_page'
    })
  }
})
