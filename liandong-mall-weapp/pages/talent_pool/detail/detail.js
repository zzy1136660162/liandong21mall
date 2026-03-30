const app = getApp();

Page({
  data: {
    talentId: null,
    talentInfo: null,
    loading: true
  },

  onLoad(options) {
    const { id } = options;
    if (id) {
      this.setData({ talentId: parseInt(id) });
      this.loadTalentDetail();
    } else {
      wx.showToast({
        title: '参数错误',
        icon: 'none'
      });
      setTimeout(() => {
        wx.navigateBack();
      }, 1500);
    }
  },

  loadTalentDetail() {
    wx.showLoading({ title: '加载中...' });

    app.request({
      url: `/api/talent_pool/detail/${this.data.talentId}`,
      success: (res) => {
        wx.hideLoading();
        if (res.data) {
          this.setData({
            talentInfo: res.data,
            loading: false
          });
        } else {
          wx.showToast({
            title: '人才信息不存在',
            icon: 'none'
          });
          setTimeout(() => {
            wx.navigateBack();
          }, 1500);
        }
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({
          title: '加载失败',
          icon: 'none'
        });
        this.setData({ loading: false });
      }
    });
  },

  onShareAppMessage() {
    const { talentInfo } = this.data;
    return {
      title: `${talentInfo.name} - ${talentInfo.title}`,
      path: `/pages/talent_pool/detail/detail?id=${this.data.talentId}`
    };
  }
});
