Page({
  data: {
    currentTab: 'sales',
    rankInfo: '根据近24小时销量排序，每小时更新',
    products: []
  },

  onLoad() {
    this.loadProducts();
  },

  // 切换榜单
  switchTab(e) {
    const tab = e.currentTarget.dataset.tab;
    const infoMap = {
      sales: '根据近24小时销量排序，每小时更新',
      commission: '根据佣金比例从高到低排序',
      rising: '根据销量增长率排序，发现潜力爆款',
      new: '近7天上新商品，按销量排序'
    };
    
    this.setData({
      currentTab: tab,
      rankInfo: infoMap[tab]
    });
    
    this.loadProducts();
  },

  // 加载商品数据
  loadProducts() {
    const allProducts = [
      {
        id: 1,
        image: 'https://picsum.photos/400/400?random=1',
        title: '立白大师香氛洗衣液持久留香护色护衣天然酵素',
        price: '39.9',
        originalPrice: '69.9',
        commissionRate: 20,
        commissionAmount: '7.98',
        sales: 120000,
        salesText: '12万',
        dailySales: '1.2万',
        riseRate: '150%',
        tag: '爆款',
        tags: ['正品保障', '7天无理由', '运费险'],
        shop: '立白官方旗舰店',
        shopScore: 4.9,
        location: '广东广州'
      },
      {
        id: 6,
        image: 'https://picsum.photos/400/400?random=6',
        title: '完美日记眼影盘动物盘十二色眼影小猫盘',
        price: '99',
        originalPrice: '159',
        commissionRate: 20,
        commissionAmount: '19.8',
        sales: 210000,
        salesText: '21万',
        dailySales: '2.1万',
        riseRate: '300%',
        tag: '爆款',
        tags: ['正品保障', '7天无理由'],
        shop: '完美日记旗舰店',
        shopScore: 4.7,
        location: '广东广州'
      },
      {
        id: 5,
        image: 'https://picsum.photos/400/400?random=5',
        title: '花西子散粉定妆粉饼持久控油防水防汗不脱妆',
        price: '149',
        originalPrice: '199',
        commissionRate: 22,
        commissionAmount: '32.78',
        sales: 156000,
        salesText: '15.6万',
        dailySales: '1.5万',
        riseRate: '180%',
        tags: ['正品保障', '7天无理由', '国货之光'],
        shop: '花西子旗舰店',
        shopScore: 4.8,
        location: '浙江杭州'
      },
      {
        id: 2,
        image: 'https://picsum.photos/400/400?random=2',
        title: '维达超韧抽纸3层130抽24包整箱装家用实惠',
        price: '45.9',
        originalPrice: '59.9',
        commissionRate: 18,
        commissionAmount: '8.26',
        sales: 85000,
        salesText: '8.5万',
        dailySales: '8500',
        riseRate: '120%',
        tag: '官方',
        tags: ['正品保障', '极速退款'],
        shop: '维达官方旗舰店',
        shopScore: 4.8,
        location: '浙江杭州'
      },
      {
        id: 3,
        image: 'https://picsum.photos/400/400?random=3',
        title: '漫花悬挂式抽纸整箱批发家用实惠装10提',
        price: '29.9',
        originalPrice: '49.9',
        commissionRate: 25,
        commissionAmount: '7.48',
        sales: 56000,
        salesText: '5.6万',
        dailySales: '5600',
        riseRate: '200%',
        tags: ['正品保障', '7天无理由'],
        shop: '漫花旗舰店',
        shopScore: 4.7,
        location: '江苏苏州'
      },
      {
        id: 4,
        image: 'https://picsum.photos/400/400?random=4',
        title: 'SK-II神仙水精华液护肤套装补水保湿230ml',
        price: '899',
        originalPrice: '1299',
        commissionRate: 15,
        commissionAmount: '134.85',
        sales: 23000,
        salesText: '2.3万',
        dailySales: '2300',
        riseRate: '80%',
        tag: '精选',
        tags: ['正品保障', '假一赔十', '专柜直发'],
        shop: 'SK-II官方旗舰店',
        shopScore: 4.9,
        location: '上海'
      },
      {
        id: 7,
        image: 'https://picsum.photos/400/400?random=7',
        title: '兰蔻小黑瓶精华肌底液修护保湿50ml',
        price: '680',
        originalPrice: '850',
        commissionRate: 12,
        commissionAmount: '81.6',
        sales: 32000,
        salesText: '3.2万',
        dailySales: '3200',
        riseRate: '90%',
        tags: ['正品保障', '专柜直发'],
        shop: '兰蔻官方旗舰店',
        shopScore: 4.9,
        location: '上海'
      },
      {
        id: 8,
        image: 'https://picsum.photos/400/400?random=8',
        title: '雅诗兰黛小棕瓶精华液抗老修护50ml第七代',
        price: '720',
        originalPrice: '900',
        commissionRate: 10,
        commissionAmount: '72',
        sales: 45000,
        salesText: '4.5万',
        dailySales: '4500',
        riseRate: '110%',
        tag: '大牌',
        tags: ['正品保障', '假一赔十'],
        shop: '雅诗兰黛官方旗舰店',
        shopScore: 4.9,
        location: '上海'
      }
    ];

    let sortedProducts = [...allProducts];
    
    // 根据当前榜单类型排序
    switch (this.data.currentTab) {
      case 'sales':
        sortedProducts.sort((a, b) => b.sales - a.sales);
        break;
      case 'commission':
        sortedProducts.sort((a, b) => b.commissionRate - a.commissionRate);
        break;
      case 'rising':
        sortedProducts.sort((a, b) => parseInt(b.riseRate) - parseInt(a.riseRate));
        break;
      case 'new':
        // 新品榜 - 假设id大的为新品
        sortedProducts.sort((a, b) => b.id - a.id);
        break;
    }

    this.setData({ products: sortedProducts });
  },

  // 跳转到商品详情
  goToProductDetail(e) {
    const productId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/product-detail/product-detail?id=' + productId
    });
  },

  // 申请样品
  applySample(e) {
    e.stopPropagation();
    const productId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/sample-apply/sample-apply?productId=' + productId
    });
  }
});
