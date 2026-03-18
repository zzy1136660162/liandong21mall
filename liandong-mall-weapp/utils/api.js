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
    getCategories: () => api.get('/product/category/list'),

    getProducts: (params) => api.get('/product/list', params),

    getProductDetail: (productId) => api.get(`/product/${productId}`),

    getHotProducts: (limit = 10) => api.get('/product/hot', { limit }),

    getNewProducts: (limit = 10) => api.get('/product/new', { limit }),

    getRecommendProducts: (limit = 10) => api.get('/product/recommend', { limit }),

    searchProducts: (keyword, page = 1, pageSize = 10) =>
        api.get('/product/search', { keyword, page, pageSize })
}

const cartApi = {
    getCartList: () => api.get('/product/cart/list'),

    addToCart: (productId, skuId = null, quantity = 1) =>
        api.post('/product/cart/add', { productId, skuId, quantity }),

    updateCartQuantity: (cartId, quantity) =>
        api.put(`/product/cart/update/${cartId}`, { quantity }),

    updateCartSelected: (cartId, selected) =>
        api.put(`/product/cart/select/${cartId}`, { selected }),

    deleteCartItem: (cartId) => api.delete(`/product/cart/delete/${cartId}`),

    clearCart: () => api.delete('/product/cart/clear'),

    getCartTotal: () => api.get('/product/cart/total')
}

const orderApi = {
    submitOrder: (cartItems, addressInfo, remark) =>
        api.post('/product/order/submit', { cartItems, addressInfo, remark }),

    getOrderList: (status = null, page = 1, pageSize = 10) =>
        api.get('/product/order/list', { status, page, pageSize }),

    getOrderDetail: (orderId) => api.get(`/product/order/detail/${orderId}`),

    cancelOrder: (orderId, reason) =>
        api.post(`/product/order/cancel/${orderId}`, { reason })
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

module.exports = {
    BASE_URL,
    request,
    api,
    productApi,
    cartApi,
    orderApi,
    userApi,
    talentApi
}
