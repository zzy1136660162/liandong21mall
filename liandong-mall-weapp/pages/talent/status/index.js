// 达人申请状态页
const { api } = require('../../../utils/api.js');

Page({
  data: {
    status: null,
    statusText: '',
    applyTime: '',
    auditTime: '',
    rejectReason: ''
  },

  onLoad() {
    this.loadStatus();
  },

  onShow() {
    this.loadStatus();
  },

  // 加载状态
  async loadStatus() {
    try {
      wx.showLoading({ title: '加载中' });
      
      const res = await api.get('/api/user/talent/status');
      
      wx.hideLoading();
      
      if (res.code === 200) {
        this.setData({
          status: res.data.status,
          statusText: res.data.statusText,
          applyTime: res.data.applyTime,
          auditTime: res.data.auditTime,
          rejectReason: res.data.rejectReason
        });
      }
    } catch (error) {
      wx.hideLoading();
      console.error('加载状态失败:', error);
      
      // 模拟数据
      this.setData({
        status: 'PENDING',
        statusText: '审核中',
        applyTime: '2024-01-15 10:30:00',
        auditTime: '',
        rejectReason: ''
      });
    }
  },

  // 返回
  goBack() {
    wx.navigateBack();
  },

  // 进入达人中心
  goToTalentCenter() {
    wx.navigateTo({
      url: '/pages/talent/center/index'
    });
  },

  // 重新申请
  reApply() {
    wx.redirectTo({
      url: '/pages/talent/apply/index'
    });
  },

  // 立即申请
  goToApply() {
    wx.navigateTo({
      url: '/pages/talent/apply/index'
    });
  }
});
