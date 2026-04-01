const app = getApp();

Page({
  data: {
    demandId: null,
    detail: {},
    statusClass: ''
  },

  onLoad(options) {
    const { id } = options;
    if (!id) {
      wx.showToast({
        title: '参数错误',
        icon: 'none'
      });
      wx.navigateBack();
      return;
    }

    this.setData({ demandId: id });
    this.loadDetail();
  },

  // 加载详情
  loadDetail() {
    const { demandId } = this.data;
    const submitterId = app.globalData.userId;

    app.request({
      url: `/demand/detail/${demandId}?submitterId=${submitterId}`,
      success: (res) => {
        this.setData({
          detail: res.data,
          statusClass: this.getStatusClass(res.data.status)
        });
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

  // 查看进度
  viewProgress() {
    const { demandId } = this.data;
    wx.navigateTo({
      url: `/pages/demandProgress/demandProgress?demandId=${demandId}`
    });
  },

  // 撤回需求
  withdrawDemand() {
    const { demandId, detail } = this.data;
    
    // 只有待处理状态可以撤回
    if (detail.status !== 0) {
      wx.showToast({
        title: '该需求状态不允许撤回',
        icon: 'none'
      });
      return;
    }

    wx.showModal({
      title: '确认撤回',
      content: '撤回后该需求将取消，是否确认？',
      confirmColor: '#ff4d4f',
      success: (res) => {
        if (res.confirm) {
          this.doWithdraw();
        }
      }
    });
  },

  // 执行撤回
  doWithdraw() {
    const { demandId } = this.data;
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
        
        // 刷新详情
        this.loadDetail();
        
        // 通知列表页刷新
        const pages = getCurrentPages();
        const prevPage = pages[pages.length - 2];
        if (prevPage && prevPage.route === 'pages/demandList/demandList') {
          prevPage.setData({ page: 1 });
          prevPage.loadDemandList();
        }
      },
      fail: () => {
        wx.hideLoading();
      }
    });
  },

  // 重新申请
  reapplyDemand() {
    const { demandId, detail } = this.data;
    
    // 只有已取消状态可以重新申请
    if (detail.status !== 5) {
      wx.showToast({
        title: '该需求状态不允许重新申请',
        icon: 'none'
      });
      return;
    }

    wx.showModal({
      title: '确认重新申请',
      content: '重新申请后将生成新的需求编号，是否确认？',
      confirmColor: '#faad14',
      success: (res) => {
        if (res.confirm) {
          this.doReapply();
        }
      }
    });
  },

  // 执行重新申请
  doReapply() {
    const { demandId } = this.data;
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
        
        // 刷新详情
        this.loadDetail();
        
        // 通知列表页刷新
        const pages = getCurrentPages();
        const prevPage = pages[pages.length - 2];
        if (prevPage && prevPage.route === 'pages/demandList/demandList') {
          prevPage.setData({ page: 1 });
          prevPage.loadDemandList();
        }
      },
      fail: () => {
        wx.hideLoading();
      }
    });
  },

  // 删除需求
  deleteDemand() {
    const { demandId, detail } = this.data;
    
    // 只有已取消状态可以删除
    if (detail.status !== 5) {
      wx.showToast({
        title: '该需求状态不允许删除',
        icon: 'none'
      });
      return;
    }

    wx.showModal({
      title: '确认删除',
      content: '删除后数据将无法恢复，是否确认？',
      confirmColor: '#ff4d4f',
      success: (res) => {
        if (res.confirm) {
          this.doDelete();
        }
      }
    });
  },

  // 执行删除
  doDelete() {
    const { demandId } = this.data;
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
        
        // 返回列表页
        setTimeout(() => {
          wx.navigateBack();
        }, 1500);
      },
      fail: () => {
        wx.hideLoading();
      }
    });
  }
});
