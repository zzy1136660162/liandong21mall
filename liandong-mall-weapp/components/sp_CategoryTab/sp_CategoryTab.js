Component({
  properties: {
    currentTab: {
      type: String,
      value: 'tibao'
    }
  },

  data: {
    tabs: [
      { id: 'tibao', name: '体表保健' },
      { id: 'gongneng', name: '功能食品' }
    ]
  },

  methods: {
    switchTab(e) {
      const id = e.currentTarget.dataset.id
      if (id !== this.data.currentTab) {
        this.triggerEvent('tabchange', { tabId: id })
      }
    }
  }
})