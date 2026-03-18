const productService = require('../../services/productService');

Page({
  data: {
    searchKeyword: '',
    currentCategory: 'all',
    currentFilter: 'all',
    products: [],
    allProducts: [],
    searchHistory: [],
    hotSearches: ['洗衣液', '抽纸', '面膜', '口红', '零食'],
    showSearchPanel: false,
    page: 1,
    pageSize: 10,
    loading: false,
    hasMore: true,
    // Banner轮播图
    banners: [
      {
        id: 1,
        image: 'https://picsum.photos/750/280?random=101',
        title: '新人高佣专场',
        subtitle: '佣金提升30% 限时开启',
        type: 'activity',
        link: '/pages/rank/rank'
      },
      {
        id: 2,
        image: 'https://picsum.photos/750/280?random=102',
        title: '春日爆品计划',
        subtitle: '已售10万+ 佣金25%',
        type: 'product',
        productId: 6
      },
      {
        id: 3,
        image: 'https://picsum.photos/750/280?random=103',
        title: '正品保障・极速发货',
        subtitle: '7天无理由退换',
        type: 'brand',
        link: ''
      },
      {
        id: 4,
        image: 'https://picsum.photos/750/280?random=104',
        title: '申请样品攻略',
        subtitle: '免费领样 轻松带货',
        type: 'guide',
        link: ''
      }
    ],
    // 二级筛选
    filterOptions: {
      commission: [
        { label: '不限', value: 'all', min: 0 },
        { label: '10%以上', value: '10', min: 10 },
        { label: '20%以上', value: '20', min: 20 },
        { label: '30%以上', value: '30', min: 30 }
      ],
      price: [
        { label: '不限', value: 'all', min: 0, max: 99999 },
        { label: '50元以下', value: '50', min: 0, max: 50 },
        { label: '50-100元', value: '50-100', min: 50, max: 100 },
        { label: '100-500元', value: '100-500', min: 100, max: 500 },
        { label: '500元以上', value: '500', min: 500, max: 99999 }
      ],
      sales: [
        { label: '不限', value: 'all', min: 0 },
        { label: '1万+', value: '1w', min: 10000 },
        { label: '5万+', value: '5w', min: 50000 },
        { label: '10万+', value: '10w', min: 100000 }
      ]
    },
    currentFilters: {
      commission: 'all',
      price: 'all',
      sales: 'all'
    },
    showFilterPanel: false
  },

  onLoad() {
    this.checkLoginStatus();
    this.loadProducts();
    this.loadSearchHistory();
  },

  // 检查登录状态
  checkLoginStatus() {
    const token = wx.getStorageSync('token');
    if (!token) {
      console.log('用户未登录');
    }
  },

  // 加载搜索历史
  loadSearchHistory() {
    const history = wx.getStorageSync('searchHistory') || [];
    this.setData({ searchHistory: history });
  },

  // 保存搜索历史
  saveSearchHistory(keyword) {
    if (!keyword.trim()) return;
    let history = this.data.searchHistory;
    // 去重并放到最前面
    history = history.filter(item => item !== keyword);
    history.unshift(keyword);
    // 只保留10条
    history = history.slice(0, 10);
    this.setData({ searchHistory: history });
    wx.setStorageSync('searchHistory', history);
  },

  // 加载商品数据
  async loadProducts(refresh = false) {
    if (this.data.loading) return;
    
    this.setData({ loading: true });
    
    try {
      const page = refresh ? 1 : this.data.page;
      const params = {
        page,
        pageSize: this.data.pageSize
      };
      
      // 添加分类筛选
      if (this.data.currentCategory !== 'all') {
        params.category = this.data.currentCategory;
      }
      
      // 添加关键词搜索
      if (this.data.searchKeyword) {
        params.keyword = this.data.searchKeyword;
      }
      
      // 添加排序
      if (this.data.currentFilter === 'commission') {
        params.sortBy = 'commission';
        params.sortOrder = 'desc';
      } else if (this.data.currentFilter === 'sales') {
        params.sortBy = 'sales';
        params.sortOrder = 'desc';
      }
      
      const res = await productService.getProducts(params);
      
      if (res.code === 200) {
        const products = res.data.list.map(item => ({
          id: item.id,
          image: item.image,
          title: item.name,
          price: item.price.toString(),
          commissionRate: item.commissionRate,
          commissionAmount: item.commissionAmount.toString(),
          sales: item.sales,
          salesText: item.monthlySales.replace('月销', '').replace('件', ''),
          tags: item.tags,
          isBrand: item.isBrand,
          hasCashback: item.hasCashback
        }));
        
        this.setData({
          products: refresh ? products : [...this.data.products, ...products],
          allProducts: refresh ? products : [...this.data.allProducts, ...products],
          page: page + 1,
          hasMore: products.length === this.data.pageSize,
          loading: false
        });
      } else {
        throw new Error(res.message || '获取商品失败');
      }
    } catch (error) {
      console.error('加载商品失败:', error);
      this.setData({ loading: false });
      wx.showToast({
        title: '加载失败，使用默认数据',
        icon: 'none'
      });
      // 使用默认数据
      this.loadDefaultProducts();
    }
  },

  // 加载默认商品数据（当API失败时使用）
  loadDefaultProducts() {
    const products = [
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
        tag: '爆款',
        tags: ['正品保障', '7天无理由', '运费险'],
        shop: '立白官方旗舰店',
        shopScore: 4.9,
        location: '广东广州'
      }
    ];

    this.setData({
      products: products,
      allProducts: products
    });
  },

  // 搜索输入
  onSearchInput(e) {
    this.setData({
      searchKeyword: e.detail.value
    });
  },

  // 显示搜索面板
  onSearchFocus() {
    this.setData({ showSearchPanel: true });
  },

  // 隐藏搜索面板
  onSearchBlur() {
    // 延迟隐藏，给点击事件留出时间
    setTimeout(() => {
      this.setData({ showSearchPanel: false });
    }, 300);
  },

  // 点击热门搜索
  onHotSearchTap(e) {
    const keyword = e.currentTarget.dataset.keyword;
    this.setData({ searchKeyword: keyword });
    this.onSearch();
  },

  // 点击历史搜索
  onHistoryTap(e) {
    const keyword = e.currentTarget.dataset.keyword;
    this.setData({ searchKeyword: keyword });
    this.onSearch();
  },

  // 清除搜索历史
  clearHistory() {
    wx.removeStorageSync('searchHistory');
    this.setData({ searchHistory: [] });
  },

  // 搜索
  async onSearch() {
    const keyword = this.data.searchKeyword.trim();
    this.setData({ showSearchPanel: false });
    
    if (!keyword) {
      this.setData({
        page: 1,
        products: []
      });
      this.loadProducts(true);
      return;
    }

    this.saveSearchHistory(keyword);

    try {
      wx.showLoading({ title: '搜索中...' });
      const res = await productService.searchProducts(keyword, {
        page: 1,
        pageSize: this.data.pageSize
      });
      wx.hideLoading();
      
      if (res.code === 200) {
        const products = res.data.list.map(item => ({
          id: item.id,
          image: item.image,
          title: item.name,
          price: item.price.toString(),
          commissionRate: item.commissionRate,
          commissionAmount: item.commissionAmount.toString(),
          sales: item.sales,
          salesText: item.monthlySales.replace('月销', '').replace('件', ''),
          tags: item.tags,
          isBrand: item.isBrand,
          hasCashback: item.hasCashback
        }));
        
        this.setData({
          products: products,
          page: 2,
          hasMore: products.length === this.data.pageSize
        });

        if (products.length === 0) {
          wx.showToast({
            title: '未找到相关商品',
            icon: 'none'
          });
        }
      }
    } catch (error) {
      wx.hideLoading();
      console.error('搜索失败:', error);
      wx.showToast({
        title: '搜索失败',
        icon: 'none'
      });
    }
  },

  // 切换分类
  switchCategory(e) {
    const category = e.currentTarget.dataset.category;
    this.setData({
      currentCategory: category
    });
    this.applyFilters();
  },

  // 跳转到分类页面
  goToCategory(e) {
    const category = e.currentTarget.dataset.category;
    wx.navigateTo({
      url: '/pages/category/category?category=' + category
    });
  },

  // 切换筛选
  switchFilter(e) {
    const filter = e.currentTarget.dataset.filter;
    this.setData({
      currentFilter: filter
    });
    this.applyFilters();
  },

  // 显示筛选面板
  toggleFilterPanel() {
    this.setData({
      showFilterPanel: !this.data.showFilterPanel
    });
  },

  // 选择二级筛选
  selectSubFilter(e) {
    const { type, value } = e.currentTarget.dataset;
    const currentFilters = this.data.currentFilters;
    currentFilters[type] = value;
    this.setData({ currentFilters });
    this.applyFilters();
  },

  // 应用筛选
  applyFilters() {
    let filtered = this.data.allProducts;
    const filters = this.data.currentFilters;

    // 佣金筛选
    if (filters.commission !== 'all') {
      const minCommission = parseInt(filters.commission);
      filtered = filtered.filter(p => p.commissionRate >= minCommission);
    }

    // 价格筛选
    if (filters.price !== 'all') {
      const priceOption = this.data.filterOptions.price.find(p => p.value === filters.price);
      if (priceOption) {
        filtered = filtered.filter(p => {
          const price = parseFloat(p.price);
          return price >= priceOption.min && price <= priceOption.max;
        });
      }
    }

    // 销量筛选
    if (filters.sales !== 'all') {
      const salesOption = this.data.filterOptions.sales.find(s => s.value === filters.sales);
      if (salesOption) {
        filtered = filtered.filter(p => p.sales >= salesOption.min);
      }
    }

    // 主筛选（精选/热销/新品/高佣）
    switch (this.data.currentFilter) {
      case 'hot':
        filtered = filtered.sort((a, b) => b.sales - a.sales);
        break;
      case 'commission':
        filtered = filtered.sort((a, b) => b.commissionRate - a.commissionRate);
        break;
      case 'new':
        filtered = filtered.filter(p => p.tag === '新品' || p.tag === '精选');
        break;
    }

    this.setData({ products: filtered });
  },

  // Banner点击
  onBannerTap(e) {
    const item = e.currentTarget.dataset.item;
    
    switch (item.type) {
      case 'activity':
        if (item.link) {
          wx.navigateTo({ url: item.link });
        }
        break;
      case 'product':
        if (item.productId) {
          wx.navigateTo({
            url: '/pages/product-detail/product-detail?id=' + item.productId
          });
        }
        break;
      case 'brand':
        wx.showToast({
          title: '品牌保障说明',
          icon: 'none'
        });
        break;
      case 'guide':
        wx.showToast({
          title: '样品攻略详情',
          icon: 'none'
        });
        break;
      default:
        break;
    }
  },

  // 快捷入口点击
  onEntryTap(e) {
    const type = e.currentTarget.dataset.type;
    const pageMap = {
      hot: '/pages/activity/hot',
      follow: '/pages/activity/follow',
      video: '/pages/activity/video',
      merchant: '/pages/activity/merchant',
      cheap: '/pages/activity/cheap'
    };
    
    const url = pageMap[type];
    if (url) {
      wx.navigateTo({ url });
    }
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
    const productId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/sample-apply/sample-apply?productId=' + productId
    });
  },

  // 下拉刷新
  async onPullDownRefresh() {
    this.setData({
      page: 1,
      products: []
    });
    await this.loadProducts(true);
    wx.stopPullDownRefresh();
  },

  // 上拉加载更多
  onReachBottom() {
    if (this.data.hasMore && !this.data.loading) {
      this.loadProducts();
    }
  }
});
