Page({
  data: {
    statusBarHeight: 88,
    currentFilter: 'all',
    stats: {
      productCount: '2,580',
      avgCommission: '25',
      totalSales: '1.2亿'
    },
    products: []
  },

  onLoad() {
    // 获取系统状态栏高度
    const systemInfo = wx.getSystemInfoSync();
    const statusBarHeight = systemInfo.statusBarHeight || 20;
    
    this.setData({
      statusBarHeight: statusBarHeight * 2
    });
    
    this.loadProducts();
  },

  // 加载商品数据
  loadProducts() {
    const products = [
      {
        id: 'hot_1',
        image: 'https://picsum.photos/400/400?random=1',
        title: '立白大师香氛洗衣液持久留香护色护衣天然酵素',
        price: '39.9',
        commission: '7.98',
        rate: '20%',
        sales: '月销12万件',
        dailySales: '1.2万',
        tag: '爆款',
        cashback: true,
        trust: true,
        isBrand: true,
        rankTag: '入选洗衣液爆款榜第1名'
      },
      {
        id: 'hot_2',
        image: 'https://picsum.photos/400/400?random=2',
        title: '维达超韧抽纸3层130抽24包整箱装家用实惠',
        price: '45.9',
        commission: '8.26',
        rate: '18%',
        sales: '月销8.5万件',
        dailySales: '8500',
        cashback: false,
        trust: true,
        isBrand: true,
        rankTag: '入选抽纸爆款榜第2名'
      },
      {
        id: 'hot_3',
        image: 'https://picsum.photos/400/400?random=3',
        title: '花西子散粉定妆粉饼持久控油防水防汗不脱妆',
        price: '149',
        commission: '32.78',
        rate: '22%',
        sales: '月销15.6万件',
        dailySales: '1.5万',
        tag: '国货之光',
        cashback: true,
        trust: true,
        isBrand: true,
        rankTag: '入选散粉爆款榜第1名'
      },
      {
        id: 'hot_4',
        image: 'https://picsum.photos/400/400?random=4',
        title: '完美日记眼影盘动物盘十二色眼影小猫盘',
        price: '99',
        commission: '19.8',
        rate: '20%',
        sales: '月销21万件',
        dailySales: '2.1万',
        tag: '新品',
        cashback: false,
        trust: true,
        isBrand: true,
        rankTag: '入选眼影爆款榜第3名'
      },
      {
        id: 'hot_5',
        image: 'https://picsum.photos/400/400?random=5',
        title: '李海龙麻辣烫正宗东北老式黏糊麻辣烫',
        price: '39.8',
        commission: '6.77',
        rate: '17%',
        sales: '月销3911件',
        dailySales: '1200',
        cashback: true,
        trust: false,
        isBrand: false,
        rankTag: '入选麻辣烫爆款榜第1名'
      },
      {
        id: 'hot_6',
        image: 'https://picsum.photos/400/400?random=6',
        title: '【拍1发4包】麻辣牛板筋自拌延边特产',
        price: '8.98',
        commission: '1.98',
        rate: '22%',
        sales: '月销1.3万件',
        dailySales: '3500',
        cashback: false,
        trust: true,
        isBrand: false,
        rankTag: '入选素鸡/素肉爆款榜第2名'
      }
    ];

    this.setData({ products });
  },

  // 切换筛选
  switchFilter(e) {
    const filter = e.currentTarget.dataset.filter;
    this.setData({ currentFilter: filter });
    // 这里可以根据筛选条件重新加载商品
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
