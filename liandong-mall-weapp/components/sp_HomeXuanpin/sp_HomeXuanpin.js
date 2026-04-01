const productService = require('../../services/productService')

Component({
  properties: {
    title: {
      type: String,
      value: '选品推荐'
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
    products: [],
    loading: true,
    error: null
  },

  lifetimes: {
    attached() {
      this.loadProducts()
    }
  },

  pageLifetimes: {
    show() {
      if (!this.data.products.length) {
        this.loadProducts()
      }
    }
  },

  methods: {
    async loadProducts() {
      this.setData({ loading: true, error: null })

      try {
        const res = await productService.getProducts({
          page: 1,
          pageSize: this.data.limit
        })

        const list = res.list || []
        const products = list.map(item => ({
          id: item.id,
          image: item.image,
          title: item.name || item.title,
          price: typeof item.price === 'number' ? item.price.toString() : item.price,
          originalPrice: item.originalPrice ? item.originalPrice.toString() : '',
          commissionRate: item.commissionRate || 0,
          commissionAmount: item.commissionAmount,
          tags: item.tags || []
        }))

        this.setData({
          products: products || [],
          loading: false
        })
      } catch (error) {
        console.error('加载选品商品失败:', error)
        this.setData({
          error: '加载失败',
          loading: false
        })
      }
    },

    goToProduct(e) {
      const { id } = e.currentTarget.dataset
      wx.navigateTo({
        url: `/pages/product-detail/product-detail?id=${id}`
      })
    },

    goToXuanpin() {
      wx.switchTab({
        url: '/pages/xuanpinindex/xuanpinindex'
      })
    },

    refresh() {
      this.loadProducts()
    }
  }
})