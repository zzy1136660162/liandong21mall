Page({
  data: {
    product: {
      id: '',
      title: '立白大师香氛洗衣液香味持久留香去污渍正品柔顺护色香水洗衣液',
      price: '39.9',
      originalPrice: '59.9',
      commissionRate: 25,
      commissionAmount: '9.97',
      images: [
        'https://picsum.photos/750/750?random=1',
        'https://picsum.photos/750/750?random=2',
        'https://picsum.photos/750/750?random=3'
      ],
      shopName: '立白Liby旗舰店',
      shopLogo: 'https://picsum.photos/80/80?random=10',
      shopSales: '6860',
      shopScore: '4.84',
      productScore: '4.96',
      logisticsScore: '4.74',
      serviceScore: '4.79',
      sales: '2473',
      goodRate: '98',
      reviewCount: '2652',
      darenCount: '4',
      stock: '4',
      location: '贵州省黔南布依族苗族自治州',
      monthSales: '182',
      monthViews: '3166',
      monthDaren: '1万',
      reviewTags: ['有图/视频', '很好用', '味道好', '香味很香'],
      tuanzhangName: '飞鸽传媒团长精选',
      tuanzhangAvatar: 'https://picsum.photos/80/80?random=20',
      tuanzhangDesc: '聊高佣·帮申样·响应快',
      tags: ['官方正品', '大牌大补', '品质保障']
    }
  },

  onLoad(options) {
    const productId = options.id;
    if (productId) {
      this.loadProductDetail(productId);
    }
  },

  // 加载商品详情
  loadProductDetail(productId) {
    // 模拟加载商品数据
    // 实际项目中这里应该是 wx.request 调用接口
    console.log('加载商品详情:', productId);
    
    // 根据ID生成不同的数据
    const randomNum = parseInt(productId) || 1;
    this.setData({
      'product.id': productId,
      'product.images': [
        `https://picsum.photos/750/750?random=${randomNum}`,
        `https://picsum.photos/750/750?random=${randomNum + 100}`,
        `https://picsum.photos/750/750?random=${randomNum + 200}`
      ],
      'product.shopLogo': `https://picsum.photos/80/80?random=${randomNum + 300}`,
      'product.tuanzhangAvatar': `https://picsum.photos/80/80?random=${randomNum + 400}`
    });
  },

  // 返回上一页
  goBack() {
    wx.navigateBack();
  },

  // 分享商品
  shareProduct() {
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    });
  },

  // 预览图片
  previewImage(e) {
    const url = e.currentTarget.dataset.url;
    wx.previewImage({
      current: url,
      urls: this.data.product.images
    });
  },

  // 联系团长
  contactTuanzhang() {
    wx.showModal({
      title: '联系团长',
      content: '团长微信号：feige888\n电话：13888888888',
      showCancel: false,
      confirmText: '复制微信',
      success: (res) => {
        if (res.confirm) {
          wx.setClipboardData({
            data: 'feige888',
            success: () => {
              wx.showToast({
                title: '已复制',
                icon: 'success'
              });
            }
          });
        }
      }
    });
  },

  // 进店选品
  goToShop() {
    wx.showToast({
      title: '进入店铺',
      icon: 'none'
    });
  },

  // 加入货架
  addToShelf() {
    wx.showModal({
      title: '加入货架',
      content: '确定将该商品加入您的货架吗？',
      success: (res) => {
        if (res.confirm) {
          // 获取已存在的货架商品
          let shelfProducts = wx.getStorageSync('shelfProducts') || [];
          
          // 检查是否已存在
          const exists = shelfProducts.some(item => item.id === this.data.product.id);
          if (exists) {
            wx.showToast({
              title: '商品已在货架中',
              icon: 'none'
            });
            return;
          }
          
          // 添加到货架
          shelfProducts.unshift({
            id: this.data.product.id,
            title: this.data.product.title,
            price: this.data.product.price,
            commissionRate: this.data.product.commissionRate,
            image: this.data.product.images[0],
            addTime: new Date().toISOString()
          });
          
          wx.setStorageSync('shelfProducts', shelfProducts);
          
          wx.showToast({
            title: '加入成功',
            icon: 'success'
          });
        }
      }
    });
  },

  // 去货架
  goToShelf() {
    wx.switchTab({
      url: '/pages/my/my'
    });
  },

  // 申请样品
  applySample() {
    wx.navigateTo({
      url: '/pages/sample-apply/sample-apply?productId=' + this.data.product.id
    });
  },

  onShareAppMessage() {
    return {
      title: this.data.product.title,
      path: '/pages/product-detail/product-detail?id=' + this.data.product.id,
      imageUrl: this.data.product.images[0]
    };
  }
});
