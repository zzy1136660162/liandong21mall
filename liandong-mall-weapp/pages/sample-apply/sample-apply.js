Page({
  data: {
    selectedProducts: [],
    formData: {
      name: '',
      phone: '',
      region: [],
      address: '',
      remark: ''
    },
    notices: [
      '样品申请需经过审核，审核通过后才会寄出',
      '每个达人每月最多可申请5个样品',
      '收到样品后需在7天内完成测评并发布',
      '样品仅供测评使用，禁止转售',
      '如未按时完成测评，将影响后续样品申请资格'
    ],
    canSubmit: false,
    totalCommission: '0.00'
  },

  onLoad(options) {
    // 获取传入的商品ID
    const productId = options.productId;
    if (productId) {
      this.loadProductInfo(productId);
    }
    
    // 检查提交按钮状态
    this.checkCanSubmit();
  },

  // 加载商品信息
  loadProductInfo(productId) {
    // 模拟加载商品数据
    const product = {
      id: productId,
      image: 'https://picsum.photos/120/120?random=' + productId,
      name: '立白大师香氛洗衣液持久留香护色护衣',
      price: '39.9',
      commissionRate: 20,
      commissionAmount: '7.98'
    };
    
    this.setData({
      selectedProducts: [product]
    }, () => {
      this.calculateTotalCommission();
      this.checkCanSubmit();
    });
  },

  // 计算总佣金
  calculateTotalCommission() {
    const total = this.data.selectedProducts.reduce((sum, item) => {
      return sum + parseFloat(item.commissionAmount || 0);
    }, 0);
    this.setData({
      totalCommission: total.toFixed(2)
    });
  },

  // 添加商品
  addProduct() {
    wx.navigateTo({
      url: '/pages/index/index?selectMode=true'
    });
  },

  // 移除商品
  removeProduct(e) {
    const productId = e.currentTarget.dataset.id;
    const products = this.data.selectedProducts.filter(item => item.id != productId);
    this.setData({
      selectedProducts: products
    }, () => {
      this.calculateTotalCommission();
      this.checkCanSubmit();
    });
  },

  // 选择地址
  selectAddress() {
    wx.showActionSheet({
      itemList: ['使用微信地址', '手动填写', '从收货地址选择'],
      success: (res) => {
        switch (res.tapIndex) {
          case 0:
            this.getWXAddress();
            break;
          case 1:
            // 手动填写，保持当前状态
            break;
          case 2:
            wx.showToast({
              title: '地址簿功能开发中',
              icon: 'none'
            });
            break;
        }
      }
    });
  },

  // 获取微信地址
  getWXAddress() {
    wx.chooseAddress({
      success: (res) => {
        this.setData({
          'formData.name': res.userName,
          'formData.phone': res.telNumber,
          'formData.region': [res.provinceName, res.cityName, res.countyName],
          'formData.address': res.detailInfo
        });
        this.checkCanSubmit();
      },
      fail: (err) => {
        if (err.errMsg.indexOf('fail auth') > -1) {
          wx.showModal({
            title: '需要授权',
            content: '请授权访问您的通讯地址',
            success: (res) => {
              if (res.confirm) {
                wx.openSetting();
              }
            }
          });
        }
      }
    });
  },

  // 输入姓名
  onNameInput(e) {
    this.setData({
      'formData.name': e.detail.value
    });
    this.checkCanSubmit();
  },

  // 输入电话
  onPhoneInput(e) {
    this.setData({
      'formData.phone': e.detail.value
    });
    this.checkCanSubmit();
  },

  // 选择地区
  onRegionChange(e) {
    this.setData({
      'formData.region': e.detail.value
    });
    this.checkCanSubmit();
  },

  // 输入详细地址
  onAddressInput(e) {
    this.setData({
      'formData.address': e.detail.value
    });
    this.checkCanSubmit();
  },

  // 输入备注
  onRemarkInput(e) {
    this.setData({
      'formData.remark': e.detail.value
    });
  },

  // 检查是否可以提交
  checkCanSubmit() {
    const { selectedProducts, formData } = this.data;
    const canSubmit = selectedProducts.length > 0 && 
                      formData.name.trim() !== '' && 
                      formData.phone.trim() !== '' && 
                      formData.region.length > 0 && 
                      formData.address.trim() !== '';
    this.setData({ canSubmit });
  },

  // 提交申请
  submitApplication() {
    if (!this.data.canSubmit) {
      wx.showToast({
        title: '请填写完整信息',
        icon: 'none'
      });
      return;
    }

    // 验证手机号
    const phone = this.data.formData.phone;
    if (!/^1[3-9]\d{9}$/.test(phone)) {
      wx.showToast({
        title: '请输入正确的手机号',
        icon: 'none'
      });
      return;
    }

    // 构建提交数据
    const submitData = {
      products: this.data.selectedProducts.map(item => item.id),
      recipient: {
        name: this.data.formData.name,
        phone: this.data.formData.phone,
        province: this.data.formData.region[0],
        city: this.data.formData.region[1],
        district: this.data.formData.region[2],
        address: this.data.formData.address
      },
      remark: this.data.formData.remark,
      applyTime: new Date().toISOString()
    };

    console.log('提交数据:', submitData);

    // 显示确认弹窗
    wx.showModal({
      title: '确认提交',
      content: '提交后不可修改，是否确认提交样品申请？',
      success: (res) => {
        if (res.confirm) {
          this.doSubmit(submitData);
        }
      }
    });
  },

  // 执行提交
  doSubmit(data) {
    wx.showLoading({
      title: '提交中...'
    });

    // 模拟提交
    setTimeout(() => {
      wx.hideLoading();
      
      // 生成申请记录ID
      const applicationId = 'SA' + Date.now();
      
      // 保存到本地存储（模拟）
      const applications = wx.getStorageSync('sampleApplications') || [];
      applications.unshift({
        id: applicationId,
        ...data,
        status: 'pending',
        statusText: '待审核',
        shipStatus: 'not_shipped',
        shipStatusText: '未寄出'
      });
      wx.setStorageSync('sampleApplications', applications);

      wx.showToast({
        title: '申请成功',
        icon: 'success',
        duration: 1500,
        success: () => {
          setTimeout(() => {
            // 跳转到我的样品申请页
            wx.redirectTo({
              url: '/pages/my-samples/my-samples'
            });
          }, 1500);
        }
      });
    }, 1500);
  }
});
