// 达人中心页
const { talentApi } = require('../../../utils/api.js');

Page({
  data: {
    isTalent: false,
    talentInfo: {
      avatar: '',
      realName: '',
      region: '',
      auditTime: ''
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
    
    talentApi.getTalentInfo()
      .then(data => {
        wx.hideLoading();
        if (data && data.isTalent) {
          this.setData({
            isTalent: true,
            talentInfo: data.talentInfo || this.data.talentInfo,
            stats: data.stats || this.data.stats
          });
        } else {
          this.setData({
            isTalent: false,
            talentInfo: {
              avatar: '',
              realName: '',
              region: '',
              auditTime: ''
            },
            stats: {
              promotionCount: 0,
              sampleCount: 0,
              demandCount: 0
            }
          });
        }
      })
      .catch(error => {
        wx.hideLoading();
        console.log('不是达人或加载失败:', error);
        this.setData({
          isTalent: false,
          talentInfo: {
            avatar: '',
            realName: '',
            region: '',
            auditTime: ''
          },
          stats: {
            promotionCount: 0,
            sampleCount: 0,
            demandCount: 0
          }
        });
      });
  },

  // 跳转到选品池
  goToSelectionPool() {
    wx.switchTab({
      url: '/pages/xuanpinindex/xuanpinindex'
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
    wx.switchTab({
      url: '/pages/rd_index/rd_index'
    });
  },

  // 跳转到达人申请页面
  goToApply() {
    wx.navigateTo({
      url: '/pages/talent/apply/index'
    });
  }
});
