Page({
  data: {
    currentFilter: 'all',
    stats: {
      followerCount: '12.5万',
      successRate: '85',
      avgIncome: '¥3,280'
    },
    talents: [],
    products: []
  },

  onLoad() {
    this.loadTalents();
    this.loadProducts();
  },

  loadTalents() {
    const talents = [
      {
        id: 1,
        avatar: 'https://picsum.photos/100/100?random=1',
        name: '小美带货达人',
        tag: '美妆达人',
        sales: '¥128万',
        isFollowing: true
      },
      {
        id: 2,
        avatar: 'https://picsum.photos/100/100?random=2',
        name: '吃货小王',
        tag: '美食博主',
        sales: '¥96万',
        isFollowing: false
      },
      {
        id: 3,
        avatar: 'https://picsum.photos/100/100?random=3',
        name: '家居生活家',
        tag: '家居达人',
        sales: '¥85万',
        isFollowing: false
      },
      {
        id: 4,
        avatar: 'https://picsum.photos/100/100?random=4',
        name: '潮流穿搭师',
        tag: '时尚博主',
        sales: '¥72万',
        isFollowing: true
      },
      {
        id: 5,
        avatar: 'https://picsum.photos/100/100?random=5',
        name: '数码测评君',
        tag: '数码达人',
        sales: '¥68万',
        isFollowing: false
      }
    ];

    this.setData({ talents });
  },

  loadProducts() {
    const products = [
      {
        id: 'follow_1',
        image: 'https://picsum.photos/400/400?random=10',
        title: '花间颂粉饼控油定妆持久遮瑕散粉',
        price: '49.9',
        commission: '13.97',
        rate: '28%',
        sales: '月销6.4万件',
        followerAvatar: 'https://picsum.photos/50/50?random=1',
        followerName: '小美带货达人',
        followCount: '2.3万',
        tag: '跟选爆款',
        cashback: true,
        trust: true,
        isBrand: true
      },
      {
        id: 'follow_2',
        image: 'https://picsum.photos/400/400?random=11',
        title: '【拍1发4包】麻辣牛板筋自拌延边特产',
        price: '8.98',
        commission: '1.98',
        rate: '22%',
        sales: '月销1.3万件',
        followerAvatar: 'https://picsum.photos/50/50?random=2',
        followerName: '吃货小王',
        followCount: '1.8万',
        cashback: false,
        trust: true,
        isBrand: false
      },
      {
        id: 'follow_3',
        image: 'https://picsum.photos/400/400?random=12',
        title: '南极人A类抗菌大豆被加厚保暖冬被',
        price: '82',
        commission: '8.2',
        rate: '10%',
        sales: '304人已上架',
        followerAvatar: 'https://picsum.photos/50/50?random=3',
        followerName: '家居生活家',
        followCount: '1.2万',
        tag: '新品推荐',
        cashback: true,
        trust: false,
        isBrand: true
      },
      {
        id: 'follow_4',
        image: 'https://picsum.photos/400/400?random=13',
        title: '春季爆款高腰显瘦阔腿裤',
        price: '98',
        commission: '12.74',
        rate: '13%',
        sales: '月销2088件',
        followerAvatar: 'https://picsum.photos/50/50?random=4',
        followerName: '潮流穿搭师',
        followCount: '9,856',
        cashback: false,
        trust: true,
        isBrand: false
      }
    ];

    this.setData({ products });
  },

  switchFilter(e) {
    const filter = e.currentTarget.dataset.filter;
    this.setData({ currentFilter: filter });
  },

  followTalent(e) {
    const id = e.currentTarget.dataset.id;
    const talents = this.data.talents.map(t => {
      if (t.id === id) {
        t.isFollowing = !t.isFollowing;
      }
      return t;
    });
    this.setData({ talents });
    wx.showToast({ title: '操作成功', icon: 'success' });
  },

  goToProductDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({ url: '/pages/product-detail/product-detail?id=' + id });
  },

  addToShelf(e) {
    wx.showToast({ title: '已加入货架', icon: 'success' });
  }
});