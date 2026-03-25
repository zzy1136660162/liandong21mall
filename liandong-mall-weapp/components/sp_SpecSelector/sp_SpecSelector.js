Component({
  properties: {
    show: {
      type: Boolean,
      value: false
    },
    product: {
      type: Object,
      value: {}
    }
  },

  data: {
    selectedSpecs: {},
    quantity: 1,
    selectedPrice: 0,
    selectedStock: 0,
    totalPrice: 0
  },

  observers: {
    'product, selectedSpecs': function(product, selectedSpecs) {
      this.updatePriceAndStock()
    },
    'quantity': function(quantity) {
      this.updateTotalPrice()
    }
  },

  methods: {
    onClose() {
      this.triggerEvent('close')
    },

    stopPropagation() {
      
    },

    onSelectSpec(e) {
      const { name, value } = e.currentTarget.dataset
      const selectedSpecs = { ...this.data.selectedSpecs }
      selectedSpecs[name] = value
      this.setData({ selectedSpecs })
    },

    onDecrease() {
      const quantity = this.data.quantity
      if (quantity > 1) {
        this.setData({ quantity: quantity - 1 })
      }
    },

    onIncrease() {
      const quantity = this.data.quantity
      const selectedStock = this.data.selectedStock
      if (quantity < selectedStock) {
        this.setData({ quantity: quantity + 1 })
      }
    },

    updatePriceAndStock() {
      const product = this.data.product
      const selectedSpecs = this.data.selectedSpecs
      
      if (!product.skus || product.skus.length === 0) {
        this.setData({
          selectedPrice: product.price || 0,
          selectedStock: product.stock || 0
        })
        this.updateTotalPrice()
        return
      }

      let matchedSku = null
      
      for (const sku of product.skus) {
        if (!sku.spec) continue
        
        let isMatch = true
        for (const key in selectedSpecs) {
          if (sku.spec[key] !== selectedSpecs[key]) {
            isMatch = false
            break
          }
        }
        
        if (isMatch) {
          matchedSku = sku
          break
        }
      }

      if (matchedSku) {
        this.setData({
          selectedPrice: matchedSku.price,
          selectedStock: matchedSku.stock
        })
      } else {
        this.setData({
          selectedPrice: product.price,
          selectedStock: product.stock
        })
      }
      
      this.updateTotalPrice()
    },

    updateTotalPrice() {
      const selectedPrice = this.data.selectedPrice
      const quantity = this.data.quantity
      const totalPrice = (selectedPrice * quantity).toFixed(2)
      this.setData({ totalPrice })
    },

    onAddToCart() {
      if (!this.validateSelection()) return

      const { selectedSpecs, quantity } = this.data
      const product = this.data.product
      
      let skuId = null
      if (product.skus && product.skus.length > 0) {
        for (const sku of product.skus) {
          if (!sku.spec) continue
          
          let isMatch = true
          for (const key in selectedSpecs) {
            if (sku.spec[key] !== selectedSpecs[key]) {
              isMatch = false
              break
            }
          }
          
          if (isMatch) {
            skuId = sku.skuId
            break
          }
        }
      }

      this.triggerEvent('addtocart', {
        productId: product.id,
        skuId: skuId,
        quantity: quantity,
        specs: selectedSpecs
      })
    },

    onBuyNow() {
      if (!this.validateSelection()) return

      const { selectedSpecs, quantity } = this.data
      const product = this.data.product
      
      let skuId = null
      if (product.skus && product.skus.length > 0) {
        for (const sku of product.skus) {
          if (!sku.spec) continue
          
          let isMatch = true
          for (const key in selectedSpecs) {
            if (sku.spec[key] !== selectedSpecs[key]) {
              isMatch = false
              break
            }
          }
          
          if (isMatch) {
            skuId = sku.skuId
            break
          }
        }
      }

      this.triggerEvent('buynow', {
        productId: product.id,
        skuId: skuId,
        quantity: quantity,
        specs: selectedSpecs,
        price: this.data.selectedPrice,
        totalPrice: this.data.totalPrice
      })
    },

    validateSelection() {
      const product = this.data.product
      const selectedSpecs = this.data.selectedSpecs
      
      if (product.specs && product.specs.length > 0) {
        for (const spec of product.specs) {
          if (!selectedSpecs[spec.name]) {
            wx.showToast({
              title: `请选择${spec.name}`,
              icon: 'none',
              duration: 2000
            })
            return false
          }
        }
      }
      
      return true
    }
  }
})
