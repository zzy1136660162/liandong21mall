const app = getApp();

Component({
  properties: {
    title: {
      type: String,
      value: '研发人才库'
    },
    showMore: {
      type: Boolean,
      value: true
    },
    limit: {
      type: Number,
      value: 3
    }
  },

  data: {
    talents: [],
    loading: true,
    error: null
  },

  lifetimes: {
    attached() {
      this.loadTalents()
    }
  },

  pageLifetimes: {
    show() {
      if (!this.data.talents.length) {
        this.loadTalents()
      }
    }
  },

  methods: {
    async loadTalents() {
      this.setData({ loading: true, error: null })

      try {
        const res = await new Promise((resolve, reject) => {
          app.request({
            url: `/api/talent_pool/list?page=1&pageSize=${this.data.limit}`,
            success: (res) => {
              console.log('人才API响应:', res)
              resolve(res)
            },
            fail: (err) => reject(err)
          })
        })

        console.log('人才数据:', res)
        
        let talents = []
        if (res && res.data && res.data.list) {
          talents = res.data.list
        } else if (res && res.list) {
          talents = res.list
        }

        this.setData({
          talents: talents,
          loading: false
        })
      } catch (error) {
        console.error('加载人才信息失败:', error)
        this.setData({
          error: '加载失败',
          loading: false
        })
      }
    },

    goToTalentDetail(e) {
      const { id } = e.currentTarget.dataset
      wx.navigateTo({
        url: `/pages/talent_pool/detail/detail?id=${id}`
      })
    },

    goToTalentList() {
      wx.navigateTo({
        url: '/pages/talent_pool/index/index'
      })
    },

    refresh() {
      this.loadTalents()
    }
  }
})
