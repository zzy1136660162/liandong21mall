const app = getApp();

Page({
  data: {
    form: {
      title: '',
      functionalAppeal: '',
      targetAudience: '',
      dosageFormPreference: '',
      budgetRange: '',
      expectedDeliveryTime: '',
      remark: '',
      submitterName: '',
      submitterPhone: ''
    },
    budgetOptions: ['50000以下', '50000-100000', '100000-200000', '200000-500000', '500000以上'],
    today: ''
  },

  onLoad() {
    // 设置今天日期为最小日期
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    this.setData({
      today: `${year}-${month}-${day}`
    });
  },

  // 输入框变化
  onInput(e) {
    const { field } = e.currentTarget.dataset;
    const { value } = e.detail;
    this.setData({
      [`form.${field}`]: value
    });
  },

  // 预算选择
  onBudgetChange(e) {
    const { value } = e.detail;
    this.setData({
      'form.budgetRange': this.data.budgetOptions[value]
    });
  },

  // 日期选择
  onDateChange(e) {
    const { value } = e.detail;
    this.setData({
      'form.expectedDeliveryTime': value
    });
  },

  // 表单验证
  validateForm() {
    const { form } = this.data;
    const requiredFields = [
      { field: 'title', label: '需求标题' },
      { field: 'functionalAppeal', label: '功能诉求' },
      { field: 'targetAudience', label: '目标人群' },
      { field: 'budgetRange', label: '预算范围' },
      { field: 'expectedDeliveryTime', label: '期望交付时间' }
    ];

    for (const item of requiredFields) {
      if (!form[item.field] || form[item.field].trim() === '') {
        wx.showToast({
          title: `请填写${item.label}`,
          icon: 'none'
        });
        return false;
      }
    }

    return true;
  },

  // 跳转到人才库
  goToTalentPool() {
    wx.navigateTo({
      url: '/pages/talent_pool/index/index'
    });
  },

  // 提交表单
  submitForm() {
    if (!this.validateForm()) {
      return;
    }

    const submitterId = app.globalData.userId;
    const data = {
      ...this.data.form,
      submitterId
    };

    wx.showLoading({
      title: '提交中...'
    });

    app.request({
      url: '/demand/submit',
      method: 'POST',
      data,
      success: (res) => {
        wx.hideLoading();
        wx.showToast({
          title: '提交成功',
          icon: 'success'
        });
        
        // 延迟跳转到列表页
        setTimeout(() => {
          wx.navigateTo({
            url: '/pages/demandList/demandList'
          });
        }, 1500);
      },
      fail: () => {
        wx.hideLoading();
      }
    });
  }
});
