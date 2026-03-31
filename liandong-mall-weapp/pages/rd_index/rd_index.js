// rd_index.js
const app = getApp()

Page({
  data: {
    recentDemands: []
  },
  onLoad() {
    this.loadRecentDemands()
  },
  loadRecentDemands() {
    wx.request({
      url: `${app.globalData.apiBaseUrl}/demand/list`,
      method: 'GET',
      data: {
        page: 1,
        pageSize: 3
      },
      success: (res) => {
        if (res.data.code === 200 && res.data.data) {
          this.setData({
            recentDemands: res.data.data.list || []
          })
        }
      },
      fail: (err) => {
        console.error('加载需求列表失败', err)
      }
    })
  },
  goToSubmit() {
    // 检查是否已登录
    const token = wx.getStorageSync('token')
    if (!token) {
      wx.navigateTo({
        url: '/pages/login/index'
      })
      return
    }
    wx.navigateTo({
      url: '/pages/demandSubmit/demandSubmit'
    })
  },
  goToList() {
    wx.navigateTo({
      url: '/pages/demandList/demandList'
    })
  },
  goToDetail(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/demandDetail/demandDetail?id=${id}`
    })
  },
  goToChat() {
    wx.navigateTo({
      url: '/pages/chat/chat'
    })
  }
})