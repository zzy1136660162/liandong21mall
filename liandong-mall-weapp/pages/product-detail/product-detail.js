const productService = require('../../services/productService');

Page({
  data: {
    product: {
      id: '',
      title: '',
      price: '',
      originalPrice: '',
      commissionRate: 0,
      commissionAmount: '',
      images: [],
      shopName: '',
      shopLogo: '',
      shopSales: '',
      shopScore: '',
      productScore: '',
      logisticsScore: '',
      serviceScore: '',
      sales: '',
      goodRate: '',
      reviewCount: '',
      darenCount: '',
      stock: '',
      location: '',
      monthSales: '',
      monthViews: '',
      monthDaren: '',
      reviewTags: [],
      tuanzhangName: '',
      tuanzhangAvatar: '',
      tuanzhangDesc: '',
      tags: [],
      specs: {
        weight: [],
        scent: []
      }
    },
    specModalVisible: false,
    selectedSpecs: {},
    selectedCount: 1,
    totalPrice: 0
  },

  onLoad(options) {
    const productId = options.id;
    if (productId) {
      this.loadProductDetail(productId);
    }
  },

  loadProductDetail(productId) {
    wx.showLoading({ title: '加载中...' });

    wx.request({
      url: 'http://localhost:5000/api/xp_product/' + productId,
      method: 'GET',
      success: (res) => {
        console.log('商品详情数据:', res.data);
        if (res.data.code === 200 && res.data.data) {
          const product = res.data.data;
          if (Array.isArray(product.specs) && product.specs.length > 0) {
            const specsObj = {};
            product.specs.forEach(spec => {
              if (spec.name && Array.isArray(spec.values)) {
                specsObj[spec.name] = spec.values.map((val, idx) => ({
                  id: idx + 1,
                  name: val,
                  stock: 100
                }));
              }
            });
            product.specs = specsObj;
          } else {
            product.specs = { '默认': [{ id: 1, name: '默认', stock: product.stock || 0 }] };
          }
          this.setData({ product });
          this.setData({ totalPrice: parseFloat(product.price) || 0 });
        } else {
          wx.showToast({ title: res.data.message || '加载失败', icon: 'none' });
        }
      },
      fail: (err) => {
        console.error('加载商品详情失败:', err);
        wx.showToast({ title: '网络错误', icon: 'none' });
      },
      complete: () => {
        wx.hideLoading();
      }
    });
  },

  goBack() {
    wx.navigateBack();
  },

  shareProduct() {
    wx.showShareMenu({
      withShareTicket: true,
      menus: ['shareAppMessage', 'shareTimeline']
    });
  },

  previewImage(e) {
    const url = e.currentTarget.dataset.url;
    wx.previewImage({
      current: url,
      urls: this.data.product.images
    });
  },

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
              wx.showToast({ title: '已复制', icon: 'success' });
            }
          });
        }
      }
    });
  },

  showSpecsModal() {
    this.setData({ specModalVisible: true });
  },

  hideSpecsModal() {
    this.setData({ specModalVisible: false });
  },

  selectSpec(e) {
    const { type, id } = e.currentTarget.dataset;
    const specs = this.data.product.specs;
    const specList = specs[type] || [];
    const spec = specList.find(s => s.id === id);
    if (spec) {
      const selectedSpecs = this.data.selectedSpecs;
      selectedSpecs[type] = spec;
      this.setData({ selectedSpecs });
      this.calculateTotalPrice();
    }
  },

  calculateTotalPrice() {
    const { selectedSpecs } = this.data;
    let price = parseFloat(this.data.product.price) || 0;
    Object.values(selectedSpecs).forEach(spec => {
      if (spec.price) {
        price = parseFloat(spec.price);
      }
    });
    this.setData({ totalPrice: price });
  },

  addToCart() {
    wx.showToast({ title: '已加入购物车', icon: 'success' });
    this.hideSpecsModal();
  },

  addToShelf() {
    wx.showToast({ title: '已加入货架', icon: 'success' });
  },

  goToSampleApply() {
    const productId = this.data.product.id;
    wx.navigateTo({
      url: '/pages/sample-apply/sample-apply?productId=' + productId
    });
  },

  goToShop() {
    wx.switchTab({
      url: '/pages/xuanpinindex/xuanpinindex'
    });
  },

  buyNow() {
    wx.showToast({ title: '正在下单...', icon: 'loading' });
    setTimeout(() => {
      wx.showToast({ title: '功能开发中', icon: 'none' });
    }, 1000);
  },

  onShareAppMessage() {
    return {
      title: this.data.product.title,
      path: '/pages/product-detail/product-detail?id=' + this.data.product.id,
      imageUrl: this.data.product.images[0]
    };
  }
});
