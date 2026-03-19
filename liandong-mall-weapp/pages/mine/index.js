// 个人中心页
const api = require('../../utils/api.js');
const user = require('../../utils/user.js');

Page({
  data: {
    isLogin: false,
    userInfo: {
      nickname: '',
      avatar: '',
      phone: '',
      isMember: false,
      memberLevel: null,
      memberLevelName: '普通用户',
      isTalent: false,
      talentStatus: null,
      id: ''
    },
    orderCount: {
      pending: 0,
      shipped: 0,
      received: 0,
      refund: 0
    },
    showUpgradeNotice: false
  },

  onLoad() {
    this.checkLoginStatus();
  },

  onShow() {
    this.checkLoginStatus();
  },

  checkLoginStatus() {
    const isLogin = user.isLogin();
    this.setData({
      isLogin
    });

    if (isLogin) {
      this.loadUserInfo();
      this.loadOrderCount();
    } else {
      this.setData({
        userInfo: {
          nickname: '',
          avatar: '',
          phone: '',
          isMember: false,
          memberLevel: null,
          memberLevelName: '普通用户',
          isTalent: false,
          talentStatus: null,
          id: ''
        },
        orderCount: {
          pending: 0,
          shipped: 0,
          received: 0,
          refund: 0
        }
      });
    }
  },

  async loadUserInfo() {
    try {
      const res = await api.get('/api/user/info');
      if (res.code === 200) {
        const userInfo = res.data;
        const memberLevelMap = {
          0: '普通用户',
          1: 'VIP会员',
          2: 'SVIP会员'
        };
        this.setData({
          userInfo: {
            ...userInfo,
            nickname: userInfo.nickname || '微信用户',
            memberLevelName: memberLevelMap[userInfo.memberLevel] || '普通用户'
          }
        });
        user.setUserInfo(userInfo);
      }
    } catch (error) {
      console.error('加载用户信息失败:', error);
      if (error.message === '登录已过期') {
        this.checkLoginStatus();
      }
    }
  },

  async loadOrderCount() {
    try {
      const res = await api.get('/api/order/count');
      if (res.code === 200) {
        this.setData({
          orderCount: res.data
        });
      }
    } catch (error) {
      console.error('加载订单数量失败:', error);
    }
  },

  goToLogin() {
    wx.navigateTo({
      url: '/pages/login/index?redirect=' + encodeURIComponent('/pages/mine/index')
    });
  },

  checkLoginAndGo(e) {
    const { url, status } = e.currentTarget.dataset;

    // rnd 不需要登录验证
    if (url === 'rnd') {
      this.goToRNDemand();
      return;
    }

    if (!this.data.isLogin) {
      wx.navigateTo({
        url: '/pages/login/index'
      });
      return;
    }

    switch (url) {
      case 'order':
        this.goToOrderList(e);
        break;
      case 'talent':
        this.goToTalentCenter();
        break;
      case 'sample':
        this.goToSampleApplication();
        break;
      case 'address':
        this.goToAddress();
        break;
    }
  },

  handleLogout() {
    user.logout(() => {
      this.setData({
        isLogin: false,
        userInfo: {
          nickname: '',
          avatar: '',
          phone: '',
          isMember: false,
          memberLevel: null,
          memberLevelName: '普通用户',
          isTalent: false,
          talentStatus: null,
          id: ''
        }
      });
    });
  },

  goBack() {
    wx.switchTab({
      url: '/pages/index/index'
    });
  },

  goToMemberCenter() {
    if (!this.data.isLogin) {
      this.goToLogin();
      return;
    }
    wx.navigateTo({
      url: '/pages/member/center/index'
    });
  },

  goToOrderList(e) {
    const status = e.currentTarget.dataset.status;
    let url = '/pages/order/list/index';
    if (status) {
      url += `?status=${status}`;
    }
    wx.navigateTo({ url });
  },

  goToFavorites() {
    wx.navigateTo({
      url: '/pages/favorites/index'
    });
  },

  goToHistory() {
    wx.navigateTo({
      url: '/pages/history/index'
    });
  },

  goToComments() {
    wx.navigateTo({
      url: '/pages/comments/index'
    });
  },

  goToCustomer() {
    wx.navigateTo({
      url: '/pages/customer/index'
    });
  },

  goToMemberCard() {
    wx.navigateTo({
      url: '/pages/member/card/index'
    });
  },

  goToDynamicCode() {
    wx.navigateTo({
      url: '/pages/dynamic/code/index'
    });
  },

  goToMyGroup() {
    wx.navigateTo({
      url: '/pages/group/my/index'
    });
  },

  goToMyProject() {
    wx.navigateTo({
      url: '/pages/project/my/index'
    });
  },

  goToSignIn() {
    wx.navigateTo({
      url: '/pages/signin/index'
    });
  },

  goToMaterial() {
    wx.navigateTo({
      url: '/pages/material/index'
    });
  },

  goToActivity() {
    wx.navigateTo({
      url: '/pages/activity/index'
    });
  },

  goToMore() {
    wx.navigateTo({
      url: '/pages/more/index'
    });
  },

  goToSettings() {
    wx.navigateTo({
      url: '/pages/settings/index'
    });
  },

  goToTalentCenter() {
    wx.navigateTo({
      url: '/pages/talent/center/index'
    });
  },

  goToSampleApplication() {
    wx.navigateTo({
      url: '/pages/sample/application/index'
    });
  },

  goToRNDemand() {
    wx.switchTab({
      url: '/pages/rd_index/rd_index'
    });
  },

  goToRNDemandDirect() {
    wx.switchTab({
      url: '/pages/rd_index/rd_index'
    });
  },

  goToAddress() {
    wx.navigateTo({
      url: '/pages/address/list/index'
    });
  },

  goToCustomerService() {
    wx.navigateTo({
      url: '/pages/chat/chat'
    });
  }
});
