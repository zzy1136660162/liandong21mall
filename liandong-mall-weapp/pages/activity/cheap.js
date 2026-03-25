const productService = require('../../services/productService');

Page({
  data: {
    statusBarHeight: 88,
    currentFilter: 'all',
    currentPrice: 'all',
    stats: { productCount: '12.8万', avgPrice: '¥15.9', avgCommission: '25' },
    products: []
  },
  onLoad() {
    const systemInfo = wx.getSystemInfoSync();
    this.setData({ statusBarHeight: (systemInfo.statusBarHeight || 20) * 2 });
    this.loadProducts();
  },
  async loadProducts() {
    wx.showLoading({ title: '加载中...' });
    try {
      const res = await productService.getProducts({ page: 1, pageSize: 20 });
      const products = (res.list || res || []).map(item => ({
        id: item.id,
        image: item.image || item.main_image || '/images/default.png',
        title: item.name || item.title || '未知商品',
        price: item.price || '0',
        originalPrice: item.originalPrice || '',
        commission: item.commissionAmount || '0',
        rate: (item.commissionRate || 0) + '%',
        sales: item.monthlySales || '0',
        freeShipping: true,
        highCommission: (item.commissionRate || 0) > 20,
        hot: false
      }));
      this.setData({ products });
    } catch (error) {
      console.error('加载商品失败:', error);
    } finally {
      wx.hideLoading();
    }
  },
  switchFilter(e) { this.setData({ currentFilter: e.currentTarget.dataset.filter }); },
  switchPrice(e) { this.setData({ currentPrice: e.currentTarget.dataset.price }); },
  goBack() { wx.navigateBack(); },
  goToProductDetail(e) { wx.navigateTo({ url: '/pages/product-detail/product-detail?id=' + e.currentTarget.dataset.id }); },
  addToShelf(e) { wx.showToast({ title: '已加入货架', icon: 'success' }); }
});
