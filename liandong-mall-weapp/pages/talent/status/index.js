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
      
      const data = await api.get('/api/user/talent/status');
      
      wx.hideLoading();
      
      if (data) {
        this.setData({
          status: data.status,
          statusText: data.statusText,
          applyTime: data.applyTime,
          auditTime: data.auditTime,
          rejectReason: data.rejectReason
        });
      } else {
        this.setData({
          status: 'NONE',
          statusText: '未申请',
          applyTime: '',
          auditTime: '',
          rejectReason: ''
        });
      }
    } catch (error) {
      wx.hideLoading();
      console.error('加载状态失败:', error);
      
      this.setData({
        status: 'NONE',
        statusText: '未申请',
        applyTime: '',
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
