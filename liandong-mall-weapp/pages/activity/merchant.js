const productService = require('../../services/productService');

Page({
  data: {
    currentFilter: 'all',
    stats: { merchantCount: '5,280', qualityRate: '98.5', returnRate: '1.2' },
    merchants: [],
    products: []
  },
  onLoad() {
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
        commission: item.commissionAmount || '0',
        rate: (item.commissionRate || 0) + '%',
        sales: item.monthlySales || '0',
        merchantLogo: '/images/default-shop.png',
        merchantName: item.shopName || '店铺'
      }));
      this.setData({ products });
    } catch (error) {
      console.error('加载商品失败:', error);
    } finally {
      wx.hideLoading();
    }
  },
  switchFilter(e) { this.setData({ currentFilter: e.currentTarget.dataset.filter }); },
  goToProductDetail(e) { wx.navigateTo({ url: '/pages/product-detail/product-detail?id=' + e.currentTarget.dataset.id }); },
  addToShelf(e) { wx.showToast({ title: '已加入货架', icon: 'success' }); }
});