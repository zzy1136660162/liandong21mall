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
      { id: '9', name: '疼痛舒缓', icon: '💆', parentId: 'tibao' },
      { id: '10', name: '鼻部护理', icon: '👃', parentId: 'tibao' },
      { id: '11', name: '眼部护理', icon: '👁', parentId: 'tibao' },
      { id: '12', name: '皮肤护理', icon: '🧴', parentId: 'tibao' },
      { id: '13', name: '女性调理', icon: '🌸', parentId: 'tibao' },
      { id: '26', name: '男性养护', icon: '💪', parentId: 'tibao' },
      { id: '14', name: '小儿护理', icon: '👶', parentId: 'tibao' },
      { id: '16', name: '纤体瘦身', icon: '⚖️', parentId: 'tibao' },
      { id: '17', name: '养发护发', icon: '💇', parentId: 'tibao' },
      { id: '18', name: '泡浴养生', icon: '🛁', parentId: 'tibao' },
      { id: '24', name: '人参滋补', icon: '🌿', parentId: 'gongneng' },
      { id: '19', name: '阿胶膏滋', icon: '🍯', parentId: 'gongneng' },
      { id: '20', name: '草本茶饮', icon: '🍵', parentId: 'gongneng' },
      { id: '21', name: '固体饮料', icon: '🥤', parentId: 'gongneng' },
      { id: '23', name: '压片糖果', icon: '💊', parentId: 'gongneng' },
      { id: '22', name: '营养颗粒', icon: '🧪', parentId: 'gongneng' },
      { id: '25', name: '植物饮品', icon: '🌱', parentId: 'gongneng' },
      { id: '15', name: '配制酒', icon: '🍶', parentId: 'gongneng' }
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