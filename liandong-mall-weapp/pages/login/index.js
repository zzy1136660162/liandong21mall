// 登录页面
const api = require('../../utils/api');

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
        if (res.code === 200) {
          wx.showToast({
            title: '验证码已发送',
            icon: 'success'
          });
          this.startCountdown();
        } else {
          wx.showToast({
            title: res.message || '发送失败',
            icon: 'none'
          });
        }
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
        if (res.code === 200) {
          const { token, userInfo } = res.data;

          wx.setStorageSync('token', token);
          wx.setStorageSync('userInfo', userInfo);

          wx.showToast({
            title: '登录成功',
            icon: 'success'
          });

          setTimeout(() => {
            if (redirect) {
              wx.redirectTo({
                url: decodeURIComponent(redirect)
              });
            } else {
              wx.switchTab({
                url: '/pages/index/index'
              });
            }
          }, 1500);
        } else {
          wx.showToast({
            title: res.message || '登录失败',
            icon: 'none'
          });
        }
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
        if (res.code === 200) {
          const { token, userInfo: serverUserInfo } = res.data;

          wx.setStorageSync('token', token);
          wx.setStorageSync('userInfo', serverUserInfo);

          wx.showToast({
            title: '登录成功',
            icon: 'success'
          });

          setTimeout(() => {
            if (redirect) {
              wx.redirectTo({
                url: decodeURIComponent(redirect)
              });
            } else {
              wx.switchTab({
                url: '/pages/index/index'
              });
            }
          }, 1500);
        } else {
          wx.showToast({
            title: res.message || '登录失败',
            icon: 'none'
          });
        }
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
