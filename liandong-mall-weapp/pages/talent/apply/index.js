// 达人申请页
const api = require('../../../utils/api.js');

Page({
  data: {
    formData: {
      realName: '',
      phone: '',
      applyReason: '',
      intro: ''
    },
    region: [],
    isSubmitting: false
  },

  onLoad() {
  },

  // 输入框变化
  onInputChange(e) {
    const { field } = e.currentTarget.dataset;
    const { value } = e.detail;
    
    this.setData({
      [`formData.${field}`]: value
    });
  },

  // 地区选择变化
  onRegionChange(e) {
    this.setData({
      region: e.detail.value
    });
  },

  // 打开地区选择器
  openRegionPicker() {
    wx.chooseLocation({
      success: (res) => {
        this.setData({
          region: [res.province, res.city, res.district]
        });
      }
    });
  },

  // 提交申请
  async submitApply() {
    if (this.data.isSubmitting) {
      return;
    }

    const { formData } = this.data;
    
    // 检查必填字段
    if (!formData.realName) {
      wx.showToast({
        title: '请输入真实姓名',
        icon: 'none'
      });
      return;
    }

    if (formData.realName.length < 2 || formData.realName.length > 20) {
      wx.showToast({
        title: '真实姓名需在2-20个字符之间',
        icon: 'none'
      });
      return;
    }

    if (!formData.phone) {
      wx.showToast({
        title: '请输入手机号码',
        icon: 'none'
      });
      return;
    }

    if (!/^1[3-9]\d{9}$/.test(formData.phone)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none'
      });
      return;
    }

    if (!formData.applyReason) {
      wx.showToast({
        title: '请输入申请理由',
        icon: 'none'
      });
      return;
    }

    if (formData.applyReason.length < 10 || formData.applyReason.length > 500) {
      wx.showToast({
        title: '申请理由需在10-500个字符之间',
        icon: 'none'
      });
      return;
    }

    this.setData({ isSubmitting: true });

    try {
      const params = {
        realName: formData.realName,
        phone: formData.phone,
        region: this.data.region.length > 0 ? `${this.data.region[0]} ${this.data.region[1]} ${this.data.region[2]}` : '',
        applyReason: formData.applyReason,
        intro: formData.intro
      };

      const res = await api.post('/api/user/talent/apply', params);

      if (res.code === 200) {
        wx.showToast({
          title: '申请提交成功',
          icon: 'success'
        });
        
        // 跳转到状态页
        setTimeout(() => {
          wx.redirectTo({
            url: '/pages/talent/status/index'
          });
        }, 1500);
      } else {
        wx.showToast({
          title: res.message || '提交失败',
          icon: 'none'
        });
        this.setData({ isSubmitting: false });
      }
    } catch (error) {
      console.error('提交申请失败:', error);
      wx.showToast({
        title: '网络错误，请重试',
        icon: 'none'
      });
      this.setData({ isSubmitting: false });
    }
  }
});
