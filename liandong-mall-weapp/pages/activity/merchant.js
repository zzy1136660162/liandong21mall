Page({
  data: {
    statusBarHeight: 88,
    currentFilter: 'all',
    stats: { merchantCount: '5,280', qualityRate: '98.5', returnRate: '1.2' },
    merchants: [],
    products: []
  },
  onLoad() {
    const systemInfo = wx.getSystemInfoSync();
    this.setData({ statusBarHeight: (systemInfo.statusBarHeight || 20) * 2 });
    this.loadMerchants();
    this.loadProducts();
  },
  loadMerchants() {
    const merchants = [
      { id: 1, logo: 'https://picsum.photos/100/100?random=1', name: '立白官方旗舰店', tags: ['金牌商家', '品牌旗舰'], sales: '128万件', rate: 99.2 },
      { id: 2, logo: 'https://picsum.photos/100/100?random=2', name: '维达官方旗舰店', tags: ['金牌商家', '品牌旗舰'], sales: '96万件', rate: 98.8 },
      { id: 3, logo: 'https://picsum.photos/100/100?random=3', name: '花西子旗舰店', tags: ['金牌商家', '国货之光'], sales: '85万件', rate: 98.5 },
      { id: 4, logo: 'https://picsum.photos/100/100?random=4', name: '完美日记旗舰店', tags: ['品牌旗舰'], sales: '72万件', rate: 97.9 }
    ];
    this.setData({ merchants });
  },
  loadProducts() {
    const products = [
      { id: 'merchant_1', image: 'https://picsum.photos/400/400?random=30', title: '立白大师香氛洗衣液持久留香', price: '39.9', commission: '7.98', rate: '20%', sales: '月销12万件', merchantLogo: 'https://picsum.photos/50/50?random=1', merchantName: '立白官方' },
      { id: 'merchant_2', image: 'https://picsum.photos/400/400?random=31', title: '维达超韧抽纸24包整箱装', price: '45.9', commission: '8.26', rate: '18%', sales: '月销8.5万件', merchantLogo: 'https://picsum.photos/50/50?random=2', merchantName: '维达官方' },
      { id: 'merchant_3', image: 'https://picsum.photos/400/400?random=32', title: '花西子散粉定妆控油持久', price: '149', commission: '32.78', rate: '22%', sales: '月销15.6万件', merchantLogo: 'https://picsum.photos/50/50?random=3', merchantName: '花西子' },
      { id: 'merchant_4', image: 'https://picsum.photos/400/400?random=33', title: '完美日记眼影盘十二色', price: '99', commission: '19.8', rate: '20%', sales: '月销21万件', merchantLogo: 'https://picsum.photos/50/50?random=4', merchantName: '完美日记' }
    ];
    this.setData({ products });
  },
  switchFilter(e) { this.setData({ currentFilter: e.currentTarget.dataset.filter }); },
  goBack() { wx.navigateBack(); },
  goToProductDetail(e) { wx.navigateTo({ url: '/pages/product-detail/product-detail?id=' + e.currentTarget.dataset.id }); },
  addToShelf(e) { wx.showToast({ title: '已加入货架', icon: 'success' }); }
});
