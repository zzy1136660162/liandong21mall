// 达人中心页
const api = require('../../../utils/api.js');

Page({
  data: {
    talentInfo: {
      avatar: '',
      realName: '张三',
      region: '湖北省武汉市',
      auditTime: '2024-01-15'
    },
    stats: {
      promotionCount: 0,
      sampleCount: 0,
      demandCount: 0
    }
  },

  onLoad() {
    this.loadTalentInfo();
  },

  onShow() {
    this.loadTalentInfo();
  },

  // 加载达人信息
  loadTalentInfo() {
    wx.showLoading({ title: '加载中' });
    
    api.get('/api/user/talent/info')
      .then(res => {
        wx.hideLoading();
        if (res.code === 200) {
          this.setData({
            talentInfo: res.data.talentInfo || this.data.talentInfo,
            stats: res.data.stats || this.data.stats
          });
        }
      })
      .catch(error => {
        wx.hideLoading();
        console.error('加载达人信息失败:', error);
      });
  },

  // 跳转到选品池
  goToSelectionPool() {
    wx.navigateTo({
      url: '/pages/selection/pool/index'
    });
  },

  // 跳转到样品申请
  goToSampleApply() {
    wx.navigateTo({
      url: '/pages/sample/apply/index'
    });
  },

  // 跳转到研发需求
  goToRdDemand() {
    wx.navigateTo({
      url: '/pages/rd/demand/index'
    });
  }
});
