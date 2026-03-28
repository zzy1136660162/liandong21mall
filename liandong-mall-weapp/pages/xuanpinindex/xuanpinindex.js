const productService = require('../../services/productService');

Page({
  data: {
    currentCategory: 'all',
    currentFilter: 'all',
    products: [],
    allProducts: [],
    searchHistory: [],
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
      console.log('API返回数据:', res);
      console.log('商品列表:', res.list);
      
      const list = res.list || [];
      console.log('处理后的列表:', list);
      
      const products = list.map(item => ({
        id: item.id,
        image: item.image,
        title: item.name || item.title,
        price: typeof item.price === 'number' ? item.price.toString() : item.price,
        originalPrice: item.originalPrice ? item.originalPrice.toString() : '',
        commissionRate: item.commissionRate || 0,
        commissionAmount: item.commissionAmount ? item.commissionAmount.toString() : (item.commissionRate ? (parseFloat(item.price) * item.commissionRate / 100).toFixed(2) : '0'),
        sales: item.sales || 0,
        salesText: item.monthlySales ? item.monthlySales.replace('月销', '').replace('件', '') : (item.sales ? item.sales.toString() : '0'),
        tags: item.tags || [],
        isBrand: item.isBrand || false,
        hasCashback: item.hasCashback || false
      }));

      this.setData({
        products: refresh ? products : [...this.data.products, ...products],
        allProducts: refresh ? products : [...this.data.allProducts, ...products],
        page: page + 1,
        hasMore: products.length === this.data.pageSize,
        loading: false
      });
    } catch (error) {
      console.error('加载商品失败:', error);
      this.setData({ loading: false, products: [], allProducts: [] });
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    }
  },

  // 搜索输入
  onSearchInput(e) {
    const keyword = e.detail.value;
    this.setData({
      searchKeyword: keyword,
      showSuggestions: keyword.length > 0
    });
    
    if (keyword.length > 0) {
      this.getSearchSuggestions(keyword);
    } else {
      this.setData({ searchSuggestions: [] });
    }
  },

  // 获取搜索联想（本地实现）
  getSearchSuggestions(keyword) {
    const allKeywords = [
      '洗衣液', '洗衣粉', '洗衣凝珠', '洗衣皂',
      '抽纸', '卷纸', '湿巾', '厨房纸',
      '面膜', '面霜', '乳液', '精华', '口红', '唇膏',
      '零食', '坚果', '饼干', '糖果', '巧克力',
      '饮料', '矿泉水', '果汁', '奶茶', '咖啡',
      '手机', '耳机', '充电宝', '数据线', '手机壳',
      '奶粉', '尿不湿', '奶瓶', '婴儿油', '儿童玩具',
      '猪肉', '牛肉', '鸡肉', '海鲜', '水果', '蔬菜',
      '床品', '四件套', '被子', '枕头', '凉席'
    ];
    
    const suggestions = allKeywords.filter(k => k.includes(keyword)).slice(0, 5);
    this.setData({ searchSuggestions: suggestions });
  },

  // 点击联想词
  onSuggestionTap(e) {
    const keyword = e.currentTarget.dataset.keyword;
    this.setData({
      searchKeyword: keyword,
      showSuggestions: false,
      showSearchPanel: false
    });
    this.doSearch(keyword);
  },

  // 显示搜索面板
  showSearchPanel() {
    console.log('显示搜索面板');
    this.setData({ showSearchPanel: true });
  },

  // 隐藏搜索面板
  hideSearchPanel() {
    this.setData({ showSearchPanel: false });
  },

  // 显示搜索面板（focus时）
  onSearchFocus() {
    console.log('onSearchFocus');
    this.setData({ showSearchPanel: true });
  },

  // 隐藏搜索面板（blur时）
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

  // 执行搜索
  async doSearch(keyword, sort = 'default') {
    if (!keyword) return;

    this.setData({ 
      searchStatus: 'searching',
      showSearchPanel: false,
      showSuggestions: false
    });

    this.saveSearchHistory(keyword);

    try {
      wx.showLoading({ title: '搜索中...' });
      const res = await productService.searchProducts(keyword, {
        page: 1,
        pageSize: this.data.pageSize,
        sort: sort
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
          salesText: item.monthlySales ? item.monthlySales.replace('月销', '').replace('件', '') : '0',
          tags: item.tags,
          isBrand: item.isBrand,
          hasCashback: item.hasCashback
        }));
        
        this.setData({
          products: products,
          page: 2,
          hasMore: products.length === this.data.pageSize,
          searchStatus: 'result',
          currentSort: sort
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
      wx.showToast({ title: '搜索失败', icon: 'none' });
      this.setData({ searchStatus: 'home' });
    }
  },

  // 点击搜索按钮
  async onSearch() {
    const keyword = this.data.searchKeyword.trim();
    console.log('搜索:', keyword);
    
    if (!keyword) {
      wx.showToast({ title: '请输入搜索关键词', icon: 'none' });
      return;
    }

    this.doSearch(keyword, this.data.currentSort);
  },

  // 排序筛选
  onSortChange(e) {
    const sort = e.currentTarget.dataset.value;
    const keyword = this.data.searchKeyword;
    
    this.setData({ currentSort: sort });
    
    if (this.data.searchStatus === 'result' && keyword) {
      this.doSearch(keyword, sort);
    }
  },

  // 清空搜索，回到首页
  clearSearch() {
    this.setData({
      searchKeyword: '',
      searchStatus: 'home',
      showSearchPanel: false,
      showSuggestions: false,
      products: this.data.allProducts,
      page: 1,
      hasMore: true
    });
    this.loadProducts(true);
  },

  // 切换分类
  switchCategory(e) {
    const category = e.currentTarget.dataset.category;
    console.log('切换分类:', category);
    this.setData({
      currentCategory: category,
      products: this.data.allProducts
    });
  },

  // 跳转到分类页面
  goToCategory(e) {
    const category = e.currentTarget.dataset.category;
    wx.navigateTo({
      url: '/pages/category/category?category=' + category
    });
  },

  // 跳转到搜索页面
  goToSearch() {
    wx.navigateTo({
      url: '/pages/search/search'
    });
  },

  // 跳转到相机页面
  goToCamera() {
    wx.showActionSheet({
      itemList: ['拍照识别', '扫码识别'],
      success: (res) => {
        if (res.tapIndex === 0) {
          wx.chooseMedia({
            count: 1,
            mediaType: ['image'],
            sourceType: ['camera'],
            success: (photoRes) => {
              const tempFilePath = photoRes.tempFiles[0].tempFilePath;
              this.processImage(tempFilePath);
            }
          });
        } else {
          wx.scanCode({
            success: (scanRes) => {
              if (scanRes.result) {
                this.processScanResult(scanRes.result);
              }
            }
          });
        }
      }
    });
  },

  // 处理拍照识别结果
  processImage(imagePath) {
    wx.showLoading({ title: '识别中...' });
    // TODO: 调用图像识别API
    setTimeout(() => {
      wx.hideLoading();
      wx.showToast({
        title: '图片已选择',
        icon: 'none'
      });
    }, 1000);
  },

  // 处理扫码结果
  processScanResult(result) {
    wx.showLoading({ title: '识别中...' });
    // TODO: 调用扫码结果处理API
    setTimeout(() => {
      wx.hideLoading();
      wx.showToast({
        title: '扫码成功',
        icon: 'none'
      });
    }, 1000);
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
