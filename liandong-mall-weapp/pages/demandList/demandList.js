const app = getApp();

Page({
  data: {
    demandList: [],
    currentStatus: '',
    page: 1,
    pageSize: 10,
    hasMore: true,
    loading: false
  },

  onLoad() {
    this.loadDemandList();
  },

  onShow() {
    // 每次显示页面时刷新列表
    this.setData({ page: 1, hasMore: true });
    this.loadDemandList();
  },

  onPullDownRefresh() {
    this.setData({ page: 1, hasMore: true });
    this.loadDemandList(() => {
      wx.stopPullDownRefresh();
    });
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.loading) {
      this.loadMore();
    }
  },

  // 加载需求列表
  loadDemandList(callback) {
    const { currentStatus, page, pageSize } = this.data;
    const submitterId = app.globalData.userId;

    console.log('需求列表页 - submitterId:', submitterId);
    console.log('需求列表页 - app.globalData:', app.globalData);

    this.setData({ loading: true });

    let url = `/demand/list?submitterId=${submitterId}&page=${page}&pageSize=${pageSize}`;
    if (currentStatus !== '') {
      url += `&status=${currentStatus}`;
    }

    app.request({
      url,
      success: (res) => {
        console.log('需求列表页 - 返回数据:', res);
        console.log('需求列表页 - res.data:', res.data);
        const { list, total, page: currentPage } = res.data;
        console.log('需求列表页 - list:', list, 'total:', total, 'currentPage:', currentPage);
        
        const formattedList = list.map(item => ({
          ...item,
          statusClass: this.getStatusClass(item.status)
        }));
        console.log('需求列表页 - formattedList:', formattedList);

        this.setData({
          demandList: page === 1 ? formattedList : [...this.data.demandList, ...formattedList],
          hasMore: currentPage * pageSize < total,
          loading: false
        }, () => {
          console.log('需求列表页 - setData后 demandList:', this.data.demandList);
        });

        callback && callback();
      },
      fail: () => {
        this.setData({ loading: false });
        callback && callback();
      }
    });
  },

  // 获取状态样式类名
  getStatusClass(status) {
    const classMap = {
      0: 'pending',
      1: 'confirming',
      2: 'developing',
      3: 'sampling',
      4: 'completed',
      5: 'cancelled'
    };
    return classMap[status] || 'pending';
  },

  // 按状态筛选
  filterByStatus(e) {
    const { status } = e.currentTarget.dataset;
    this.setData({
      currentStatus: status,
      page: 1,
      hasMore: true,
      demandList: []
    });
    this.loadDemandList();
  },

  // 加载更多
  loadMore() {
    this.setData({
      page: this.data.page + 1
    });
    this.loadDemandList();
  },

  // 跳转到详情
  goToDetail(e) {
    const id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/demandDetail/demandDetail?id=${id}`
    });
  },

  // 跳转到提交页面
  goToSubmit() {
    wx.navigateTo({
      url: '/pages/demandSubmit/demandSubmit'
    });
  },

  // 撤回需求
  withdrawDemand(e) {
    const { id, index } = e.currentTarget.dataset;
    
    wx.showModal({
      title: '确认撤回',
      content: '撤回后该需求将取消，是否确认？',
      confirmColor: '#ff4d4f',
      success: (res) => {
        if (res.confirm) {
          this.doWithdraw(id, index);
        }
      }
    });
  },

  // 执行撤回
  doWithdraw(demandId, index) {
    const submitterId = app.globalData.userId;

    wx.showLoading({ title: '处理中...' });

    app.request({
      url: '/demand/withdraw',
      method: 'POST',
      data: {
        demandId: parseInt(demandId),
        submitterId
      },
      success: (res) => {
        wx.hideLoading();
        wx.showToast({
          title: '已撤回',
          icon: 'success'
        });
        
        // 更新列表数据
        const demandList = this.data.demandList;
        demandList[index].status = 5;
        demandList[index].statusText = '已取消';
        demandList[index].statusClass = 'cancelled';
        
        this.setData({ demandList });
        
        // 如果当前筛选不是全部，刷新列表
        if (this.data.currentStatus !== '') {
          this.loadDemandList();
        }
      },
      fail: () => {
        wx.hideLoading();
      }
    });
  },

  // 重新申请
  reapplyDemand(e) {
    const { id, index } = e.currentTarget.dataset;
    
    wx.showModal({
      title: '确认重新申请',
      content: '重新申请后将生成新的需求编号，是否确认？',
      confirmColor: '#faad14',
      success: (res) => {
        if (res.confirm) {
          this.doReapply(id, index);
        }
      }
    });
  },

  // 执行重新申请
  doReapply(demandId, index) {
    const submitterId = app.globalData.userId;

    wx.showLoading({ title: '处理中...' });

    app.request({
      url: '/demand/reapply',
      method: 'POST',
      data: {
        demandId: parseInt(demandId),
        submitterId
      },
      success: (res) => {
        wx.hideLoading();
        wx.showToast({
          title: '重新申请成功',
          icon: 'success'
        });
        
        // 更新列表数据
        const demandList = this.data.demandList;
        demandList[index].status = 0;
        demandList[index].statusText = '待处理';
        demandList[index].statusClass = 'pending';
        demandList[index].demandNo = res.data.demandNo;
        
        this.setData({ demandList });
        
        // 如果当前筛选不是全部或已取消，刷新列表
        if (this.data.currentStatus !== '' && this.data.currentStatus !== '5') {
          this.loadDemandList();
        }
      },
      fail: () => {
        wx.hideLoading();
      }
    });
  },

  // 删除需求
  deleteDemand(e) {
    const { id, index } = e.currentTarget.dataset;
    
    wx.showModal({
      title: '确认删除',
      content: '删除后数据将无法恢复，是否确认？',
      confirmColor: '#ff4d4f',
      success: (res) => {
        if (res.confirm) {
          this.doDelete(id, index);
        }
      }
    });
  },

  // 执行删除
  doDelete(demandId, index) {
    const submitterId = app.globalData.userId;

    wx.showLoading({ title: '处理中...' });

    app.request({
      url: '/demand/delete',
      method: 'POST',
      data: {
        demandId: parseInt(demandId),
        submitterId
      },
      success: (res) => {
        wx.hideLoading();
        wx.showToast({
          title: '已删除',
          icon: 'success'
        });
        
        // 从列表中移除
        const demandList = this.data.demandList;
        demandList.splice(index, 1);
        
        this.setData({ 
          demandList,
          // 如果删除后列表为空，显示空状态
          hasMore: demandList.length > 0
        });
      },
      fail: () => {
        wx.hideLoading();
      }
    });
  }
});
