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
  loadProducts() {
    const products = [
      { id: 'cheap_1', image: 'https://picsum.photos/400/400?random=40', title: '【9.9包邮】厨房清洁刷套装5件套', price: '9.9', originalPrice: '19.9', commission: '2.97', rate: '30%', sales: '月销8.5万件', freeShipping: true, highCommission: true, hot: true },
      { id: 'cheap_2', image: 'https://picsum.photos/400/400?random=41', title: '【9.9包邮】创意挂钩强力粘钩10个装', price: '9.9', originalPrice: '15.9', commission: '2.97', rate: '30%', sales: '月销6.2万件', freeShipping: true, highCommission: false, hot: true },
      { id: 'cheap_3', image: 'https://picsum.photos/400/400?random=42', title: '【19.9包邮】多功能削皮器三件套', price: '19.9', originalPrice: '39.9', commission: '5.97', rate: '30%', sales: '月销4.8万件', freeShipping: true, highCommission: true, hot: false },
      { id: 'cheap_4', image: 'https://picsum.photos/400/400?random=43', title: '【19.9包邮】便携折叠购物袋环保袋', price: '19.9', originalPrice: '29.9', commission: '4.97', rate: '25%', sales: '月销3.5万件', freeShipping: true, highCommission: false, hot: true },
      { id: 'cheap_5', image: 'https://picsum.photos/400/400?random=44', title: '【29.9包邮】不锈钢保温杯500ml', price: '29.9', originalPrice: '59.9', commission: '7.47', rate: '25%', sales: '月销2.8万件', freeShipping: true, highCommission: true, hot: false },
      { id: 'cheap_6', image: 'https://picsum.photos/400/400?random=45', title: '【29.9包邮】多功能收纳盒3个装', price: '29.9', originalPrice: '49.9', commission: '5.97', rate: '20%', sales: '月销2.1万件', freeShipping: true, highCommission: false, hot: false }
    ];
    this.setData({ products });
  },
  switchFilter(e) { this.setData({ currentFilter: e.currentTarget.dataset.filter }); },
  switchPrice(e) { this.setData({ currentPrice: e.currentTarget.dataset.price }); },
  goBack() { wx.navigateBack(); },
  goToProductDetail(e) { wx.navigateTo({ url: '/pages/product-detail/product-detail?id=' + e.currentTarget.dataset.id }); },
  addToShelf(e) { wx.showToast({ title: '已加入货架', icon: 'success' }); }
});
