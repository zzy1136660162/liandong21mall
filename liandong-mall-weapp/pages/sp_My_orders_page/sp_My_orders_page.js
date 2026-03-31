
const orderApi = require('../../utils/sp_api.js').orderApi
const { checkLogin, getLoginStatus } = require('../../utils/sp_auth.js')

const DEFAULT_PRODUCT_IMAGE = '/static/images/products/product_1_main.jpg'

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
    useMockData: false,
    isLoading: false,
    isLoggedIn: false,
    searchKeyword: '',
    showSearch: false,
    orderStatistics: null
  },

  onLoad(options) {
    const loginStatus = getLoginStatus()
    this.setData({ isLoggedIn: loginStatus.isLoggedIn })
    
    if (!loginStatus.isLoggedIn) {
      checkLogin({ showToast: true })
      return
    }
    
    const { tab } = options
    if (tab) {
      this.setData({ currentTab: tab })
    }
    this.loadOrders()
    this.loadOrderStatistics()
  },

  onShow() {
    const loginStatus = getLoginStatus()
    this.setData({ isLoggedIn: loginStatus.isLoggedIn })
    
    if (loginStatus.isLoggedIn) {
      this.loadOrders()
    }
  },

  onPullDownRefresh() {
    this.setData({ page: 1, hasMore: true })
    Promise.all([
      this.loadOrders(),
      this.loadOrderStatistics()
    ]).finally(() => {
      wx.stopPullDownRefresh()
    })
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.isLoading) {
      this.loadMoreOrders()
    }
  },

  async loadOrderStatistics() {
    try {
      const statistics = await orderApi.getOrderStatistics()
      if (statistics) {
        this.setData({ orderStatistics: statistics })
        wx.setStorageSync('orderStatistics', statistics)
      }
    } catch (error) {
      console.error('加载订单统计失败:', error)
      const cachedStatistics = wx.getStorageSync('orderStatistics')
      if (cachedStatistics) {
        this.setData({ orderStatistics: cachedStatistics })
      }
    }
  },

  async loadOrders() {
    if (this.data.isLoading) return
    
    try {
      this.setData({ isLoading: true })
      wx.showLoading({ title: '加载中...' })
      
      const { currentTab, page, pageSize, searchKeyword } = this.data
      const status = currentTab === 'all' ? null : currentTab
      
      let res
      if (searchKeyword) {
        res = await orderApi.searchOrders(searchKeyword, page, pageSize)
      } else {
        res = await orderApi.getOrderList(status, page, pageSize)
      }
      
      let orders = []
      if (res) {
        if (Array.isArray(res)) {
          orders = res
        } else if (res.list && Array.isArray(res.list)) {
          orders = res.list
        } else if (res.orders && Array.isArray(res.orders)) {
          orders = res.orders
        } else {
          orders = [res]
        }
      }
      
      const orderList = orders.map(order => ({
        ...order,
        statusText: this.getStatusText(order.status)
      }))

      if (page === 1) {
        this.setData({ orderList })
        wx.setStorageSync('orderList', orderList)
      } else {
        this.setData({
          orderList: [...this.data.orderList, ...orderList]
        })
      }

      this.setData({
        hasMore: orders.length >= pageSize,
        useMockData: false
      })
      
      wx.hideLoading()
    } catch (error) {
      console.error('加载订单列表失败:', error)
      wx.hideLoading()
      
      if (page === 1) {
        const cachedOrders = wx.getStorageSync('orderList')
        if (cachedOrders && cachedOrders.length > 0) {
          this.setData({ orderList: cachedOrders })
          wx.showToast({
            title: '数据加载失败，已显示缓存',
            icon: 'none'
          })
          return
        }
      }
      
      this.setData({ useMockData: true })
      this.loadMockData()
      wx.showToast({
        title: '网络异常，请检查网络',
        icon: 'none'
      })
    } finally {
      this.setData({ isLoading: false })
    }
  },

  async loadMoreOrders() {
    this.setData({
      page: this.data.page + 1
    })
    await this.loadOrders()
  },

  loadMockData() {
    const { currentTab } = this.data
    let mockOrders = []

    if (currentTab === 'all' || currentTab === 'PENDING_PAY') {
      mockOrders.push({
        orderId: 1,
        orderNo: 'ORD20240320001',
        status: 'PENDING_PAY',
        statusText: '待付款',
        createTime: '2024-03-20 10:30:00',
        products: [
          {
            productId: 42,
            productName: '焕颜修护精华液',
            productImage: DEFAULT_PRODUCT_IMAGE,
            skuName: '30ml',
            price: 299.00,
            quantity: 2
          }
        ],
        finalAmount: 598.00,
        remainingSeconds: 1800
      })
    }

    if (currentTab === 'all' || currentTab === 'PAID') {
      mockOrders.push({
        orderId: 2,
        orderNo: 'ORD20240319001',
        status: 'PAID',
        statusText: '待发货',
        createTime: '2024-03-19 15:20:00',
        products: [
          {
            productId: 43,
            productName: '水感透白面霜',
            productImage: DEFAULT_PRODUCT_IMAGE,
            skuName: '50g',
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
        orderNo: 'ORD20240318001',
        status: 'SHIPPED',
        statusText: '待收货',
        createTime: '2024-03-18 09:15:00',
        products: [
          {
            productId: 44,
            productName: '紧致眼霜',
            productImage: DEFAULT_PRODUCT_IMAGE,
            skuName: '15ml',
            price: 159.00,
            quantity: 1
          }
        ],
        finalAmount: 159.00,
        logisticsCompany: '顺丰速运',
        logisticsNo: 'SF1234567890'
      })
    }

    if (currentTab === 'all' || currentTab === 'FINISHED') {
      mockOrders.push({
        orderId: 4,
        orderNo: 'ORD20240315001',
        status: 'FINISHED',
        statusText: '已完成',
        createTime: '2024-03-15 14:45:00',
        products: [
          {
            productId: 45,
            productName: '温和洁面乳',
            productImage: DEFAULT_PRODUCT_IMAGE,
            skuName: '100ml',
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
        orderNo: 'ORD20240321001',
        status: 'CANCELLED',
        statusText: '已取消',
        createTime: '2024-03-21 09:30:00',
        products: [
          {
            productId: 46,
            productName: '补水面膜',
            productImage: DEFAULT_PRODUCT_IMAGE,
            skuName: '5片装',
            price: 69.00,
            quantity: 1
          }
        ],
        finalAmount: 69.00,
        cancelReason: '用户主动取消'
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
      hasMore: true,
      searchKeyword: '',
      showSearch: false
    })
    this.loadOrders()
  },

  onSearchInput(e) {
    this.setData({
      searchKeyword: e.detail.value
    })
  },

  onSearchConfirm(e) {
    const { value } = e.detail
    this.setData({
      searchKeyword: value,
      page: 1,
      hasMore: true
    })
    this.loadOrders()
  },

  toggleSearch() {
    this.setData({
      showSearch: !this.data.showSearch
    })
    if (!this.data.showSearch) {
      this.setData({
        searchKeyword: '',
        page: 1,
        hasMore: true
      })
      this.loadOrders()
    }
  },

  clearSearch() {
    this.setData({
      searchKeyword: '',
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
    
    if (!orderid) {
      wx.showToast({
        title: '订单ID错误',
        icon: 'none'
      })
      return
    }
    
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
            
            this.setData({ page: 1, hasMore: true })
            this.loadOrders()
            this.loadOrderStatistics()
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
