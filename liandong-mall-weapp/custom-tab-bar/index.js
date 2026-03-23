Component({
  data: {
    selected: 0,
    color: '#999999',
    selectedColor: '#1890ff',
    list: [
      {
        pagePath: '/pages/index/index',
        text: '首页',
        iconPath: '/images/首页 (2).png',
        selectedIconPath: '/images/首页-选中 (1).png'
      },
      {
        pagePath: '/pages/demandList/demandList',
        text: '我的需求',
        iconPath: '/images/我的需求 (3).png',
        selectedIconPath: '/images/我的需求 (1).png'
      }
    ]
  },
  attached() {
    // 组件挂载时检查当前页面
    const pages = getCurrentPages();
    if (pages && pages.length > 0) {
      const currentPage = pages[pages.length - 1];
      // 只使用 route 属性，__route__ 已废弃
      const route = currentPage.route;
      if (route) {
        const index = this.data.list.findIndex(item => {
          const itemPath = item.pagePath.replace(/^\//, '');
          return route === itemPath;
        });
        if (index !== -1 && index !== this.data.selected) {
          this.setData({ selected: index });
        }
      }
    }
  },
  methods: {
    switchTab(e) {
      const data = e.currentTarget.dataset;
      const url = data.path;
      wx.switchTab({ url });
      this.setData({
        selected: data.index
      });
    }
  }
});
