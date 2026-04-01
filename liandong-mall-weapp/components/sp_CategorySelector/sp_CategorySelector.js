Component({
  properties: {
    selectedCategory: {
      type: String,
      value: ''
    }
  },

  data: {
    currentTab: 'tibao',
    tabs: [
      { id: 'tibao', name: '体表保健' },
      { id: 'gongneng', name: '功能食品' }
    ],
    allCategories: [
      { id: 'tibao_1', name: '疼痛舒缓', parentId: 'tibao' },
      { id: 'tibao_2', name: '鼻部护理', parentId: 'tibao' },
      { id: 'tibao_3', name: '眼部护理', parentId: 'tibao' },
      { id: 'tibao_4', name: '皮肤护理', parentId: 'tibao' },
      { id: 'tibao_5', name: '女性调理', parentId: 'tibao' },
      { id: 'tibao_6', name: '男性养护', parentId: 'tibao' },
      { id: 'tibao_7', name: '小儿护理', parentId: 'tibao' },
      { id: 'tibao_8', name: '纤体瘦身', parentId: 'tibao' },
      { id: 'tibao_9', name: '养发护发', parentId: 'tibao' },
      { id: 'tibao_10', name: '泡浴养生', parentId: 'tibao' },
      { id: 'gongneng_1', name: '人参滋补', parentId: 'gongneng' },
      { id: 'gongneng_2', name: '阿胶膏滋', parentId: 'gongneng' },
      { id: 'gongneng_3', name: '草本茶饮', parentId: 'gongneng' },
      { id: 'gongneng_4', name: '固体饮料', parentId: 'gongneng' },
      { id: 'gongneng_5', name: '压片糖果', parentId: 'gongneng' },
      { id: 'gongneng_6', name: '营养颗粒', parentId: 'gongneng' },
      { id: 'gongneng_7', name: '植物饮品', parentId: 'gongneng' },
      { id: 'gongneng_8', name: '配制酒', parentId: 'gongneng' }
    ],
    currentCategories: []
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
    switchTab(e) {
      const id = e.currentTarget.dataset.id
      this.setData({
        currentTab: id,
        selectedCategory: ''
      })
      this.triggerEvent('categorychange', { tabId: id, categoryId: '' })
    },

    selectCategory(e) {
      const { id, name } = e.currentTarget.dataset
      this.setData({
        selectedCategory: id
      })
      this.triggerEvent('categorychange', {
        tabId: this.data.currentTab,
        categoryId: id,
        categoryName: name
      })
    },

    updateCategories() {
      const categories = this.data.allCategories.filter(
        item => item.parentId === this.data.currentTab
      )
      this.setData({
        currentCategories: categories
      })
    }
  }
})