const sampleService = require('../../services/sampleService');

Page({
  data: {
    application: {},
    statusDesc: ''
  },

  onLoad(options) {
    const applicationId = options.id;
    if (applicationId) {
      this.loadApplicationDetail(applicationId);
    }
  },

  // 加载申请详情
  async loadApplicationDetail(applicationId) {
    wx.showLoading({ title: '加载中...' });
    try {
      const res = await sampleService.getSampleDetail(applicationId);
      if (res.code === 200) {
        const application = res.data;
        const statusDesc = this.getStatusDesc(application.status, application.shipStatus);
        this.setData({
          application,
          statusDesc
        });
      } else {
        wx.showToast({ title: res.message || '加载失败', icon: 'none' });
      }
    } catch (error) {
      console.error('加载申请详情失败:', error);
      wx.showToast({ title: '加载失败', icon: 'none' });
    } finally {
      wx.hideLoading();
    }
  },

  // 获取模拟详情数据
  getMockDetail(applicationId) {
    return {
      id: applicationId,
      applyTime: '2026-03-14 06:17:00',
      reviewTime: '2026-03-14 08:30:00',
      shipTime: '2026-03-14 10:00:00',
      receiveTime: '2026-03-15 14:30:00',
      status: 'approved',
      statusText: '审核通过',
      shipStatus: 'shipped',
      shipStatusText: '已寄出',
      logisticsCompany: '顺丰速运',
      trackingNo: 'SF1234567890',
      reviewRemark: '审核通过，样品质量优良，适合推广',
      remark: '希望尽快发货，谢谢！',
      recipient: {
        name: '张三',
        phone: '13800138000',
        province: '广东省',
        city: '深圳市',
        district: '南山区',
        address: '科技园南路88号'
      },
      products: [
        {
          id: 1,
          image: 'https://picsum.photos/160/160?random=10',
          name: '立白大师香氛洗衣液持久留香护色护衣天然酵素',
          price: '39.9',
          commission: '20%'
        }
      ],
      trackingList: [
        {
          content: '快件已签收，感谢您使用顺丰速运，期待再次为您服务',
          time: '2026-03-15 14:30:00'
        },
        {
          content: '【深圳市】快件已送达【深圳南山营业点】，正在派送中',
          time: '2026-03-15 08:20:00'
        },
        {
          content: '【深圳市】快件已发车，下一站【深圳南山营业点】',
          time: '2026-03-14 22:15:00'
        },
        {
          content: '【深圳市】顺丰速运 已收取快件',
          time: '2026-03-14 18:30:00'
        }
      ]
    };
  },

  // 获取状态描述
  getStatusDesc(status, shipStatus) {
    if (status === 'pending') {
      return '您的申请正在审核中，请耐心等待';
    } else if (status === 'rejected') {
      return '您的申请未通过审核，请查看审核备注';
    } else if (status === 'approved') {
      if (shipStatus === 'not_shipped') {
        return '您的申请已通过审核，样品准备中';
      } else if (shipStatus === 'shipped') {
        return '样品已寄出，请注意查收';
      } else if (shipStatus === 'received') {
        return '样品已签收，请尽快完成测评';
      }
    }
    return '';
  },

  // 复制快递单号
  copyTrackingNo() {
    const trackingNo = this.data.application.trackingNo;
    if (!trackingNo) return;
    
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
  confirmReceive() {
    wx.showModal({
      title: '确认收货',
      content: '确认已收到样品吗？确认后将开始计算测评期限',
      confirmText: '确认收货',
      cancelText: '取消',
      success: (res) => {
        if (res.confirm) {
          this.doConfirmReceive();
        }
      }
    });
  },

  // 执行确认收货
  doConfirmReceive() {
    const applicationId = this.data.application.id;
    
    // 从本地存储获取数据
    let applications = wx.getStorageSync('sampleApplications') || [];
    
    // 更新对应申请的状态
    const index = applications.findIndex(item => item.id === applicationId);
    if (index !== -1) {
      applications[index].shipStatus = 'received';
      applications[index].shipStatusText = '已签收';
      
      // 保存回本地存储
      wx.setStorageSync('sampleApplications', applications);
      
      // 刷新页面数据
      this.loadApplicationDetail(applicationId);
      
      wx.showToast({
        title: '确认收货成功',
        icon: 'success'
      });
    }
  },

  // 联系客服
  contactService() {
    wx.showModal({
      title: '联系客服',
      content: '客服电话: 400-123-4567',
      confirmText: '拨打',
      success: (res) => {
        if (res.confirm) {
          wx.makePhoneCall({
            phoneNumber: '4001234567'
          });
        }
      }
    });
  }
});
