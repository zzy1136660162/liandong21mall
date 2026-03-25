const addressApi = require('../../utils/sp_api.js').addressApi
const { checkLogin, getLoginStatus } = require('../../utils/sp_auth.js')

Page({
  data: {
    addressList: [],
    useMockData: false,
    fromOrder: false,
    isLoggedIn: false
  },

  onLoad(options) {
    const loginStatus = getLoginStatus()
    this.setData({ isLoggedIn: loginStatus.isLoggedIn })
    
    if (!loginStatus.isLoggedIn) {
      checkLogin({ showToast: false })
      setTimeout(() => {
        checkLogin({ showToast: true })
      }, 100)
      return
    }
    
    const { fromOrder } = options
    if (fromOrder === 'true') {
      this.setData({ fromOrder: true })
    }
    this.loadAddressList()
  },

  onShow() {
    const loginStatus = getLoginStatus()
    this.setData({ isLoggedIn: loginStatus.isLoggedIn })
    
    if (loginStatus.isLoggedIn) {
      this.loadAddressList()
    }
  },

  onPullDownRefresh() {
    this.loadAddressList().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  async loadAddressList() {
    try {
      const res = await addressApi.getAddressList()
      this.setData({
        addressList: res || [],
        useMockData: false
      })
    } catch (error) {
      console.error('加载地址列表失败:', error)
      this.setData({ useMockData: true })
      this.loadMockData()
    }
  },

  loadMockData() {
    const mockAddressList = [
      {
        addressId: 1,
        name: '张三',
        phone: '138****8888',
        province: '北京市',
        city: '北京市',
        district: '朝阳区',
        detail: 'xxx街道xxx号xxx小区xxx号楼xxx室',
        isDefault: true,
        selected: false
      },
      {
        addressId: 2,
        name: '李四',
        phone: '139****9999',
        province: '上海市',
        city: '上海市',
        district: '浦东新区',
        detail: 'xxx路xxx号xxx大厦xxx楼xxx室',
        isDefault: false,
        selected: false
      },
      {
        addressId: 3,
        name: '王五',
        phone: '137****7777',
        province: '广东省',
        city: '深圳市',
        district: '南山区',
        detail: 'xxx大道xxx号xxx科技园xxx栋xxx室',
        isDefault: false,
        selected: false
      }
    ]
    this.setData({ addressList: mockAddressList })
  },

  addAddress() {
    wx.navigateTo({
      url: '/pages/sp_Address_edit_page/sp_Address_edit_page'
    })
  },

  editAddress(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/sp_Address_edit_page/sp_Address_edit_page?id=${id}`
    })
  },

  async deleteAddress(e) {
    const { id } = e.currentTarget.dataset
    wx.showModal({
      title: '提示',
      content: '确定要删除该地址吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            wx.showLoading({ title: '删除中...' })
            await addressApi.deleteAddress(id)
            wx.hideLoading()
            
            wx.showToast({
              title: '删除成功',
              icon: 'success'
            })
            
            this.loadAddressList()
          } catch (error) {
            wx.hideLoading()
            console.error('删除地址失败:', error)
            wx.showToast({
              title: '删除失败',
              icon: 'none'
            })
          }
        }
      }
    })
  },

  async setDefault(e) {
    const { id } = e.currentTarget.dataset
    try {
      wx.showLoading({ title: '设置中...' })
      await addressApi.setDefaultAddress(id)
      wx.hideLoading()
      
      wx.showToast({
        title: '设置成功',
        icon: 'success'
      })
      
      this.loadAddressList()
    } catch (error) {
      wx.hideLoading()
      console.error('设置默认地址失败:', error)
      wx.showToast({
        title: '设置失败',
        icon: 'none'
      })
    }
  },

  selectAddress(e) {
    const { id } = e.currentTarget.dataset
    const { addressList, fromOrder } = this.data
    
    if (fromOrder) {
      const selectedAddress = addressList.find(item => item.addressId === id)
      if (selectedAddress) {
        const pages = getCurrentPages()
        const prevPage = pages[pages.length - 2]
        if (prevPage) {
          prevPage.setData({
            selectedAddress: selectedAddress
          })
          wx.navigateBack()
        }
      }
    }
  },

  stopPropagation() {
    event.stopPropagation()
  }
})