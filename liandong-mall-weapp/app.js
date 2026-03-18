const { mockRequest } = require('./utils/mockApi');

// 是否使用模拟数据（当后端服务不可用时设为 true）
const USE_MOCK = true;

App({
  globalData: {
    userInfo: null,
    apiBaseUrl: 'http://localhost:3000/',
    userId: null
  },

  onLaunch() {
    // 模拟登录，获取用户ID
    // 实际项目中这里应该调用微信登录接口
    this.globalData.userId = wx.getStorageSync('userId') || this.generateUserId();
    wx.setStorageSync('userId', this.globalData.userId);
    
    console.log('当前用户ID:', this.globalData.userId);
    console.log('使用模拟数据:', USE_MOCK);
  },

  // 生成临时用户ID（仅用于演示）
  generateUserId() {
    return 'USER_' + Date.now();
  },

  // 全局请求方法
  request(options) {
    const { url, method = 'GET', data, success, fail, complete } = options;
    console.log('app.js request called, USE_MOCK:', USE_MOCK, 'url:', url);

    // 如果使用模拟数据
    if (USE_MOCK) {
      console.log('app.js 使用模拟数据');
      mockRequest({
        url,
        method,
        data,
        success: (res) => {
          console.log('app.js mockRequest success:', res);
          console.log('app.js res.code:', res.code);
          console.log('app.js res.data:', res.data);
          if (res.code === 0) {
            // 模拟 wx.request 的返回格式 { data: { code, message, data } }
            const result = { data: res.data };
            console.log('app.js 调用页面success，数据:', result);
            success && success(result);
          } else {
            wx.showToast({
              title: res.message || '请求失败',
              icon: 'none'
            });
            fail && fail(res);
          }
          complete && complete();
        },
        fail: (err) => {
          wx.showToast({
            title: '请求失败',
            icon: 'none'
          });
          fail && fail(err);
          complete && complete();
        }
      });
      return;
    }

    // 真实 API 请求
    const baseUrl = this.globalData.apiBaseUrl;
    wx.request({
      url: baseUrl + url,
      method,
      data,
      header: {
        'Content-Type': 'application/json'
      },
      success: (res) => {
        if (res.statusCode === 200 && res.data.code === 0) {
          success && success(res.data);
        } else {
          wx.showToast({
            title: res.data.message || '请求失败',
            icon: 'none'
          });
          fail && fail(res);
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '网络请求失败',
          icon: 'none'
        });
        fail && fail(err);
      },
      complete
    });
  }
});
