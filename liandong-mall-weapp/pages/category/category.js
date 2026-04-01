const productService = require('../../services/productService.js');
const categoryData = require('../../utils/category-data.js');

const categoryNameMap = {
  'nasal_care': '鼻部护理',
  'pain_relief': '缓解疼痛',
  'eye_care': '护眼',
  'sub_health': '调理亚健康',
  'kidney_care': '固肾养肾',
  'body_odor': '狐臭护理',
  'skin_care': '美肤护肤',
  'facial_rehab': '面瘫康复',
  'women_health': '女性调理',
  'solid_drink': '固体饮料',
  'tablet_candy': '压片糖果',
  'herbal_paste': '膏滋',
  'herbal_drink': '植物饮品',
  'prepared_wine': '配制酒',
  'tea_substitute': '代用茶'
};

Page({
  data: {
    currentMainCategory: 'all',
    products: [],
    page: 1,
    pageSize: 20,
    loading: false,
    hasMore: true
  },

  onLoad(options) {
    // 获取系统状态栏高度和胶囊按钮位置
    const systemInfo = wx.getSystemInfoSync();
    const menuButtonInfo = wx.getMenuButtonBoundingClientRect();
    const statusBarHeight = systemInfo.statusBarHeight || 20;
    const navBarHeight = (menuButtonInfo.top - statusBarHeight) * 2 + menuButtonInfo.height * 2;
    
    const category = options.category || 'all';
    this.setData({
      currentMainCategory: category,
      statusBarHeight: (statusBarHeight + navBarHeight / 2) * 2
    });
    this.loadProducts(category);
  },

  // 加载商品数据
  async loadProducts(categoryId) {
    if (this.data.loading) return;
    
    this.setData({ loading: true, products: [] });
    wx.showLoading({ title: '加载中...' });
    
    try {
      let params = {
        page: 1,
        pageSize: this.data.pageSize
      };
      
      // 根据分类ID查询
      if (categoryId && categoryId !== 'all') {
        // 将分类ID转换为分类名称
        const categoryName = categoryNameMap[categoryId] || categoryId;
        params.category = categoryName;
      }
      
      const res = await productService.getProducts(params);
      wx.hideLoading();
      
      let products = [];
      if (res && res.list) {
        products = res.list.map(item => ({
          id: item.id,
          title: item.name,
          price: item.price,
          commissionAmount: item.commission_amount || item.commission || '0',
          commissionRate: item.commission_rate || '0',
          salesText: item.sales || '0',
          image: item.main_image || item.image
        }));
      }
      
      this.setData({ 
        products: products,
        loading: false,
        hasMore: products.length >= this.data.pageSize
      });
    } catch (err) {
      wx.hideLoading();
      console.error('加载商品失败:', err);
      this.setData({ loading: false });
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    }
  },

  // 切换主分类
  switchMainCategory(e) {
    const category = e.currentTarget.dataset.category;
    this.setData({
      currentMainCategory: category
    });
    this.loadProducts(category);
  },

  // 显示更多分类
  showMoreCategories() {
    wx.showActionSheet({
      itemList: ['鼻部护理', '缓解疼痛', '护眼', '调理亚健康', '固肾养肾', '狐臭护理', '美肤护肤', '面瘫康复', '女性调理', '固体饮料', '压片糖果', '膏滋', '植物饮品', '配制酒', '代用茶'],
      success: (res) => {
        const categories = ['nasal_care', 'pain_relief', 'eye_care', 'sub_health', 'kidney_care', 'body_odor', 'skin_care', 'facial_rehab', 'women_health', 'solid_drink', 'tablet_candy', 'herbal_paste', 'herbal_drink', 'prepared_wine', 'tea_substitute'];
        this.switchMainCategory({ currentTarget: { dataset: { category: categories[res.tapIndex] } } });
      }
    });
  },

  // 返回
  goBack() {
    wx.navigateBack();
  },

  // 返回首页
  goToHome() {
    wx.switchTab({
      url: '/pages/xuanpinindex/xuanpinindex'
    });
  },

  // 跳转到商品详情
  goToProductDetail(e) {
    const productId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: '/pages/product-detail/product-detail?id=' + productId
    });
  },

  // 去搜索
  goToSearch() {
    wx.navigateTo({
      url: '/pages/search/search'
    });
  },

  // 拍照搜索和扫码
  onCameraTap() {
    wx.showActionSheet({
      itemList: ['拍照搜索', '扫码识别'],
      success: (res) => {
        if (res.tapIndex === 0) {
          this.takePhoto();
        } else if (res.tapIndex === 1) {
          this.scanCode();
        }
      }
    });
  },

  // 拍照搜索
  takePhoto() {
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

  processImage(imagePath) {
    wx.showLoading({ title: '识别中...' });
    setTimeout(() => {
      wx.hideLoading();
      wx.showToast({
        title: '图片已选择',
        icon: 'none'
      });
    }, 1000);
  },

  processScanResult(result) {
    wx.showLoading({ title: '识别中...' });
    setTimeout(() => {
      wx.hideLoading();
      wx.showToast({
        title: '扫码成功',
        icon: 'none'
      });
    }, 1000);
  },

  // 切换Tab
  switchTab(e) {
    const page = e.currentTarget.dataset.page;
    const urls = {
      index: '/pages/index/index',
      shelf: '/pages/my/my',
      data: '/pages/rank/rank',
      my: '/pages/my/my'
    };
    if (page !== 'index') {
      wx.switchTab({
        url: urls[page]
      });
    }
  },

  // 加入货架
  addToShelf(e) {
    const productId = e.currentTarget.dataset.id;
    wx.showToast({
      title: '已加入货架',
      icon: 'success'
    });
  }
});
