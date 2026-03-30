const app = getApp();

Page({
  data: {
    talentList: [],
    page: 1,
    pageSize: 10,
    hasMore: true,
    loading: false,
    keyword: '',
    currentArea: '',
    areas: ['全部', '化妆品研发', '功能性食品', '天然原料', '项目管理', '功效评测', '包装研发', '品质控制'],
    searchKeyword: ''
  },

  onLoad() {
    this.loadTalentList();
  },

  onShow() {
    // 每次显示页面时刷新列表
    this.setData({ page: 1, hasMore: true });
    this.loadTalentList();
  },

  onPullDownRefresh() {
    this.setData({ page: 1, hasMore: true });
    this.loadTalentList(() => {
      wx.stopPullDownRefresh();
    });
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.loading) {
      this.loadMore();
    }
  },

  loadTalentList(callback) {
    const { page, pageSize, currentArea, searchKeyword } = this.data;

    if (this.data.loading) return;
    this.setData({ loading: true });

    let url = `/api/talent_pool/list?page=${page}&pageSize=${pageSize}`;
    if (currentArea && currentArea !== '全部') {
      url += `&area=${encodeURIComponent(currentArea)}`;
    }
    if (searchKeyword) {
      url += `&keyword=${encodeURIComponent(searchKeyword)}`;
    }

    app.request({
      url,
      success: (res) => {
        const { list, total, currentPage, totalPages } = res.data;
        this.setData({
          talentList: page === 1 ? list : [...this.data.talentList, ...list],
          hasMore: currentPage < totalPages,
          loading: false
        });
        callback && callback();
      },
      fail: () => {
        this.setData({ loading: false });
        callback && callback();
      }
    });
  },

  loadMore() {
    this.setData({ page: this.data.page + 1 });
    this.loadTalentList();
  },

  onSearch(e) {
    const keyword = e.detail.value || '';
    this.setData({
      searchKeyword: keyword,
      page: 1,
      hasMore: true
    });
    this.loadTalentList();
  },

  onSearchConfirm(e) {
    const keyword = e.detail.value || '';
    this.setData({
      searchKeyword: keyword,
      page: 1,
      hasMore: true
    });
    this.loadTalentList();
  },

  clearSearch() {
    this.setData({
      searchKeyword: '',
      page: 1,
      hasMore: true
    });
    this.loadTalentList();
  },

  filterByArea(e) {
    const area = e.currentTarget.dataset.area;
    this.setData({
      currentArea: area,
      page: 1,
      hasMore: true
    });
    this.loadTalentList();
  },

  goToDetail(e) {
    const { id } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/talent_pool/detail/detail?id=${id}`
    });
  }
});
