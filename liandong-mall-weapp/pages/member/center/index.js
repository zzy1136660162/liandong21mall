// 会员中心页
const { api } = require('../../../utils/api.js');

Page({
  data: {
    memberInfo: {
      isMember: false,
      levelCode: '',
      levelName: '',
      discount: 1.0,
      benefits: [],
      upgradeCondition: '',
      validStart: '',
      validEnd: ''
    },
    currentLevel: 'normal'
  },

  onLoad() {
    this.loadMemberInfo();
  },

  onShow() {
    this.loadMemberInfo();
  },

  // 加载会员信息
  async loadMemberInfo() {
    try {
      wx.showLoading({ title: '加载中' });

      const userInfo = await api.get('/api/user/info');

      wx.hideLoading();

      const memberLevel = userInfo.memberLevel || {};

      this.setData({
        memberInfo: {
          isMember: userInfo.isMember || false,
          levelCode: memberLevel.levelCode || 'normal',
          levelName: memberLevel.levelName || '普通用户',
          discount: memberLevel.discount || 1.0,
          benefits: memberLevel.benefits || [],
          upgradeCondition: memberLevel.upgradeCondition || '完成首单购买自动升级为VIP',
          validStart: memberLevel.validStart || '',
          validEnd: memberLevel.validEnd || ''
        },
        currentLevel: memberLevel.levelCode || 'normal'
      });
    } catch (error) {
      wx.hideLoading();
      console.error('加载会员信息失败:', error);
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    }
  }
});
