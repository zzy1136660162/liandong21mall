Page({
  data: {
    activeTabName: '首页',
    tabConfig: [
      {
        id: 0,
        name: '首页',
        path: '/pages/index/index',
        selectedIcon: '/images/tab/首页 (选中).png'
      },
      {
        id: 1,
        name: '商城',
        path: '/pages/Product_list_page/Product_list_page',
        selectedIcon: '/images/tab/商城（选中）.png'
      },
      {
        id: 2,
        name: '选品',
        path: '/pages/selection/selection',
        selectedIcon: '/images/tab/选品（选中）.png'
      },
      {
        id: 3,
        name: '研发',
        path: '/pages/rd/rd',
        selectedIcon: '/images/tab/研发（选中）.png'
      },
      {
        id: 4,
        name: '我的',
        path: '/pages/Profile_page/Profile_page',
        selectedIcon: '/images/tab/我的 (选中).png'
      }
    ]
  },

  onLoad(options) {
    const pages = getCurrentPages()
    const currentPage = pages[pages.length - 1]
    const route = currentPage.route

    const tabMap = {
      'pages/index/index': 0,
      'pages/Product_list_page/Product_list_page': 1,
      'pages/selection/selection': 2,
      'pages/rd/rd': 3,
      'pages/Profile_page/Profile_page': 4
    }

    const tabNames = ['首页', '商城', '选品', '研发', '我的']

    const activeTab = tabMap[route] || 0

    this.setData({
      activeTabName: tabNames[activeTab]
    })
  }
})
