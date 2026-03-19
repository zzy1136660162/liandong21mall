const productService = require('../../services/productService');

Page({
  data: {
    searchKeyword: '',
    searchStatus: 'home', // home-首页, result-搜索结果
    searchHistory: [],
    searchSuggestions: [],
    showSuggestions: false,
    products: [],
    page: 1,
    pageSize: 10,
    loading: false,
    hasMore: true,
    currentSort: 'default',
    hotSearches: ['洗衣液', '抽纸', '面膜', '口红', '零食', '手机', '奶粉', '耳机', '水果', '猪肉', '饮料', '床品']
  },

  onLoad() {
    this.loadSearchHistory();
  },

  loadSearchHistory() {
    const history = wx.getStorageSync('searchHistory') || [];
    this.setData({ searchHistory: history });
  },

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
    
    const suggestions = allKeywords.filter(k => k.includes(keyword)).slice(0, 6);
    this.setData({ searchSuggestions: suggestions });
  },

  clearInput() {
    this.setData({
      searchKeyword: '',
      showSuggestions: false,
      searchSuggestions: []
    });
  },

  goToCamera() {
    wx.navigateTo({
      url: '/pages/camera/camera'
    });
  },

  onSuggestionTap(e) {
    const keyword = e.currentTarget.dataset.keyword;
    this.setData({
      searchKeyword: keyword,
      showSuggestions: false,
      searchSuggestions: []
    });
    this.doSearch(keyword);
  },

  onHistoryTap(e) {
    const keyword = e.currentTarget.dataset.keyword;
    this.setData({ searchKeyword: keyword });
    this.doSearch(keyword);
  },

  onHotSearchTap(e) {
    const keyword = e.currentTarget.dataset.keyword;
    this.setData({ searchKeyword: keyword });
    this.doSearch(keyword);
  },

  clearHistory() {
    wx.removeStorageSync('searchHistory');
    this.setData({ searchHistory: [] });
  },

  saveSearchHistory(keyword) {
    if (!keyword.trim()) return;
    let history = this.data.searchHistory;
    history = history.filter(item => item !== keyword);
    history.unshift(keyword);
    history = history.slice(0, 10);
    this.setData({ searchHistory: history });
    wx.setStorageSync('searchHistory', history);
  },

  onSearch() {
    const keyword = this.data.searchKeyword.trim();
    if (!keyword) {
      wx.showToast({ title: '请输入搜索关键词', icon: 'none' });
      return;
    }
    this.doSearch(keyword);
  },

  async doSearch(keyword, sort = 'default') {
    if (!keyword) return;

    this.setData({ 
      searchStatus: 'result',
      showSuggestions: false,
      products: [],
      page: 1,
      loading: true
    });

    this.saveSearchHistory(keyword);

    try {
      const res = await productService.searchProducts(keyword, {
        page: 1,
        pageSize: this.data.pageSize,
        sort: sort
      });
      
      if (res.code === 200) {
        const products = res.data.list.map(item => ({
          id: item.id,
          image: item.image,
          title: item.name,
          price: item.price.toString(),
          originalPrice: item.originalPrice ? item.originalPrice.toString() : '',
          commissionRate: item.commissionRate,
          commissionAmount: item.commissionAmount ? item.commissionAmount.toString() : '0',
          sales: item.sales || 0
        }));
        
        this.setData({
          products: products,
          page: 2,
          hasMore: products.length === this.data.pageSize,
          loading: false,
          currentSort: sort
        });
      }
    } catch (error) {
      console.error('搜索失败:', error);
      wx.showToast({ title: '搜索失败', icon: 'none' });
      this.setData({ loading: false });
    }
  },

  async loadMore() {
    if (this.data.loading || !this.data.hasMore) return;
    
    const keyword = this.data.searchKeyword;
    if (!keyword) return;

    this.setData({ loading: true });

    try {
      const res = await productService.searchProducts(keyword, {
        page: this.data.page,
        pageSize: this.data.pageSize,
        sort: this.data.currentSort
      });
      
      if (res.code === 200) {
        const newProducts = res.data.list.map(item => ({
          id: item.id,
          image: item.image,
          title: item.name,
          price: item.price.toString(),
          originalPrice: item.originalPrice ? item.originalPrice.toString() : '',
          commissionRate: item.commissionRate,
          commissionAmount: item.commissionAmount ? item.commissionAmount.toString() : '0',
          sales: item.sales || 0
        }));
        
        this.setData({
          products: [...this.data.products, ...newProducts],
          page: this.data.page + 1,
          hasMore: newProducts.length === this.data.pageSize,
          loading: false
        });
      }
    } catch (error) {
      console.error('加载更多失败:', error);
      this.setData({ loading: false });
    }
  },

  onSortChange(e) {
    const sort = e.currentTarget.dataset.value;
    this.setData({ currentSort: sort });
    this.doSearch(this.data.searchKeyword, sort);
  },

  goToDetail(e) {
    const productId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/product-detail/product-detail?id=' + productId
    });
  }
});
