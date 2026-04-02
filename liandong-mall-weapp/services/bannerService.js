const { productApi } = require('../utils/sp_api.js')

class BannerService {
  constructor() {
    this.cache = new Map()
    this.cacheTimeout = 5 * 60 * 1000
    this.defaultBanner = {
      id: 0,
      image: 'https://picsum.photos/750/400?random=default',
      title: '默认轮播图',
      subtitle: ''
    }
  }

  isCacheValid(key) {
    const cached = this.cache.get(key)
    if (!cached) return false
    return Date.now() - cached.timestamp < this.cacheTimeout
  }

  setCache(key, data) {
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    })
  }

  getFromCache(key) {
    const cached = this.cache.get(key)
    if (cached && this.isCacheValid(key)) {
      return cached.data
    }
    return null
  }

  clearCache(key = null) {
    if (key) {
      this.cache.delete(key)
    } else {
      this.cache.clear()
    }
  }

  validateBannerData(banner) {
    if (!banner || typeof banner !== 'object') {
      return false
    }
    if (!banner.imageUrl && !banner.image) {
      return false
    }
    return true
  }

  formatBanner(banner, index = 0) {
    if (!this.validateBannerData(banner)) {
      console.warn('无效的轮播图数据:', banner)
      return null
    }

    return {
      id: banner.id || index,
      image: banner.imageUrl || banner.image,
      title: banner.title || '',
      subtitle: banner.subtitle || '',
      linkType: banner.linkType || 'none',
      linkValue: banner.linkValue || '',
      sort: banner.sort || index,
      position: banner.position || 'mall',
      isLoaded: false,
      loadFailed: false
    }
  }

  formatBanners(banners) {
    if (!Array.isArray(banners)) {
      console.warn('轮播图数据不是数组格式')
      return []
    }

    const validBanners = banners
      .map((banner, index) => this.formatBanner(banner, index))
      .filter(banner => banner !== null)

    return validBanners
  }

  async getBanners(position = null, useCache = true) {
    const cacheKey = `banners_${position || 'all'}`

    if (useCache) {
      const cached = this.getFromCache(cacheKey)
      if (cached) {
        console.log('从缓存获取轮播图:', cacheKey)
        return cached
      }
    }

    try {
      let banners
      if (position === 'home') {
        banners = await productApi.getHomeBanners()
      } else if (position === 'mall') {
        banners = await productApi.getMallBanners()
      } else {
        banners = await productApi.getBanners()
      }

      const formattedBanners = this.formatBanners(banners)

      this.setCache(cacheKey, formattedBanners)

      return formattedBanners
    } catch (error) {
      console.error('获取轮播图失败:', error)
      throw error
    }
  }

  async getMallBanners(useCache = true) {
    return this.getBanners('mall', useCache)
  }

  async getHomeBanners(useCache = true) {
    return this.getBanners('home', useCache)
  }

  handleBannerClick(banner, app) {
    if (!banner) {
      console.warn('轮播图数据为空')
      return
    }

    const { linkType, linkValue, id, title } = banner

    console.log('点击轮播图:', { id, title, linkType, linkValue })

    switch (linkType) {
      case 'product':
        if (linkValue) {
          this.navigateToProduct(linkValue)
        }
        break

      case 'category':
        if (linkValue) {
          this.navigateToCategory(linkValue)
        }
        break

      case 'url':
        if (linkValue) {
          this.navigateToWebview(linkValue)
        }
        break

      case 'none':
      default:
        console.log('轮播图无链接配置')
        wx.showToast({
          title: title || '轮播图',
          icon: 'none',
          duration: 1500
        })
        break
    }
  }

  navigateToProduct(productId) {
    if (!productId) {
      console.warn('商品ID为空')
      return
    }

    wx.navigateTo({
      url: `/pages/sp_Details/sp_Details?id=${productId}`,
      fail: (err) => {
        console.error('跳转到商品详情页失败:', err)
        wx.showToast({
          title: '页面跳转失败',
          icon: 'none',
          duration: 2000
        })
      }
    })
  }

  navigateToCategory(categoryId) {
    if (!categoryId) {
      console.warn('分类ID为空')
      return
    }

    wx.navigateTo({
      url: `/pages/sp_Product_list/sp_Product_list?categoryId=${categoryId}`,
      fail: (err) => {
        console.error('跳转到分类商品页失败:', err)
        wx.showToast({
          title: '页面跳转失败',
          icon: 'none',
          duration: 2000
        })
      }
    })
  }

  navigateToWebview(url) {
    if (!url) {
      console.warn('URL为空')
      return
    }

    wx.navigateTo({
      url: `/pages/webview/webview?url=${encodeURIComponent(url)}`,
      fail: (err) => {
        console.error('打开网页视图失败:', err)
        wx.showToast({
          title: '无法打开链接',
          icon: 'none',
          duration: 2000
        })
      }
    })
  }

  preloadImage(imageUrl) {
    return new Promise((resolve, reject) => {
      if (!imageUrl) {
        resolve(false)
        return
      }

      wx.getImageInfo({
        src: imageUrl,
        success: () => {
          console.log('图片预加载成功:', imageUrl)
          resolve(true)
        },
        fail: (err) => {
          console.warn('图片预加载失败:', imageUrl, err)
          resolve(false)
        }
      })
    })
  }

  async preloadImages(banners) {
    if (!Array.isArray(banners) || banners.length === 0) {
      return
    }

    const preloadPromises = banners.slice(0, 3).map(banner =>
      this.preloadImage(banner.image)
    )

    await Promise.all(preloadPromises)
    console.log('轮播图预加载完成')
  }

  getDefaultBanners() {
    return [
      {
        id: 1,
        image: 'https://picsum.photos/750/400?random=1',
        title: '新人专享优惠',
        subtitle: '首单立减20元',
        linkType: 'none',
        linkValue: ''
      },
      {
        id: 2,
        image: 'https://picsum.photos/750/400?random=2',
        title: '热门推荐',
        subtitle: '精选好物等你来',
        linkType: 'none',
        linkValue: ''
      },
      {
        id: 3,
        image: 'https://picsum.photos/750/400?random=3',
        title: '限时秒杀',
        subtitle: '每天10点准时开抢',
        linkType: 'none',
        linkValue: ''
      }
    ]
  }
}

const bannerService = new BannerService()

module.exports = bannerService
