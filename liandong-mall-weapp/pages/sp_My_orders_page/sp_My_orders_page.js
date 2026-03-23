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
      const res = await orderApi.getOrderList({ status, page, pageSize })
      
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
        orderId: 'ORD20240320001',
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
        orderId: 'ORD20240319001',
        status: 'PAID',
        statusText: '待发货',
        createTime: '2024-03-19 15:20:00',
        products: [
          {
            productId: 43,
            productName: '深层清洁洁面乳',
            mainImage: 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop',
            specs: '100ml',
            price: 158.00,
            quantity: 1
          },
          {
            productId: 44,
            productName: '保湿修护面霜',
            mainImage: 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=400&h=400&fit=crop',
            specs: '50g',
            price: 358.00,
            quantity: 1
          }
        ],
        finalAmount: 516.00
      })
    }

    if (currentTab === 'all' || currentTab === 'SHIPPED') {
      mockOrders.push({
        orderId: 'ORD20240318001',
        status: 'SHIPPED',
        statusText: '待收货',
        createTime: '2024-03-18 09:15:00',
        products: [
          {
            productId: 45,
            productName: '舒缓修护精华水',
            mainImage: 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc8?w=400&h=400&fit=crop',
            specs: '150ml',
            price: 228.00,
            quantity: 2
          }
        ],
        finalAmount: 456.00
      })
    }

    if (currentTab === 'all' || currentTab === 'FINISHED') {
      mockOrders.push({
        orderId: 'ORD20240315001',
        status: 'FINISHED',
        statusText: '已完成',
        createTime: '2024-03-15 14:45:00',
        products: [
          {
            productId: 46,
            productName: '紧致抗皱眼霜',
            mainImage: 'https://images.unsplash.com/photo-1570194065650-d99fb4b38b15?w=400&h=400&fit=crop',
            specs: '15g',
            price: 268.00,
            quantity: 1
          }
        ],
        finalAmount: 268.00
      })
    }

    // 添加已取消订单
    if (currentTab === 'all' || currentTab === 'CANCELLED') {
      mockOrders.push({
        orderId: 'ORD20240321001',
        status: 'CANCELLED',
        statusText: '已取消',
        createTime: '2024-03-21 09:30:00',
        products: [
          {
            productId: 47,
            productName: '美白保湿面膜',
            mainImage: 'https://images.unsplash.com/photo-1556228578-71154565c555?w=400&h=400&fit=crop',
            specs: '25ml*10片',
            price: 198.00,
            quantity: 1
          }
        ],
        finalAmount: 198.00
      })
    }

    this.setData({
      orderList: mockOrders,
      hasMore: false
    })
  },

  async loadMoreOrders() {
    if (!this.data.hasMore) return

    try {
      const { currentTab, page, pageSize, orderList } = this.data
      const status = currentTab === 'all' ? null : currentTab
      const res = await orderApi.getOrderList({ status, page: page + 1, pageSize })
      
      const newOrders = (res || []).map(order => ({
        ...order,
        statusText: this.getStatusText(order.status)
      }))

      this.setData({
        orderList: [...orderList, ...newOrders],
        page: page + 1,
        hasMore: newOrders.length >= pageSize
      })
    } catch (error) {
      console.error('加载更多订单失败:', error)
    }
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
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/sp_Order_detail_page/sp_Order_detail_page?id=${id}`
    })
  },

  async cancelOrder(e) {
    const { id } = e.currentTarget.dataset
    wx.showModal({
      title: '提示',
      content: '确定要取消该订单吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            wx.showLoading({ title: '取消中...' })
            await orderApi.cancelOrder(id)
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
    const { id } = e.currentTarget.dataset
    wx.showToast({
      title: '支付功能开发中',
      icon: 'none'
    })
  },

  async confirmReceipt(e) {
    const { id } = e.currentTarget.dataset
    wx.showModal({
      title: '提示',
      content: '确定要确认收货吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            wx.showLoading({ title: '确认中...' })
            await orderApi.confirmReceipt(id)
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
    const { id } = e.currentTarget.dataset
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
