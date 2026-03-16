const categoryData = require('../../utils/category-data.js');

Page({
  data: {
    currentMainCategory: 'food',
    subCategories: [],
    filterTags: [
      { id: 'kuaishou', name: '快手优选' },
      { id: 'hot', name: '爆品计划' },
      { id: 'nationwide', name: '全国可售' },
      { id: 'sample-back', name: '买样后返' }
    ],
    currentFilter: 'kuaishou',
    products: []
  },

  onLoad(options) {
    // 获取系统状态栏高度和胶囊按钮位置
    const systemInfo = wx.getSystemInfoSync();
    const menuButtonInfo = wx.getMenuButtonBoundingClientRect();
    const statusBarHeight = systemInfo.statusBarHeight || 20;
    const navBarHeight = (menuButtonInfo.top - statusBarHeight) * 2 + menuButtonInfo.height * 2;
    
    const category = options.category || 'food';
    this.setData({
      currentMainCategory: category,
      statusBarHeight: (statusBarHeight + navBarHeight / 2) * 2 // 状态栏+导航栏高度
    });
    this.loadSubCategories(category);
    this.loadProducts(category);
  },

  // 加载二级分类
  loadSubCategories(categoryId) {
    const category = categoryData.categories.find(c => c.id === categoryId);
    if (category && category.subCategories) {
      this.setData({
        subCategories: category.subCategories
      });
    }
  },

  // 加载商品数据
  loadProducts(categoryId) {
    // 模拟商品数据
    const products = this.generateProducts(categoryId);
    this.setData({ products });
  },

  // 生成模拟商品数据
  generateProducts(categoryId) {
    const productTemplates = {
      food: [
        { title: '李海龙麻辣烫正宗东北老式黏糊麻辣烫', price: '39.8', commission: '6.77', rate: '17%', sales: '月销3911件', image: 'https://picsum.photos/400/400?random=1' },
        { title: '【拍1发4包】麻辣牛板筋自拌延边特产', price: '8.98', commission: '1.98', rate: '22%', sales: '月销1.3万件', image: 'https://picsum.photos/400/400?random=2' },
        { title: '今麦郎大今野1.5倍红烧牛肉面', price: '33', commission: '1.1', rate: '3%', sales: '月销5.2万件', image: 'https://picsum.photos/400/400?random=3' },
        { title: '五得利八星雪花小麦粉5kg', price: '39.9', commission: '1.8', rate: '4%', sales: '月销4.3万件', image: 'https://picsum.photos/400/400?random=4' }
      ],
      home: [
        { title: '南极人A类抗菌大豆被加厚保暖冬被', price: '82', commission: '8.2', rate: '10%', sales: '304人已上架', image: 'https://picsum.photos/400/400?random=5' },
        { title: '新店【每人一单】手提加厚垃圾袋', price: '2.98', commission: '0.51', rate: '17%', sales: '19人已上架', image: 'https://picsum.photos/400/400?random=6' },
        { title: '超能洗衣液整箱批发持久留香', price: '49.9', commission: '5.99', rate: '12%', sales: '月销2.1万件', image: 'https://picsum.photos/400/400?random=7' },
        { title: '厨房置物架多层收纳架', price: '29.9', commission: '3.59', rate: '12%', sales: '月销8563件', image: 'https://picsum.photos/400/400?random=8' }
      ],
      clothing: [
        { title: '春季爆款高腰显瘦阔腿裤', price: '98', commission: '12.74', rate: '13%', sales: '月销2088件', image: 'https://picsum.photos/400/400?random=9' },
        { title: '白色荷叶边吊带连衣裙女', price: '169.9', commission: '35.68', rate: '21%', sales: '3568人已上架', image: 'https://picsum.photos/400/400?random=10' },
        { title: '法式复古方领泡泡袖上衣', price: '79', commission: '9.48', rate: '12%', sales: '月销4521件', image: 'https://picsum.photos/400/400?random=11' },
        { title: '韩版宽松休闲西装外套', price: '128', commission: '15.36', rate: '12%', sales: '月销3215件', image: 'https://picsum.photos/400/400?random=12' }
      ],
      beauty: [
        { title: '花间颂粉饼控油定妆持久遮瑕', price: '49.9', commission: '13.97', rate: '28%', sales: '6.4万人已上架', image: 'https://picsum.photos/400/400?random=13' },
        { title: '婉嫔新中式自然纤长款假睫毛', price: '9.9', commission: '2.97', rate: '30%', sales: '2287人已上架', image: 'https://picsum.photos/400/400?random=14' },
        { title: '完美日记动物眼影盘十二色', price: '99', commission: '19.8', rate: '20%', sales: '月销1.2万件', image: 'https://picsum.photos/400/400?random=15' },
        { title: '花西子散粉定妆控油持久', price: '149', commission: '32.78', rate: '22%', sales: '月销2.3万件', image: 'https://picsum.photos/400/400?random=16' }
      ],
      personal: [
        { title: '春蔻氨基酸洗发水控油蓬松去屑', price: '39.9', commission: '7.98', rate: '20%', sales: '月销3.6万件', image: 'https://picsum.photos/400/400?random=17' },
        { title: '小竹牙线棒超细家庭装300支', price: '9.9', commission: '3.76', rate: '38%', sales: '月销3621件', image: 'https://picsum.photos/400/400?random=18' },
        { title: '可立克蜂毒牙膏去黄去口臭', price: '29.9', commission: '5.98', rate: '20%', sales: '月销1.2万件', image: 'https://picsum.photos/400/400?random=19' },
        { title: '叶黄素蒸汽眼罩缓解眼疲劳', price: '19.9', commission: '3.98', rate: '20%', sales: '月销8563件', image: 'https://picsum.photos/400/400?random=20' }
      ],
      health: [
        { title: 'Kingscom益生菌冻干粉', price: '159', commission: '15.9', rate: '10%', sales: '月销1.2万件', image: 'https://picsum.photos/400/400?random=21' },
        { title: 'PANDORA BABY进口活性菌株', price: '69.9', commission: '24.46', rate: '35%', sales: '月销1890件', image: 'https://picsum.photos/400/400?random=22' },
        { title: '益驰胶原蛋白肽口服液', price: '199', commission: '19.9', rate: '10%', sales: '月销4521件', image: 'https://picsum.photos/400/400?random=23' },
        { title: 'vitafusion女士复合维生素', price: '89', commission: '26.7', rate: '30%', sales: '月销3215件', image: 'https://picsum.photos/400/400?random=24' }
      ],
      baby: [
        { title: '【宝宝面霜】滋润倍护有机沙棘', price: '69', commission: '6.9', rate: '10%', sales: '月销3542件', image: 'https://picsum.photos/400/400?random=25' },
        { title: '【可心柔】婴儿柔纸巾110抽12包', price: '47.9', commission: '4.79', rate: '10%', sales: '1848人已上架', image: 'https://picsum.photos/400/400?random=26' },
        { title: '贝亲婴儿奶瓶PPSU宽口径', price: '89', commission: '8.9', rate: '10%', sales: '月销1.8万件', image: 'https://picsum.photos/400/400?random=27' },
        { title: ' babycare纸尿裤超薄透气', price: '99', commission: '14.85', rate: '15%', sales: '月销2.3万件', image: 'https://picsum.photos/400/400?random=28' }
      ],
      fresh: [
        { title: '脱骨侠蒜香无骨鸡爪1000g', price: '29.9', commission: '5.38', rate: '18%', sales: '月销2.2万件', image: 'https://picsum.photos/400/400?random=29' },
        { title: '【选购到手80根】火山石烤肠', price: '39.99', commission: '10.4', rate: '26%', sales: '3.9万人已上架', image: 'https://picsum.photos/400/400?random=30' },
        { title: '正宗潮汕牛肉丸手打牛筋丸', price: '59.9', commission: '8.98', rate: '15%', sales: '月销1.5万件', image: 'https://picsum.photos/400/400?random=31' },
        { title: '大连特产海带结干货', price: '19.9', commission: '3.98', rate: '20%', sales: '月销9563件', image: 'https://picsum.photos/400/400?random=32' }
      ],
      men: [
        { title: '美式工装外套男生潮流春秋季', price: '79', commission: '15.01', rate: '19%', sales: '月销655件', image: 'https://picsum.photos/400/400?random=33' },
        { title: 'jeep吉普夹克男士春秋季', price: '99', commission: '31.68', rate: '32%', sales: '月销1966件', image: 'https://picsum.photos/400/400?random=34' },
        { title: '七匹狼男士休闲裤直筒宽松', price: '129', commission: '19.35', rate: '15%', sales: '月销4521件', image: 'https://picsum.photos/400/400?random=35' },
        { title: '海澜之家男士polo衫短袖', price: '89', commission: '13.35', rate: '15%', sales: '月销3215件', image: 'https://picsum.photos/400/400?random=36' }
      ],
      sports: [
        { title: '【100%新疆棉】优质运动袜5双装', price: '9.9', commission: '3.17', rate: '32%', sales: '1.2万人已上架', image: 'https://picsum.photos/400/400?random=37' },
        { title: '健身拉力绳弹力绳训练器材', price: '29.9', commission: '12.56', rate: '42%', sales: '月销1520件', image: 'https://picsum.photos/400/400?random=38' },
        { title: '拉筋小腿按摩器瑜伽辅助器', price: '39.9', commission: '5.99', rate: '15%', sales: '月销8563件', image: 'https://picsum.photos/400/400?random=39' },
        { title: '户外折叠椅便携式露营椅子', price: '49.9', commission: '7.48', rate: '15%', sales: '月销4521件', image: 'https://picsum.photos/400/400?random=40' }
      ],
      digital: [
        { title: '【新款】家用手机支架可折叠升降', price: '9.9', commission: '4.95', rate: '50%', sales: '月销1737件', image: 'https://picsum.photos/400/400?random=41' },
        { title: 'hellokitty暖宫腰带女生大姨妈神器', price: '78', commission: '17.16', rate: '22%', sales: '月销672件', image: 'https://picsum.photos/400/400?random=42' },
        { title: '120W超级快充充电宝20000毫安', price: '59.9', commission: '11.98', rate: '20%', sales: '月销3215件', image: 'https://picsum.photos/400/400?random=43' },
        { title: '复古手机包斜挎包女2024新款', price: '29.9', commission: '5.98', rate: '20%', sales: '月销1890件', image: 'https://picsum.photos/400/400?random=44' }
      ],
      luxury: [
        { title: '【秋冬必备】复古豹纹毛绒发箍', price: '3.88', commission: '0.78', rate: '20%', sales: '月销3.9万件', image: 'https://picsum.photos/400/400?random=45' },
        { title: '非金属仿玉石手镯女款', price: '59.9', commission: '20.96', rate: '35%', sales: '975人已上架', image: 'https://picsum.photos/400/400?random=46' },
        { title: 'FANCI范琦925银项链女款', price: '199', commission: '39.8', rate: '20%', sales: '月销1520件', image: 'https://picsum.photos/400/400?random=47' },
        { title: '满天星戒指女925银时尚指环', price: '89', commission: '26.7', rate: '30%', sales: '月销3215件', image: 'https://picsum.photos/400/400?random=48' }
      ],
      tea: [
        { title: '【AAAAA】正品台湾冻顶乌龙茶', price: '39.8', commission: '12.34', rate: '31%', sales: '月销335件', image: 'https://picsum.photos/400/400?random=49' },
        { title: 'LeTea乐茶组合装4袋送冰变杯', price: '29.9', commission: '2.99', rate: '10%', sales: '7850人已上架', image: 'https://picsum.photos/400/400?random=50' },
        { title: '玉米须茶养生茶包独立包装', price: '19.9', commission: '3.98', rate: '20%', sales: '月销4521件', image: 'https://picsum.photos/400/400?random=51' },
        { title: '温县原产地道怀菊花养生茶', price: '29.9', commission: '5.98', rate: '20%', sales: '月销1890件', image: 'https://picsum.photos/400/400?random=52' }
      ]
    };

    const templates = productTemplates[categoryId] || productTemplates.food;
    return templates.map((item, index) => ({
      id: categoryId + '_' + index,
      ...item,
      cashback: index % 2 === 0,
      trust: index % 3 === 0,
      isBrand: index % 2 === 1,
      rankTag: index < 2 ? ['入选麻辣烫/麻辣拌爆款榜', '入选素鸡/素肉爆款榜'][index] : null
    }));
  },

  // 切换主分类
  switchMainCategory(e) {
    const category = e.currentTarget.dataset.category;
    if (category === 'home') {
      wx.switchTab({
        url: '/pages/index/index'
      });
      return;
    }
    this.setData({
      currentMainCategory: category
    });
    this.loadSubCategories(category);
    this.loadProducts(category);
  },

  // 选择二级分类
  selectSubCategory(e) {
    const item = e.currentTarget.dataset.item;
    wx.showToast({
      title: '选择: ' + item.name,
      icon: 'none'
    });
  },

  // 切换筛选
  switchFilter(e) {
    const filter = e.currentTarget.dataset.filter;
    this.setData({
      currentFilter: filter
    });
  },

  // 显示筛选面板
  showFilterPanel() {
    wx.showToast({
      title: '筛选功能开发中',
      icon: 'none'
    });
  },

  // 显示更多分类
  showMoreCategories() {
    wx.showActionSheet({
      itemList: ['春焕新', '零食饮料', '家居百货', '女装女鞋', '美妆护肤', '个护清洁', '医疗保健', '母婴玩具', '生鲜食品', '男装男鞋', '运动户外', '数码家电', '珠宝奢品', '茶叶酒水'],
      success: (res) => {
        const categories = ['spring', 'food', 'home', 'clothing', 'beauty', 'personal', 'health', 'baby', 'fresh', 'men', 'sports', 'digital', 'luxury', 'tea'];
        this.switchMainCategory({ currentTarget: { dataset: { category: categories[res.tapIndex] } } });
      }
    });
  },

  // 返回
  goBack() {
    wx.navigateBack();
  },

  // 去搜索
  goToSearch() {
    wx.navigateTo({
      url: '/pages/index/index'
    });
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
