const productService = require('../../services/productService');

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
      tags: ['官方正品', '大牌大补', '品质保障'],
      // 商品规格信息
      specs: {
        weight: [
          { id: 1, name: '500g', price: '29.9', stock: 100 },
          { id: 2, name: '1.5kg', price: '39.9', stock: 100 },
          { id: 3, name: '3kg', price: '59.9', stock: 100 },
          { id: 4, name: '9kg', price: '99.9', stock: 100 }
        ],
        scent: [
          { id: 1, name: '樱花香', stock: 100 },
          { id: 2, name: '薰衣草', stock: 100 },
          { id: 3, name: '茉莉香', stock: 100 },
          { id: 4, name: '柠檬香', stock: 100 }
        ]
      }
    },
    // 规格选择弹窗相关数据
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

  // 加载商品详情
  async loadProductDetail(productId) {
    wx.showLoading({ title: '加载中...' });
    try {
      const res = await productService.getProductDetail(productId);
      console.log('商品详情返回:', res);
      
      let data = null;
      if (res.code === 200 && res.data) {
        data = res.data;
      } else if (res.id) {
        data = res;
      }
      
      if (data) {
        this.setData({
          'product.id': data.id || productId,
          'product.title': data.name || data.product_name || '未知商品',
          'product.price': data.price || '0',
          'product.originalPrice': data.originalPrice || data.original_price || '',
          'product.commissionRate': data.commissionRate || data.commission_rate || 0,
          'product.commissionAmount': data.commissionAmount || data.commission_amount || '0',
          'product.images': data.images || [data.main_image || data.image || '/images/default.png'],
          'product.shopName': data.shopName || data.shop_name || '店铺',
          'product.shopLogo': data.shopLogo || '/images/default-shop.png',
          'product.sales': data.sales || '0',
          'product.goodRate': data.goodRate || '98',
          'product.stock': data.stock || '99',
          'product.location': data.location || '未知'
        });
      }
    } catch (error) {
      console.error('加载商品详情失败:', error);
    } finally {
      wx.hideLoading();
    }
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
  },

  // 立即购买按钮点击事件
  buyNow() {
    // 显示规格选择弹窗
    this.setData({
      specModalVisible: true,
      // 重置选择状态
      selectedSpecs: {},
      selectedCount: 1,
      totalPrice: parseFloat(this.data.product.price)
    });
  },

  // 更新总价
  updateTotalPrice() {
    const { selectedSpecs, selectedCount, product } = this.data;
    const price = selectedSpecs.weight ? parseFloat(selectedSpecs.weight.price) : parseFloat(product.price);
    const totalPrice = price * selectedCount;
    this.setData({
      totalPrice: parseFloat(totalPrice.toFixed(2))
    });
  },

  // 关闭规格选择弹窗
  closeSpecModal() {
    this.setData({
      specModalVisible: false
    });
  },

  // 选择规格
  selectSpec(e) {
    const { type, spec } = e.currentTarget.dataset;
    const selectedSpecs = { ...this.data.selectedSpecs };
    selectedSpecs[type] = spec;
    this.setData({
      selectedSpecs
    });
    // 更新总价
    this.updateTotalPrice();
  },

  // 调整购买数量
  changeQuantity(e) {
    const { type } = e.currentTarget.dataset;
    let { selectedCount } = this.data;
    
    if (type === 'minus' && selectedCount > 1) {
      selectedCount--;
    } else if (type === 'plus') {
      // 检查库存限制
      const maxStock = this.data.selectedSpecs.weight ? this.data.selectedSpecs.weight.stock : this.data.product.stock;
      if (selectedCount < maxStock) {
        selectedCount++;
      } else {
        wx.showToast({
          title: '已达到最大库存',
          icon: 'none'
        });
        return;
      }
    }
    
    this.setData({
      selectedCount
    });
    // 更新总价
    this.updateTotalPrice();
  },

  // 确认规格选择
  confirmSpec() {
    const { selectedSpecs, selectedCount, product } = this.data;
    
    // 检查是否选择了所有必要的规格
    if (!selectedSpecs.weight || !selectedSpecs.scent) {
      wx.showToast({
        title: '请选择完整的商品规格',
        icon: 'none'
      });
      return;
    }
    
    // 准备订单商品数据
    const orderItem = {
      productId: product.id,
      productName: product.title,
      mainImage: product.images[0],
      price: selectedSpecs.weight.price,
      quantity: selectedCount,
      specs: `${selectedSpecs.weight.name} - ${selectedSpecs.scent.name}`
    };
    
    // 关闭弹窗
    this.closeSpecModal();
    
    // 跳转到订单确认页面
    wx.navigateTo({
      url: `/pages/sp_Order_confirm_page/sp_Order_confirm_page`,
      success: (res) => {
        // 通过eventChannel传递数据到下一个页面
        res.eventChannel.emit('orderDataFromProduct', {
          orderItems: [orderItem],
          from: 'buyNow' // 标识是从立即购买过来的
        });
      }
    });
  }
});
