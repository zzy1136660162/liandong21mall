Page({
  data: {
    currentTab: 'tibao',
    banners: [
      {
        id: 1,
        image: 'https://picsum.photos/750/300?random=1',
        title: '新人专享优惠',
        subtitle: '首单立减20元'
      },
      {
        id: 2,
        image: 'https://picsum.photos/750/300?random=2',
        title: '热门推荐',
        subtitle: '精选好物等你来'
      },
      {
        id: 3,
        image: 'https://picsum.photos/750/300?random=3',
        title: '限时秒杀',
        subtitle: '每天10点准时开抢'
      }
    ]
  },

  onTabChange(e) {
    const { tabId } = e.detail
    this.setData({
      currentTab: tabId
    })
    console.log('Tab切换:', tabId)
  },

  onCategoryChange(e) {
    const { tabId, categoryId, categoryName } = e.detail
    console.log('分类切换:', tabId, categoryId, categoryName)
  }
})