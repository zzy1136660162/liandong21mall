const productService = require('../../services/productService');

Page({
  data: {
    currentFilter: 'all',
    stats: {
      productCount: '2,580',
      avgCommission: '25',
      totalSales: '1.2亿'
    },
    products: []
  },

  onLoad() {
    this.loadProducts();
  },

  // 加载商品数据
  async loadProducts() {
    wx.showLoading({ title: '加载中...' });
    try {
      const res = await productService.getProducts({ page: 1, pageSize: 20 });
      const products = (res.list || res || []).map(item => ({
        id: item.id,
        image: item.image || item.main_image || '/images/default.png',
        title: item.name || item.title || '未知商品',
        price: item.price || '0',
        commission: item.commissionAmount || '0',
        rate: (item.commissionRate || 0) + '%',
        sales: item.monthlySales || '0',
        dailySales: item.dailySales || '0',
        tag: item.tag || '',
        cashback: item.hasCashback || false,
        trust: true,
        isBrand: item.isBrand || false,
        rankTag: ''
      }));
      
      this.setData({ products });
    } catch (error) {
      console.error('加载商品失败:', error);
    } finally {
      wx.hideLoading();
    }
  },

  // 切换筛选
  switchFilter(e) {
    const filter = e.currentTarget.dataset.filter;
    this.setData({ currentFilter: filter });
    this.loadProducts();
  },

  // 返回
  goBack() {
    wx.navigateBack();
  },

  // 去商品详情
  goToProductDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/product-detail/product-detail?id=' + id
    });
  },

  // 加入货架
  addToShelf(e) {
    const id = e.currentTarget.dataset.id;
    wx.showToast({
      title: '已加入货架',
      icon: 'success'
    });
  }
});
