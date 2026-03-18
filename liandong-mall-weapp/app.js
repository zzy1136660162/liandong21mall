App({
  globalData: {
    userInfo: null,
    apiBaseUrl: 'http://127.0.0.1:5000',
    userId: null
  },

  onLaunch() {
    // 获取用户ID
    this.globalData.userId = wx.getStorageSync('userId') || this.generateUserId();
    wx.setStorageSync('userId', this.globalData.userId);
    
    console.log('当前用户ID:', this.globalData.userId);
  },

  // 生成临时用户ID
  generateUserId() {
    return 'USER_' + Date.now();
  },

  // 全局请求方法 - 使用真实后端 API
  request(options) {
    const { url, method = 'GET', data, success, fail, complete } = options;
    console.log('app.js request called, url:', url);

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
        if (res.statusCode === 200 && res.data.code === 200) {
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
