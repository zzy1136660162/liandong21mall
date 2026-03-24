const addressApi = require('../../utils/sp_api.js').addressApi

Page({
  data: {
    addressId: null,
    formData: {
      name: '',
      phone: '',
      province: '',
      city: '',
      district: '',
      detail: '',
      postcode: '',
      isDefault: false
    }
  },

  onLoad(options) {
    const { id } = options
    if (id) {
      this.setData({ addressId: id })
      this.loadAddressDetail(id)
    }
  },

  async loadAddressDetail(id) {
    try {
      const res = await addressApi.getAddressDetail(id)
      if (res) {
        this.setData({
          formData: {
            name: res.name || '',
            phone: res.phone || '',
            province: res.province || '',
            city: res.city || '',
            district: res.district || '',
            detail: res.detail || '',
            postcode: res.postcode || '',
            isDefault: res.isDefault || false
          }
        })
      }
    } catch (error) {
      console.error('加载地址详情失败:', error)
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
    }
  },

  onNameInput(e) {
    this.setData({
      'formData.name': e.detail.value
    })
  },

  onPhoneInput(e) {
    this.setData({
      'formData.phone': e.detail.value
    })
  },

  chooseRegion() {
    wx.chooseLocation({
      success: (res) => {
        this.setData({
          'formData.province': res.province || '',
          'formData.city': res.city || '',
          'formData.district': res.district || '',
          'formData.detail': res.address || this.data.formData.detail
        })
      },
      fail: (err) => {
        console.error('选择位置失败:', err)
        wx.showToast({
          title: '选择失败',
          icon: 'none'
        })
      }
    })
  },

  onDetailInput(e) {
    this.setData({
      'formData.detail': e.detail.value
    })
  },

  onPostcodeInput(e) {
    this.setData({
      'formData.postcode': e.detail.value
    })
  },

  toggleDefault() {
    this.setData({
      'formData.isDefault': !this.data.formData.isDefault
    })
  },

  validateForm() {
    const { name, phone, province, city, district, detail } = this.data.formData

    if (!name || name.trim() === '') {
      wx.showToast({
        title: '请输入收货人姓名',
        icon: 'none'
      })
      return false
    }

    if (!phone || phone.trim() === '') {
      wx.showToast({
        title: '请输入手机号码',
        icon: 'none'
      })
      return false
    }

    if (!/^1[3-9]\d{9}$/.test(phone)) {
      wx.showToast({
        title: '请输入正确的手机号码',
        icon: 'none'
      })
      return false
    }

    if (!province || !city || !district) {
      wx.showToast({
        title: '请选择所在地区',
        icon: 'none'
      })
      return false
    }

    if (!detail || detail.trim() === '') {
      wx.showToast({
        title: '请输入详细地址',
        icon: 'none'
      })
      return false
    }

    return true
  },

  async saveAddress() {
    if (!this.validateForm()) {
      return
    }

    try {
      wx.showLoading({ title: '保存中...' })

      const { addressId, formData } = this.data
      const addressData = {
        ...formData,
        name: formData.name.trim(),
        phone: formData.phone.trim(),
        detail: formData.detail.trim()
      }

      if (addressId) {
        await addressApi.updateAddress(addressId, addressData)
      } else {
        await addressApi.addAddress(addressData)
      }

      wx.hideLoading()

      wx.showToast({
        title: '保存成功',
        icon: 'success'
      })

      setTimeout(() => {
        wx.navigateBack()
      }, 1500)
    } catch (error) {
      wx.hideLoading()
      console.error('保存地址失败:', error)
      wx.showToast({
        title: '保存失败',
        icon: 'none'
      })
    }
  }
})