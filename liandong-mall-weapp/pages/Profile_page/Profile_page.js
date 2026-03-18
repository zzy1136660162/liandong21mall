Page({
  data: {
    orderCounts: {
      pending: 3,
      shipping: 2,
      receiving: 1,
      review: 5
    }
  },

  onLoad(options) {
    
  },

  onSettingsTap() {
    wx.showToast({
      title: '功能开发中',
      icon: 'none',
      duration: 2000
    })
  },

  onAddressTap() {
    wx.showToast({
      title: '功能开发中',
      icon: 'none',
      duration: 2000
    })
  },

  onAboutTap() {
    wx.showToast({
      title: '功能开发中',
      icon: 'none',
      duration: 2000
    })
  },

  onFeedbackTap() {
    wx.showToast({
      title: '功能开发中',
      icon: 'none',
      duration: 2000
    })
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

    if (activeTab !== 4) {
      wx.switchTab({
        url: tabPaths[activeTab]
      })
    }
  }
})
