Page({
  data: {
    projects: [],
    loading: false,
    noMore: false,
    page: 1,
    pageSize: 10
  },

  onLoad(options) {
    this.loadProjects()
  },

  async loadProjects() {
    if (this.data.loading || this.data.noMore) return

    this.setData({ loading: true })

    try {
      const mockProjects = this.getMockProjects()
      
      if (mockProjects.length === 0) {
        this.setData({ noMore: true })
      } else {
        const newProjects = [...this.data.projects, ...mockProjects]
        this.setData({
          projects: newProjects,
          page: this.data.page + 1
        })
      }
    } catch (error) {
      console.error('加载项目失败:', error)
    } finally {
      this.setData({ loading: false })
    }
  },

  getMockProjects() {
    const projects = []
    const categories = ['新材料', '工艺优化', '产品研发', '技术创新']
    const statuses = ['active', 'completed', 'pending']
    const statusTexts = { active: '进行中', completed: '已完成', pending: '待开始' }
    const icons = ['🔬', '⚡', '🧪', '🔧', '💡', '🎯', '📊', '🔭']

    for (let i = 0; i < 5; i++) {
      const status = statuses[Math.floor(Math.random() * statuses.length)]
      const progress = status === 'completed' ? 100 : Math.floor(Math.random() * 90) + 10
      
      projects.push({
        id: Date.now() + i,
        name: `研发项目 ${this.data.projects.length + i + 1}`,
        category: categories[Math.floor(Math.random() * categories.length)],
        description: '这是一个重要的研发项目，旨在提升产品质量和技术创新能力，为公司发展提供强有力的技术支撑。',
        progress: progress,
        statusClass: status,
        statusText: statusTexts[status],
        icon: icons[Math.floor(Math.random() * icons.length)],
        leader: '研发团队',
        deadline: '2026-06-30'
      })
    }
    return projects
  },

  goToProjectDetail(e) {
    const projectId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/project-detail/project-detail?id=${projectId}`,
      fail: () => {
        wx.showToast({
          title: '页面跳转失败',
          icon: 'none'
        })
      }
    })
  },

  viewProject(e) {
    const projectId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/project-detail/project-detail?id=${projectId}`,
      fail: () => {
        wx.showToast({
          title: '页面跳转失败',
          icon: 'none'
        })
      }
    })
  },

  viewAllProjects() {
    wx.showToast({
      title: '查看全部项目',
      icon: 'none'
    })
  },

  onReachBottom() {
    if (!this.data.noMore && !this.data.loading) {
      this.loadProjects()
    }
  },

  onTabChange(e) {
    const { activeTab } = e.detail
    const tabPaths = [
      '/pages/index/index',
      '/pages/Product_list_page/Product_list_page',
      '/pages/selection/selection',
      '/pages/rd/rd',
      '/pages/Profile_page/Profile_page'
    ]

    if (activeTab !== 3) {
      wx.switchTab({
        url: tabPaths[activeTab]
      })
    }
  }
})
