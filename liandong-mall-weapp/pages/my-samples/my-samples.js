const { isLogin } = require('../../utils/user');

Page({
  data: {
    currentFilter: 'all',
    filterText: '',
    sampleList: [],
    hasMore: true,
    page: 1,
    pageSize: 10
  },

  // 筛选标签映射
  filterMap: {
    'all': '',
    'pending': '待审核',
    'approved': '审核通过',
    'shipped': '已寄出',
    'rejected': '已拒绝'
  },

  onLoad() {
    // 检查登录状态
    if (!isLogin()) {
      wx.showModal({
        title: '提示',
        content: '请先登录',
        confirmText: '去登录',
        success: (res) => {
          if (res.confirm) {
            wx.redirectTo({
              url: '/pages/login/index?redirect=/pages/my-samples/my-samples'
            });
          }
        }
      });
      return;
    }
    this.loadSampleList();
  },

  onShow() {
    // 每次显示页面时刷新列表
    this.loadSampleList();
  },

  // 加载样品申请列表
  loadSampleList() {
    // 从本地存储获取申请记录（模拟数据）
    const applications = wx.getStorageSync('sampleApplications') || [];
    
    // 如果没有数据，创建一些模拟数据
    let sampleList = applications;
    if (sampleList.length === 0) {
      sampleList = this.getMockData();
    }

    // 根据当前筛选条件过滤
    const filteredList = this.filterList(sampleList, this.data.currentFilter);

    this.setData({
      sampleList: filteredList,
      filterText: this.filterMap[this.data.currentFilter],
      hasMore: false // 模拟没有更多数据
    });
  },

  // 获取模拟数据
  getMockData() {
    return [
      {
        id: 'SA1773469050335',
        applyTime: '2026-03-14 06:17',
        status: 'pending',
        statusText: '待审核',
        shipStatus: 'not_shipped',
        shipStatusText: '未寄出',
        products: [
          {
            id: 1,
            image: 'https://picsum.photos/140/140?random=1',
            name: '立白大师香氛洗衣液持久留香护色护衣',
            price: '39.9',
            commission: '20%'
          }
        ]
      },
      {
        id: 'SA1773469050336',
        applyTime: '2026-03-13 15:20:00',
        status: 'approved',
        statusText: '审核通过',
        shipStatus: 'not_shipped',
        shipStatusText: '未寄出',
        products: [
          {
            id: 2,
            image: 'https://picsum.photos/140/140?random=2',
            name: '漫花悬挂式抽纸整箱批发家用实惠装',
            price: '29.9',
            commission: '15%'
          }
        ]
      },
      {
        id: 'SA1773469050337',
        applyTime: '2026-03-12 09:15:00',
        status: 'approved',
        statusText: '审核通过',
        shipStatus: 'shipped',
        shipStatusText: '已寄出',
        logisticsCompany: '顺丰速运',
        trackingNo: 'SF1234567890',
        products: [
          {
            id: 3,
            image: 'https://picsum.photos/140/140?random=3',
            name: '维达超韧抽纸3层130抽24包整箱',
            price: '45.9',
            commission: '18%'
          }
        ]
      },
      {
        id: 'SA1773469050338',
        applyTime: '2026-03-10 14:30:00',
        status: 'approved',
        statusText: '审核通过',
        shipStatus: 'received',
        shipStatusText: '已签收',
        logisticsCompany: '圆通快递',
        trackingNo: 'YT9876543210',
        receiveTime: '2026-03-12 10:30',
        products: [
          {
            id: 4,
            image: 'https://picsum.photos/140/140?random=4',
            name: '心相印茶语系列抽纸3层100抽',
            price: '35.9',
            commission: '12%'
          },
          {
            id: 5,
            image: 'https://picsum.photos/140/140?random=5',
            name: '清风原木纯品抽纸3层100抽',
            price: '32.9',
            commission: '10%'
          }
        ]
      },
      {
        id: 'SA1773469050339',
        applyTime: '2026-03-08 11:20:00',
        status: 'rejected',
        statusText: '已拒绝',
        shipStatus: 'not_shipped',
        shipStatusText: '未寄出',
        rejectReason: '库存不足',
        products: [
          {
            id: 6,
            image: 'https://picsum.photos/140/140?random=6',
            name: '洁柔纸巾抽纸整箱家用实惠装',
            price: '28.9',
            commission: '8%'
          }
        ]
      }
    ];
  },

  // 筛选列表
  filterList(list, filter) {
    if (filter === 'all') {
      return list;
    }
    if (filter === 'shipped') {
      // 已寄出包括 shipped 和 received 状态
      return list.filter(item => item.shipStatus === 'shipped' || item.shipStatus === 'received');
    }
    return list.filter(item => item.status === filter);
  },

  // 切换筛选
  switchFilter(e) {
    const filter = e.currentTarget.dataset.filter;
    this.setData({
      currentFilter: filter
    });
    this.loadSampleList();
  },

  // 跳转到详情页
  goToDetail(e) {
    const applicationId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/sample-detail/sample-detail?id=${applicationId}`
    });
  },

  // 复制快递单号
  copyTrackingNo(e) {
    const trackingNo = e.currentTarget.dataset.no;
    wx.setClipboardData({
      data: trackingNo,
      success: () => {
        wx.showToast({
          title: '单号已复制',
          icon: 'success'
        });
      }
    });
  },

  // 确认收货
  confirmReceive(e) {
    const applicationId = e.currentTarget.dataset.id;
    
    wx.showModal({
      title: '确认收货',
      content: '确认已收到样品吗？',
      success: (res) => {
        if (res.confirm) {
          // 更新状态
          this.updateShipStatus(applicationId, 'received');
        }
      }
    });
  },

  // 更新物流状态
  updateShipStatus(applicationId, status) {
    // 从本地存储获取数据
    let applications = wx.getStorageSync('sampleApplications') || [];
    
    // 更新对应申请的状态
    const index = applications.findIndex(item => item.id === applicationId);
    if (index !== -1) {
      applications[index].shipStatus = status;
      applications[index].shipStatusText = status === 'received' ? '已签收' : '已寄出';
      
      // 保存回本地存储
      wx.setStorageSync('sampleApplications', applications);
      
      // 刷新列表
      this.loadSampleList();
      
      wx.showToast({
        title: '确认收货成功',
        icon: 'success'
      });
    }
  },

  // 去申请样品
  goToApply() {
    wx.switchTab({
      url: '/pages/index/index'
    });
  },

  // 跳转物流查询页面
  goToLogistics(e) {
    const dataset = e.currentTarget.dataset;
    const status = dataset.status;
    
    if (status === 'not_shipped') {
      return;
    }
    
    // 构建物流查询参数
    const logisticsData = {
      company: dataset.company || '未知物流',
      trackingNo: dataset.tracking,
      status: status,
      receiveTime: dataset.time
    };
    
    const url = `/pages/logistics/logistics?data=${encodeURIComponent(JSON.stringify(logisticsData))}`;
    wx.navigateTo({ url });
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.setData({
      page: 1,
      hasMore: true
    });
    this.loadSampleList();
    wx.stopPullDownRefresh();
  },

  // 上拉加载更多
  onReachBottom() {
    if (this.data.hasMore) {
      this.loadMore();
    }
  },

  // 加载更多
  loadMore() {
    // 这里可以实现分页加载逻辑
    console.log('加载更多');
  }
});
