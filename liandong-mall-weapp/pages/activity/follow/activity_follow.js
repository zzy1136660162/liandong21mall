// pages/activity/follow/activity_follow.js
const productService = require('../../../services/productService.js');

Page({
  data: {
    products: [],
    page: 1,
    pageSize: 10,
    loading: false,
    hasMore: true,
    title: '同行跟选'
  },

  onLoad(options) {
    this.loadProducts();
  },

  async loadProducts() {
    if (this.data.loading || !this.data.hasMore) return;
    
    this.setData({ loading: true });
    wx.showLoading({ title: '加载中...' });
    
    try {
      const res = await productService.getActivityProducts('follow', this.data.page, this.data.pageSize);
      wx.hideLoading();
      
      if (res && res.code === 200 && res.data) {
        const newProducts = res.data.products || [];
        this.setData({
          products: this.data.page === 1 ? newProducts : [...this.data.products, ...newProducts],
          hasMore: newProducts.length >= this.data.pageSize,
          page: this.data.page + 1
        });
      }
    } catch (err) {
      wx.hideLoading();
      console.error('加载商品失败:', err);
      wx.showToast({ title: '加载失败', icon: 'none' });
    } finally {
      this.setData({ loading: false });
    }
  },

  onReachBottom() {
    this.loadProducts();
  },

  onPullDownRefresh() {
    this.setData({ page: 1, hasMore: true, products: [] });
    this.loadProducts().then(() => {
      wx.stopPullDownRefresh();
    });
  },

  goToProductDetail(e) {
    const productId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/product-detail/product-detail?id=' + productId
    });
  },

  goBack() {
    wx.navigateBack();
  }
});
