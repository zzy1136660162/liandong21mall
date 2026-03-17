const app = getApp();

Page({
  data: {
    recentDemands: []
  },

  onLoad() {
    this.loadRecentDemands();
  },

  onShow() {
    this.loadRecentDemands();
  },

  // 加载最近的需求
  loadRecentDemands() {
    const submitterId = app.globalData.userId;
    
    app.request({
      url: `/demand/list?submitterId=${submitterId}&page=1&pageSize=3`,
      success: (res) => {
        const demands = res.data.list.map(item => ({
          ...item,
          statusClass: this.getStatusClass(item.status)
        }));
        this.setData({
          recentDemands: demands
        });
      }
    });
  },

  // 获取状态样式类名
  getStatusClass(status) {
    const classMap = {
      0: 'pending',
      1: 'confirming',
      2: 'developing',
      3: 'sampling',
      4: 'completed',
      5: 'cancelled'
    };
    return classMap[status] || 'pending';
  },

  // 跳转到提交页面
  goToSubmit() {
    wx.navigateTo({
      url: '/pages/demandSubmit/demandSubmit'
    });
  },

  // 跳转到列表页面
  goToList() {
    wx.switchTab({
      url: '/pages/demandList/demandList'
    });
  },

  // 跳转到详情页面
  goToDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/demandDetail/demandDetail?id=${id}`
    });
  }
});
