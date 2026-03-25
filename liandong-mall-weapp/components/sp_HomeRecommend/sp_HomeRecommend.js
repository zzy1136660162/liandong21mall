// 首页商品推荐组件
const { productApi } = require('../../utils/sp_api.js')

Component({
  properties: {
    title: {
      type: String,
      value: '热门推荐'
    },
    showMore: {
      type: Boolean,
      value: true
    },
    productType: {
      type: String,
      value: 'recommend' // recommend: 推荐, hot: 热销, new: 新品
    },
    limit: {
      type: Number,
      value: 6
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
        let products = []
        
        switch (this.data.productType) {
          case 'hot':
            products = await productApi.getHotProducts(this.data.limit)
            break
          case 'new':
            products = await productApi.getNewProducts(this.data.limit)
            break
          case 'recommend':
          default:
            products = await productApi.getRecommendProducts(this.data.limit)
            break
        }
        
        this.setData({
          products: products || [],
          loading: false
        })
      } catch (error) {
        console.error('加载推荐商品失败:', error)
        this.setData({
          error: '加载失败',
          loading: false
        })
      }
    },

    goToProduct(e) {
      const { id } = e.currentTarget.dataset
      wx.navigateTo({
        url: `/pages/sp_Details/sp_Details?id=${id}`
      })
    },

    goToProductList() {
      const urlMap = {
        recommend: '/pages/Product_list_page/Product_list_page?type=recommend',
        hot: '/pages/Product_list_page/Product_list_page?type=hot',
        new: '/pages/Product_list_page/Product_list_page?type=new'
      }
      wx.navigateTo({
        url: urlMap[this.data.productType] || '/pages/Product_list_page/Product_list_page'
      })
    },

    refresh() {
      this.loadProducts()
    }
  }
})
