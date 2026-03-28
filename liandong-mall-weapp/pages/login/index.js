// 登录页面
const { api } = require('../../utils/api');

Page({
  data: {
    phone: '',
    code: '',
    codeText: '获取验证码',
    codeDisabled: false,
    countdown: 60,
    agreed: false,
    loading: false
  },

  onLoad(options) {
    // 检查是否从其他页面跳转过来
    const redirect = options.redirect || '';
    this.setData({
      redirect
    });
  },

  onPhoneInput(e) {
    this.setData({
      phone: e.detail.value
    });
  },

  onCodeInput(e) {
    this.setData({
      code: e.detail.value
    });
  },

  toggleAgreement() {
    this.setData({
      agreed: !this.data.agreed
    });
  },

  sendCode() {
    const phone = this.data.phone;

    if (!phone) {
      wx.showToast({
        title: '请输入手机号',
        icon: 'none'
      });
      return;
    }

    if (!/^1[3-9]\d{9}$/.test(phone)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none'
      });
      return;
    }

    if (this.data.codeDisabled) {
      return;
    }

    api.post('/api/auth/send-code', { phone }, { showLoading: true })
      .then(res => {
        wx.showToast({
          title: '验证码已发送',
          icon: 'success'
        });
        this.startCountdown();
      })
      .catch(err => {
        console.error('发送验证码失败:', err);
        wx.showToast({
          title: '发送失败，请重试',
          icon: 'none'
        });
      });
  },

  startCountdown() {
    this.setData({
      codeDisabled: true,
      countdown: 60
    });

    const timer = setInterval(() => {
      const countdown = this.data.countdown - 1;
      if (countdown <= 0) {
        clearInterval(timer);
        this.setData({
          codeText: '获取验证码',
          codeDisabled: false,
          countdown: 60
        });
      } else {
        this.setData({
          codeText: `${countdown}s后重新获取`,
          countdown: countdown
        });
      }
    }, 1000);
  },

  handleLogin() {
    const { phone, code, agreed, redirect } = this.data;

    if (!phone) {
      wx.showToast({
        title: '请输入手机号',
        icon: 'none'
      });
      return;
    }

    if (!/^1[3-9]\d{9}$/.test(phone)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none'
      });
      return;
    }

    if (!code) {
      wx.showToast({
        title: '请输入验证码',
        icon: 'none'
      });
      return;
    }

    if (!agreed) {
      wx.showToast({
        title: '请先同意用户协议',
        icon: 'none'
      });
      return;
    }

    this.setData({
      loading: true
    });

    api.post('/api/auth/login', { phone, code }, { showLoading: true })
      .then(res => {
        const token = res.token;
        const userInfo = res.userInfo;
        const userId = res.userId || (userInfo && userInfo.userId);

        wx.setStorageSync('token', token);
        wx.setStorageSync('userInfo', userInfo);
        wx.setStorageSync('userId', userId);

        wx.showToast({
          title: '登录成功',
          icon: 'success'
        });

        setTimeout(() => {
          const url = decodeURIComponent(redirect);
          
          const tabBarPages = ['/pages/mine/index', '/pages/index/index', '/pages/xuanpinindex/xuanpinindex', '/pages/rd_index/rd_index', '/pages/Product_list_page/Product_list_page'];
          
          if (tabBarPages.includes(url)) {
            wx.switchTab({ url });
          } else if (url.startsWith('/pages')) {
            const pages = getCurrentPages();
            const redirectPath = url.split('?')[0];
            
            let pageExists = false;
            for (let i = 0; i < pages.length - 1; i++) {
              if (pages[i].route === redirectPath || pages[i].route === redirectPath.slice(1)) {
                pageExists = true;
                break;
              }
            }
            
            if (pageExists) {
              wx.navigateBack({ delta: 1 });
            } else {
              wx.redirectTo({ url });
            }
          } else {
            wx.switchTab({ url: '/pages/mine/index' });
          }
        }, 1500);
      })
      .catch(err => {
        console.error('登录失败:', err);
        wx.showToast({
          title: '登录失败，请重试',
          icon: 'none'
        });
      })
      .finally(() => {
        this.setData({
          loading: false
        });
      });
  },

  wechatLogin() {
    const { agreed } = this.data;

    if (!agreed) {
      wx.showToast({
        title: '请先同意用户协议',
        icon: 'none'
      });
      return;
    }

    wx.showLoading({
      title: '登录中...',
      mask: true
    });

    // 调用微信登录获取 code
    wx.login({
      success: (res) => {
        if (res.code) {
          // 获取用户信息
          this.getWechatUserInfo(res.code);
        } else {
          wx.hideLoading();
          wx.showToast({
            title: '微信登录失败',
            icon: 'none'
          });
        }
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({
          title: '微信登录失败',
          icon: 'none'
        });
      }
    });
  },

  getWechatUserInfo(wxCode) {
    // 获取用户信息
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        const userInfo = res.userInfo;
        this.doWechatLogin(wxCode, userInfo);
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({
          title: '需要授权才能登录',
          icon: 'none'
        });
      }
    });
  },

  doWechatLogin(wxCode, userInfo) {
    const { redirect } = this.data;

    api.post('/api/auth/wechat-login', {
      code: wxCode,
      nickname: userInfo.nickName,
      avatar: userInfo.avatarUrl,
      gender: userInfo.gender,
      country: userInfo.country,
      province: userInfo.province,
      city: userInfo.city
    }, { showLoading: false })
      .then(res => {
        wx.hideLoading();

        const { token, userInfo: serverUserInfo, userId } = res;

        wx.setStorageSync('token', token);
        wx.setStorageSync('userInfo', serverUserInfo);
        wx.setStorageSync('userId', userId);

        wx.showToast({
          title: '登录成功',
          icon: 'success'
        });

        setTimeout(() => {
          if (redirect && redirect !== '/pages/login/index') {
            const url = decodeURIComponent(redirect);
            if (url.startsWith('/pages')) {
              const pages = getCurrentPages();
              const redirectPath = url.split('?')[0];
              
              let pageExists = false;
              for (let i = 0; i < pages.length - 1; i++) {
                if (pages[i].route === redirectPath) {
                  pageExists = true;
                  break;
                }
              }
              
              if (pageExists) {
                wx.navigateBack({ delta: 1 });
              } else {
                wx.redirectTo({ url });
              }
            } else {
              wx.switchTab({ url: '/pages/mine/index' });
            }
          } else {
            wx.switchTab({ url: '/pages/mine/index' });
          }
        }, 1500);
      })
      .catch(err => {
        wx.hideLoading();
        console.error('微信登录失败:', err);
        wx.showToast({
          title: '登录失败，请重试',
          icon: 'none'
        });
      });
  },

  goToAgreement() {
    wx.showToast({
      title: '用户协议页面开发中',
      icon: 'none'
    });
  },

  goToPrivacy() {
    wx.showToast({
      title: '隐私政策页面开发中',
      icon: 'none'
    });
  }
});
