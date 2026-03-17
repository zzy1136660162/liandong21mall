const app = getApp();

Page({
  data: {
    demandId: null,
    demandTitle: '',
    demandNo: '',
    statusText: '',
    statusClass: '',
    progressList: []
  },

  onLoad(options) {
    const { demandId } = options;
    if (!demandId) {
      wx.showToast({
        title: '参数错误',
        icon: 'none'
      });
      wx.navigateBack();
      return;
    }

    this.setData({ demandId });
    this.loadProgress();
  },

  // 加载进度列表
  loadProgress() {
    const { demandId } = this.data;
    const submitterId = app.globalData.userId;

    wx.showLoading({ title: '加载中...' });

    // 先加载需求详情
    app.request({
      url: `/demand/detail/${demandId}?submitterId=${submitterId}`,
      success: (detailRes) => {
        const detail = detailRes.data;
        this.setData({
          demandTitle: detail.title,
          demandNo: detail.demandNo,
          statusText: detail.statusText,
          statusClass: this.getStatusClass(detail.status)
        });

        // 再加载进度
        app.request({
          url: `/demand/progress/${demandId}?submitterId=${submitterId}`,
          success: (progressRes) => {
            wx.hideLoading();
            // 倒序排列，最新的在前面
            const progressList = progressRes.data.reverse();
            this.setData({ progressList });
          },
          fail: () => {
            wx.hideLoading();
          }
        });
      },
      fail: () => {
        wx.hideLoading();
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
  }
});
