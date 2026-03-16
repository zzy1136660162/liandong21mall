Page({
  data: {
    statusBarHeight: 88,
    currentFilter: 'all',
    stats: { videoCount: '8.6万', playCount: '28亿', conversion: '3.2' },
    products: []
  },
  onLoad() {
    const systemInfo = wx.getSystemInfoSync();
    this.setData({ statusBarHeight: (systemInfo.statusBarHeight || 20) * 2 });
    this.loadProducts();
  },
  loadProducts() {
    const products = [
      { id: 'video_1', image: 'https://picsum.photos/400/400?random=20', title: '【视频同款】网红爆款空气炸锅专用纸', price: '9.9', commission: '2.97', rate: '30%', sales: '月销5.2万件', playCount: '128万', duration: '00:32', authorAvatar: 'https://picsum.photos/50/50?random=1', authorName: '美食达人小王' },
      { id: 'video_2', image: 'https://picsum.photos/400/400?random=21', title: '【视频实测】多功能厨房剪刀不锈钢', price: '15.9', commission: '4.77', rate: '30%', sales: '月销3.8万件', playCount: '96万', duration: '00:45', authorAvatar: 'https://picsum.photos/50/50?random=2', authorName: '生活小妙招' },
      { id: 'video_3', image: 'https://picsum.photos/400/400?random=22', title: '【视频推荐】便携式榨汁杯充电式', price: '49.9', commission: '12.47', rate: '25%', sales: '月销2.1万件', playCount: '85万', duration: '01:12', authorAvatar: 'https://picsum.photos/50/50?random=3', authorName: '健康生活家' },
      { id: 'video_4', image: 'https://picsum.photos/400/400?random=23', title: '【视频爆款】懒人拖把免手洗平板拖', price: '29.9', commission: '7.47', rate: '25%', sales: '月销4.5万件', playCount: '152万', duration: '00:58', authorAvatar: 'https://picsum.photos/50/50?random=4', authorName: '家居好物推荐' }
    ];
    this.setData({ products });
  },
  switchFilter(e) { this.setData({ currentFilter: e.currentTarget.dataset.filter }); },
  goBack() { wx.navigateBack(); },
  goToProductDetail(e) { wx.navigateTo({ url: '/pages/product-detail/product-detail?id=' + e.currentTarget.dataset.id }); },
  addToShelf(e) { wx.showToast({ title: '已加入货架', icon: 'success' }); }
});
