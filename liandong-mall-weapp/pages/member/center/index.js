// 会员中心页
const api = require('../../../utils/api.js');

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
      
      const res = await api.get('/api/user/member');
      
      wx.hideLoading();
      
      if (res.code === 200) {
        const data = res.data;
        this.setData({
          memberInfo: {
            isMember: data.isMember,
            levelCode: data.levelCode,
            levelName: data.levelName,
            discount: data.discount,
            benefits: data.benefits || [],
            upgradeCondition: data.upgradeCondition,
            validStart: data.validStart,
            validEnd: data.validEnd
          },
          currentLevel: data.levelCode || 'normal'
        });
      } else {
        wx.showToast({
          title: res.message || '加载失败',
          icon: 'none'
        });
      }
    } catch (error) {
      wx.hideLoading();
      console.error('加载会员信息失败:', error);
      
      // 使用模拟数据（开发阶段）
      this.setData({
        memberInfo: {
          isMember: true,
          levelCode: 'vip',
          levelName: 'VIP会员',
          discount: 0.95,
          benefits: [
            { type: 'discount', name: '全场95折' },
            { type: 'points', name: '积分翻倍' }
          ],
          upgradeCondition: '完成首单购买自动升级为VIP，享受全场95折优惠',
          validStart: '2024-01-15 10:30:00',
          validEnd: null
        },
        currentLevel: 'vip'
      });
    }
  }
});
