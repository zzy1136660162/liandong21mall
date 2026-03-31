const BASE_URL = 'http://localhost:5000'

function request(url, options = {}) {
    return new Promise((resolve, reject) => {
        const userId = wx.getStorageSync('userId')
        const token = wx.getStorageSync('token')
        
        console.log('API请求:', options.method, url, 'UserID:', userId || '1')
        
        wx.request({
            url: `${BASE_URL}${url}`,
            method: options.method || 'GET',
            data: options.data || {},
            header: {
                'Content-Type': 'application/json',
                'X-User-Id': userId || '1',
                'Authorization': token ? `Bearer ${token}` : '',
                ...options.header
            },
            success: (res) => {
                console.log('API响应:', url, '状态:', res.statusCode, '数据:', res.data)
                
                if (res.statusCode === 200) {
                    if (res.data.code === 200) {
                        resolve(res.data.data)
                    } else {
                        if (res.data.code === 401) {
                            wx.showToast({
                                title: '请先登录',
                                icon: 'none',
                                duration: 2000
                            })
                            wx.navigateTo({
                                url: '/pages/login/index'
                            })
                        } else {
                            wx.showToast({
                                title: res.data.message || '请求失败',
                                icon: 'none',
                                duration: 2000
                            })
                        }
                        reject(res.data.message)
                    }
                } else {
                    console.error('API错误:', url, res.statusCode, res)
                    wx.showToast({
                        title: '网络错误',
                        icon: 'none',
                        duration: 2000
                    })
                    reject('网络错误')
                }
            },
            fail: (err) => {
                console.error('API请求失败:', url, err)
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
    get: (url, data) => {
        const params = {}
        for (const key in data) {
            if (data[key] !== null && data[key] !== undefined && data[key] !== '') {
                params[key] = data[key]
            }
        }
        return request(url, { method: 'GET', data: params })
    },
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

    addToCart: (productId, skuId, quantity) =>
        api.post('/api/sp/cart/add', { productId, skuId, quantity }),

    updateCartItem: (cartId, quantity) =>
        api.put(`/api/sp/cart/update/${cartId}`, { quantity }),

    deleteCartItem: (cartId) =>
        api.delete(`/api/sp/cart/delete/${cartId}`),

    clearCart: () =>
        api.delete('/api/sp/cart/clear')
}

const orderApi = {
    createOrder: (orderData) =>
        api.post('/api/sp/order/create', orderData),

    getOrderList: (status = null, page = 1, pageSize = 10, keyword = '') =>
        api.get('/api/sp/order/list', { status, page, pageSize, keyword }),

    getOrderDetail: (orderId) => api.get(`/api/sp/order/detail/${orderId}`),

    getOrderExpireTime: (orderId) => api.get(`/api/sp/order/expire-time/${orderId}`),

    getOrderStatistics: () => api.get('/api/sp/order/statistics'),

    getOrderCount: () => api.get('/api/sp/order/count'),

    cancelOrder: (orderId, reason) =>
        api.post(`/api/sp/order/cancel/${orderId}`, { reason }),

    confirmReceipt: (orderId) =>
        api.post(`/api/sp/order/confirm/${orderId}`),

    payOrder: (orderId, paymentMethod = 'WECHAT_PAY') =>
        api.post(`/api/sp/order/pay/${orderId}`, { paymentMethod }),

    searchOrders: (keyword, page = 1, pageSize = 10) =>
        api.get('/api/sp/order/list', { keyword, page, pageSize })
}

const favoriteApi = {
    getFavoriteList: (page = 1, pageSize = 10) =>
        api.get('/api/product/favorite/list', { page, pageSize }),

    addFavorite: (productId) =>
        api.post('/api/product/favorite/add', { productId }),

    removeFavorite: (productId) =>
        api.delete(`/api/product/favorite/${productId}`)
}

const addressApi = {
    getAddressList: () => api.get('/api/sp/address/list'),

    getAddressDetail: (addressId) => api.get(`/api/sp/address/${addressId}`),

    addAddress: (addressData) =>
        api.post('/api/sp/address/add', addressData),

    updateAddress: (addressId, addressData) =>
        api.put(`/api/sp/address/${addressId}`, addressData),

    deleteAddress: (addressId) =>
        api.delete(`/api/sp/address/${addressId}`),

    setDefaultAddress: (addressId) =>
        api.post(`/api/sp/address/set-default/${addressId}`)
}

module.exports = {
    api,
    productApi,
    cartApi,
    orderApi,
    favoriteApi,
    addressApi
}
