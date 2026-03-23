const cartApi = require('../../utils/sp_api.js').cartApi
const orderApi = require('../../utils/sp_api.js').orderApi
const addressApi = require('../../utils/sp_api.js').addressApi

Page({
  data: {
    address: {
      addressId: null,
      name: '张三',
      phone: '138****8888',
      province: '北京市',
      city: '北京市',
      district: '朝阳区',
      detail: 'xxx街道xxx号'
    },
    orderItems: [],
    totalAmount: 0,
    shippingFee: 0,
    discountAmount: 0,
    finalAmount: 0,
    remark: '',
    useMockData: false
  },

  onLoad(options) {
    // 监听来自商品详情页的事件
    const eventChannel = this.getOpenerEventChannel()
    if (eventChannel) {
      eventChannel.on('orderDataFromProduct', (data) => {
        // 从商品详情页直接购买
        if (data && data.from === 'buyNow') {
          this.setData({ useMockData: false })
          this.handleBuyNowData(data.orderItems)
          return
        }
      })
    }
    
    // 正常从购物车加载
    this.loadOrderItems()
    this.loadDefaultAddress()
  },

  onShow() {
    const pages = getCurrentPages()
    const currentPage = pages[pages.length - 1]
    if (currentPage.data.selectedAddress) {
      this.setData({
        address: currentPage.data.selectedAddress
      })
    }
  },

  async loadOrderItems() {
    try {
      const res = await cartApi.getCartList()
      const cartList = res || []
      const selectedItems = cartList.filter(item => item.selected)
      
      if (selectedItems.length === 0) {
        this.setData({ useMockData: true })
        this.loadMockData()
        return
      }

      const totalAmount = selectedItems.reduce((sum, item) => {
        return sum + item.price * item.quantity
      }, 0).toFixed(2)

      const shippingFee = totalAmount >= 99 ? 0 : 10
      const discountAmount = 0
      const finalAmount = (parseFloat(totalAmount) + shippingFee - discountAmount).toFixed(2)

      this.setData({
        orderItems: selectedItems,
        totalAmount,
        shippingFee,
        discountAmount,
        finalAmount,
        useMockData: false
      })
    } catch (error) {
      console.error('加载订单商品失败:', error)
      this.setData({ useMockData: true })
      this.loadMockData()
    }
  },

  loadMockData() {
    const mockOrderItems = [
      {
        productId: 42,
        productName: '焕颜修护精华液',
        mainImage: 'https://images.unsplash.com/photo-1522335789203-aabd016d8d3?w=400&h=400&fit=crop',
        specs: '30ml',
        price: 299.00,
        quantity: 2
      },
      {
        productId: 43,
        productName: '深层清洁洁面乳',
        mainImage: 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop',
        specs: '100ml',
        price: 158.00,
        quantity: 1
      },
      {
        productId: 44,
        productName: '保湿修护面霜',
        mainImage: 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=400&h=400&fit=crop',
        specs: '50g',
        price: 358.00,
        quantity: 1
      }
    ]

    const totalAmount = mockOrderItems.reduce((sum, item) => {
      return sum + item.price * item.quantity
    }, 0).toFixed(2)

    const shippingFee = totalAmount >= 99 ? 0 : 10
    const discountAmount = 0
    const finalAmount = (parseFloat(totalAmount) + shippingFee - discountAmount).toFixed(2)

    this.setData({
      orderItems: mockOrderItems,
      totalAmount,
      shippingFee,
      discountAmount,
      finalAmount
    })
  },

  // 处理直接购买的数据
  handleBuyNowData(orderItems) {
    // 计算总金额
    const totalAmount = orderItems.reduce((sum, item) => {
      return sum + item.price * item.quantity
    }, 0).toFixed(2)

    // 计算运费（满99免运费）
    const shippingFee = totalAmount >= 99 ? 0 : 10
    const discountAmount = 0
    const finalAmount = (parseFloat(totalAmount) + shippingFee - discountAmount).toFixed(2)

    this.setData({
      orderItems,
      totalAmount,
      shippingFee,
      discountAmount,
      finalAmount
    })
  },

  async loadDefaultAddress() {
    try {
      const res = await addressApi.getAddressList()
      if (res && res.length > 0) {
        const defaultAddress = res.find(item => item.isDefault) || res[0]
        this.setData({
          address: {
            addressId: defaultAddress.addressId,
            name: defaultAddress.name,
            phone: defaultAddress.phone,
            province: defaultAddress.province,
            city: defaultAddress.city,
            district: defaultAddress.district,
            detail: defaultAddress.detail
          }
        })
      }
    } catch (error) {
      console.error('加载默认地址失败:', error)
    }
  },

  editAddress() {
    const { address } = this.data
    if (address.addressId) {
      wx.navigateTo({
        url: `/pages/sp_Address_edit_page/sp_Address_edit_page?id=${address.addressId}`
      })
    } else {
      wx.navigateTo({
        url: '/pages/sp_Address_edit_page/sp_Address_edit_page'
      })
    }
  },

  selectAddress() {
    wx.navigateTo({
      url: '/pages/sp_Address_page/sp_Address_page?fromOrder=true'
    })
  },

  onRemarkInput(e) {
    this.setData({
      remark: e.detail.value
    })
  },

  async submitOrder() {
    const { orderItems, address, finalAmount, remark } = this.data

    if (!address || !address.name) {
      wx.showToast({
        title: '请选择收货地址',
        icon: 'none'
      })
      return
    }

    wx.showLoading({
      title: '提交中...'
    })

    try {
      const orderData = {
        items: orderItems.map(item => ({
          productId: item.productId,
          quantity: item.quantity,
          price: item.price
        })),
        address: {
          name: address.name,
          phone: address.phone,
          detail: address.detail
        },
        totalAmount: this.data.totalAmount,
        shippingFee: this.data.shippingFee,
        discountAmount: this.data.discountAmount,
        finalAmount: finalAmount,
        remark: remark
      }

      const res = await orderApi.createOrder(orderData)

      wx.hideLoading()

      if (res.code === 200) {
        wx.showToast({
          title: '订单提交成功',
          icon: 'success'
        })

        setTimeout(() => {
          wx.redirectTo({
            url: `/pages/sp_Order_detail_page/sp_Order_detail_page?id=${res.data.orderId}`
          })
        }, 1500)
      } else {
        wx.showToast({
          title: res.message || '提交失败',
          icon: 'none'
        })
      }
    } catch (error) {
      wx.hideLoading()
      console.error('提交订单失败:', error)
      wx.showToast({
        title: '提交失败',
        icon: 'none'
      })
    }
  }
})
