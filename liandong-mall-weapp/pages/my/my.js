Page({
  data: {
    sampleCount: 3
  },

  onLoad() {
    // 页面加载时获取数据
    this.loadUserData();
  },

  // 加载用户数据
  loadUserData() {
    // 这里可以从服务器获取真实的用户数据
    console.log('加载用户数据');
  },

  // 跳转到收益明细
  goToIncome() {
    wx.showToast({
      title: '收益明细开发中',
      icon: 'none'
    });
  },

  // 跳转到提现
  goToWithdraw() {
    wx.showToast({
      title: '提现功能开发中',
      icon: 'none'
    });
  },

  // 跳转到我的样品
  goToMySamples() {
    wx.navigateTo({
      url: '/pages/my-samples/my-samples'
    });
  },

  // 跳转到申请记录
  goToSampleApply() {
    wx.navigateTo({
      url: '/pages/my-samples/my-samples'
    });
  }
});
