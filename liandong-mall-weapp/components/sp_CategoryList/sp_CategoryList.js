Component({
  properties: {
    currentTab: {
      type: String,
      value: 'tibao'
    },
    selectedCategory: {
      type: String,
      value: ''
    }
  },

  data: {
    allCategories: [
      { id: 'tibao_1', name: '疼痛舒缓', icon: '💆', parentId: 'tibao' },
      { id: 'tibao_2', name: '鼻部护理', icon: '👃', parentId: 'tibao' },
      { id: 'tibao_3', name: '眼部护理', icon: '👁', parentId: 'tibao' },
      { id: 'tibao_4', name: '皮肤护理', icon: '🧴', parentId: 'tibao' },
      { id: 'tibao_5', name: '女性调理', icon: '🌸', parentId: 'tibao' },
      { id: 'tibao_6', name: '男性养护', icon: '💪', parentId: 'tibao' },
      { id: 'tibao_7', name: '小儿护理', icon: '👶', parentId: 'tibao' },
      { id: 'tibao_8', name: '纤体瘦身', icon: '⚖️', parentId: 'tibao' },
      { id: 'tibao_9', name: '养发护发', icon: '💇', parentId: 'tibao' },
      { id: 'tibao_10', name: '泡浴养生', icon: '🛁', parentId: 'tibao' },
      { id: 'gongneng_1', name: '人参滋补', icon: '🌿', parentId: 'gongneng' },
      { id: 'gongneng_2', name: '阿胶膏滋', icon: '🍯', parentId: 'gongneng' },
      { id: 'gongneng_3', name: '草本茶饮', icon: '🍵', parentId: 'gongneng' },
      { id: 'gongneng_4', name: '固体饮料', icon: '🥤', parentId: 'gongneng' },
      { id: 'gongneng_5', name: '压片糖果', icon: '💊', parentId: 'gongneng' },
      { id: 'gongneng_6', name: '营养颗粒', icon: '🧪', parentId: 'gongneng' },
      { id: 'gongneng_7', name: '植物饮品', icon: '🌱', parentId: 'gongneng' },
      { id: 'gongneng_8', name: '配制酒', icon: '🍶', parentId: 'gongneng' }
    ],
    categories: []
  },

  lifetimes: {
    attached() {
      this.updateCategories()
    }
  },

  observers: {
    'currentTab': function() {
      this.updateCategories()
    }
  },

  methods: {
    selectCategory(e) {
      const { id, name } = e.currentTarget.dataset
      wx.navigateTo({
        url: `/pages/categoryList/categoryList?categoryId=${id}&categoryName=${name}`
      })
    },

    updateCategories() {
      const categories = this.data.allCategories.filter(
        item => item.parentId === this.data.currentTab
      )
      this.setData({
        categories: categories
      })
    }
  }
})