const BASE_URL = 'http://localhost:5000'

function request(url, options = {}) {
    return new Promise((resolve, reject) => {
        wx.request({
            url: `${BASE_URL}${url}`,
            method: options.method || 'GET',
            data: options.data || {},
            header: {
                'Content-Type': 'application/json',
                'X-User-Id': wx.getStorageSync('userId') || '1',
                ...options.header
            },
            success: (res) => {
                if (res.statusCode === 200) {
                    if (res.data.code === 200) {
                        resolve(res.data.data)
                    } else {
                        wx.showToast({
                            title: res.data.message || '请求失败',
                            icon: 'none',
                            duration: 2000
                        })
                        reject(res.data.message)
                    }
                } else {
                    wx.showToast({
                        title: '网络错误',
                        icon: 'none',
                        duration: 2000
                    })
                    reject('网络错误')
                }
            },
            fail: (err) => {
                wx.showToast({
                    title: '网络连接失败',
                    icon: 'none',
                    duration: 2000
                })
                reject(err)
            }
        })
    })
}

const api = {
    get: (url, data) => request(url, { method: 'GET', data }),
    post: (url, data) => request(url, { method: 'POST', data }),
    put: (url, data) => request(url, { method: 'PUT', data }),
    delete: (url, data) => request(url, { method: 'DELETE', data })
}

const productApi = {
    getCategories: () => api.get('/api/sp/category/list'),

    getProducts: (params) => api.get('/api/sp/product/list', params),

    getProductDetail: (productId) => api.get(`/api/sp/product/${productId}`),

    getHotProducts: (limit = 10) => api.get('/api/sp/product/hot', { limit }),

    getNewProducts: (limit = 10) => api.get('/api/sp/product/new', { limit }),

    getRecommendProducts: (limit = 10) => api.get('/api/sp/product/recommend', { limit }),

    searchProducts: (keyword, page = 1, pageSize = 10) =>
        api.get('/api/sp/product/search', { keyword, page, pageSize })
}

const cartApi = {
    getCartList: () => api.get('/api/sp/cart/list'),

    addToCart: (productId, skuId = null, quantity = 1) =>
        api.post('/api/sp/cart/add', { productId, skuId, quantity }),

    updateCartQuantity: (cartId, quantity) =>
        api.put(`/api/sp/cart/update/${cartId}`, { quantity }),

    updateCartSelected: (cartId, selected) =>
        api.put(`/api/sp/cart/select/${cartId}`, { selected }),

    deleteCartItem: (cartId) => api.delete(`/api/sp/cart/delete/${cartId}`),

    clearCart: () => api.delete('/api/sp/cart/clear'),

    getCartTotal: () => api.get('/api/sp/cart/total')
}

const orderApi = {
    createOrder: (orderData) =>
        api.post('/api/sp/order/create', orderData),

    getOrderList: (status = null, page = 1, pageSize = 10) =>
        api.get('/api/sp/order/list', { status, page, pageSize }),

    getOrderDetail: (orderId) => api.get(`/api/sp/order/detail/${orderId}`),

    cancelOrder: (orderId, reason) =>
        api.post(`/api/sp/order/cancel/${orderId}`, { reason }),

    confirmReceipt: (orderId) =>
        api.post(`/api/sp/order/confirm/${orderId}`)
}

const favoriteApi = {
    getFavoriteList: (page = 1, pageSize = 10) =>
        api.get('/api/product/favorite/list', { page, pageSize }),

    addFavorite: (productId) =>
        api.post('/api/product/favorite/add', { productId }),

    removeFavorite: (productId) =>
        api.post('/api/product/favorite/remove', { productId }),

    checkFavorite: (productId) =>
        api.get(`/api/product/favorite/check/${productId}`),

    getFavoriteCount: () =>
        api.get('/api/product/favorite/count')
}

const userApi = {
    getUserInfo: () => api.get('/user/info'),

    updateUserInfo: (data) => api.put('/user/info', data),

    getMemberInfo: () => api.get('/user/member'),

    upgradeToVip: (orderId) => api.post('/user/member/upgrade', { orderId })
}

const talentApi = {
    submitApply: (data) => api.post('/user/talent/apply', data),

    getTalentStatus: () => api.get('/user/talent/status'),

    getTalentInfo: () => api.get('/user/talent/info')
}

const addressApi = {
    getAddressList: () => api.get('/api/sp/address/list'),

    getAddressDetail: (addressId) => api.get(`/api/sp/address/detail/${addressId}`),

    addAddress: (addressData) => api.post('/api/sp/address/add', addressData),

    updateAddress: (addressId, addressData) =>
        api.put(`/api/sp/address/update/${addressId}`, addressData),

    deleteAddress: (addressId) => api.delete(`/api/sp/address/delete/${addressId}`),

    setDefaultAddress: (addressId) =>
        api.put(`/api/sp/address/default/${addressId}`)
}

module.exports = {
    BASE_URL,
    request,
    api,
    productApi,
    cartApi,
    orderApi,
    favoriteApi,
    userApi,
    talentApi,
    addressApi
}
