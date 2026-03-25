const cartApi = require('../../utils/sp_api.js').cartApi
const { checkLogin, getLoginStatus } = require('../../utils/sp_auth.js')

Page({
  data: {
    cartList: [],
    allSelected: false,
    selectedCount: 0,
    totalPrice: 0,
    useMockData: false,
    editMode: false,
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
    
    this.loadCart()
  },

  onShow() {
    const loginStatus = getLoginStatus()
    this.setData({ isLoggedIn: loginStatus.isLoggedIn })
    
    if (loginStatus.isLoggedIn) {
      this.loadCart()
    }
  },

  onPullDownRefresh() {
    this.loadCart().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  async loadCart() {
    try {
      console.log('开始加载购物车...')
      const res = await cartApi.getCartList()
      console.log('购物车API返回数据:', res)
      const cartList = (res || []).map(item => ({
        ...item,
        selected: false
      }))
      console.log('处理后的购物车数据:', cartList)
      this.setData({ cartList, useMockData: false })
      this.calculateTotal()
    } catch (error) {
      console.error('加载购物车失败:', error)
      this.setData({ useMockData: true })
      this.loadMockData()
    }
  },

  loadMockData() {
    const mockCartList = [
      {
        cartId: 1,
        productId: 42,
        productName: '焕颜修护精华液',
        mainImage: 'https://images.unsplash.com/photo-1522335789203-aabd016d8d3?w=400&h=400&fit=crop',
        specs: '30ml',
        price: 299.00,
        quantity: 2,
        selected: false
      },
      {
        cartId: 2,
        productId: 43,
        productName: '深层清洁洁面乳',
        mainImage: 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop',
        specs: '100ml',
        price: 158.00,
        quantity: 1,
        selected: false
      },
      {
        cartId: 3,
        productId: 44,
        productName: '保湿修护面霜',
        mainImage: 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=400&h=400&fit=crop',
        specs: '50g',
        price: 358.00,
        quantity: 1,
        selected: false
      },
      {
        cartId: 4,
        productId: 45,
        productName: '舒缓修护精华水',
        mainImage: 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc8?w=400&h=400&fit=crop',
        specs: '150ml',
        price: 228.00,
        quantity: 3,
        selected: false
      },
      {
        cartId: 5,
        productId: 46,
        productName: '紧致抗皱眼霜',
        mainImage: 'https://images.unsplash.com/photo-1570194065650-d99fb4b38b15?w=400&h=400&fit=crop',
        specs: '15g',
        price: 268.00,
        quantity: 1,
        selected: false
      }
    ]
    this.setData({ cartList: mockCartList })
    this.calculateTotal()
  },

  toggleSelect(e) {
    const { id } = e.currentTarget.dataset
    const { cartList } = this.data
    const index = cartList.findIndex(item => item.cartId === id)
    if (index !== -1) {
      cartList[index].selected = !cartList[index].selected
      this.setData({ cartList })
      this.calculateTotal()
    }
  },

  selectAll() {
    const { cartList, allSelected } = this.data
    cartList.forEach(item => {
      item.selected = !allSelected
    })
    this.setData({
      cartList,
      allSelected: !allSelected
    })
    this.calculateTotal()
  },

  toggleEditMode() {
    const { editMode } = this.data
    this.setData({ editMode: !editMode })
  },

  calculateTotal() {
    const { cartList } = this.data
    const selectedItems = cartList.filter(item => item.selected)
    const selectedCount = selectedItems.length
    const totalPrice = selectedItems.reduce((sum, item) => {
      return sum + item.price * item.quantity
    }, 0).toFixed(2)
    
    const allSelected = cartList.length > 0 && cartList.every(item => item.selected)
    
    this.setData({
      selectedCount,
      totalPrice,
      allSelected
    })
  },

  async increaseQuantity(e) {
    const { id } = e.currentTarget.dataset
    const { cartList } = this.data
    const index = cartList.findIndex(item => item.cartId === id)
    if (index !== -1) {
      const newQuantity = cartList[index].quantity + 1
      try {
        await cartApi.updateCartQuantity(id, newQuantity)
        cartList[index].quantity = newQuantity
        this.setData({ cartList })
        this.calculateTotal()
      } catch (error) {
        console.error('更新数量失败:', error)
        wx.showToast({
          title: '更新失败',
          icon: 'none'
        })
      }
    }
  },

  async decreaseQuantity(e) {
    const { id } = e.currentTarget.dataset
    const { cartList } = this.data
    const index = cartList.findIndex(item => item.cartId === id)
    if (index !== -1 && cartList[index].quantity > 1) {
      const newQuantity = cartList[index].quantity - 1
      try {
        await cartApi.updateCartQuantity(id, newQuantity)
        cartList[index].quantity = newQuantity
        this.setData({ cartList })
        this.calculateTotal()
      } catch (error) {
        console.error('更新数量失败:', error)
        wx.showToast({
          title: '更新失败',
          icon: 'none'
        })
      }
    }
  },

  async deleteItem(e) {
    const { id } = e.currentTarget.dataset
    wx.showModal({
      title: '提示',
      content: '确定要删除该商品吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await cartApi.deleteCartItem(id)
            const { cartList } = this.data
            const newCartList = cartList.filter(item => item.cartId !== id)
            this.setData({ cartList: newCartList })
            this.calculateTotal()
            wx.showToast({
              title: '删除成功',
              icon: 'success'
            })
          } catch (error) {
            console.error('删除失败:', error)
            wx.showToast({
              title: '删除失败',
              icon: 'none'
            })
          }
        }
      }
    })
  },

  deleteSelected() {
    const { cartList } = this.data
    const selectedItems = cartList.filter(item => item.selected)
    if (selectedItems.length === 0) {
      wx.showToast({
        title: '请先选择商品',
        icon: 'none'
      })
      return
    }
    
    wx.showModal({
      title: '提示',
      content: `确定要删除${selectedItems.length}件商品吗？`,
      success: async (res) => {
        if (res.confirm) {
          try {
            await Promise.all(selectedItems.map(item => cartApi.deleteCartItem(item.cartId)))
            const newCartList = cartList.filter(item => !item.selected)
            this.setData({ cartList: newCartList })
            this.calculateTotal()
            wx.showToast({
              title: '删除成功',
              icon: 'success'
            })
          } catch (error) {
            console.error('批量删除失败:', error)
            wx.showToast({
              title: '删除失败',
              icon: 'none'
            })
          }
        }
      }
    })
  },

  goToShopping() {
    wx.switchTab({
      url: '/pages/Product_list_page/Product_list_page'
    })
  },

  goToCheckout() {
    if (!checkLogin({ showToast: false })) {
      checkLogin({ showToast: true })
      return
    }
    
    const { cartList } = this.data
    const selectedItems = cartList.filter(item => item.selected)
    if (selectedItems.length === 0) {
      wx.showToast({
        title: '请先选择商品',
        icon: 'none'
      })
      return
    }
    
    wx.navigateTo({
      url: '/pages/sp_Order_confirm_page/sp_Order_confirm_page'
    })
  },

  goToDetail(e) {
    const { id } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/sp_Details/sp_Details?id=${id}`
    })
  }
})
