Component({
  properties: {
    activeTab: {
      type: Number,
      value: 0
    }
  },

  data: {
    tabs: [
      {
        id: 0,
        name: '首页',
        url: '/pages/index/index',
        normalIcon: '/images/tab/首页（未选中）.png',
        selectedIcon: '/images/tab/首页 (选中).png',
        badge: 0
      },
      {
        id: 1,
        name: '商城',
        url: '/pages/Product_list_page/Product_list_page',
        normalIcon: '/images/tab/商城 (未选中).png',
        selectedIcon: '/images/tab/商城（选中）.png',
        badge: 0
      },
      {
        id: 2,
        name: '选品',
        url: '/pages/selection/selection',
        normalIcon: '/images/tab/选品 (未选中).png',
        selectedIcon: '/images/tab/选品（选中）.png',
        badge: 0
      },
      {
        id: 3,
        name: '研发',
        url: '/pages/rd/rd',
        normalIcon: '/images/tab/研发 (未选中).png',
        selectedIcon: '/images/tab/研发（选中）.png',
        badge: 0
      },
      {
        id: 4,
        name: '我的',
        url: '/pages/Profile_page/Profile_page',
        normalIcon: '/images/tab/我的 (未选中).png',
        selectedIcon: '/images/tab/我的 (选中).png',
        badge: 0
      }
    ]
  },

  methods: {
    onTabChange(e) {
      const { id, url } = e.currentTarget.dataset
      
      if (id === this.data.activeTab) {
        return
      }

      this.triggerEvent('tabchange', {
        activeTab: id
      })

      wx.switchTab({
        url: url,
        fail: () => {
          wx.redirectTo({
            url: url,
            fail: () => {
              wx.navigateTo({
                url: url
              })
            }
          })
        }
      })
    },

    updateBadge(tabId, count) {
      const tabs = this.data.tabs.map(tab => {
        if (tab.id === tabId) {
          return { ...tab, badge: count }
        }
        return tab
      })
      
      this.setData({ tabs })
    },

    setActiveTab(tabId) {
      this.triggerEvent('tabchange', {
        activeTab: tabId
      })
    }
  }
})
