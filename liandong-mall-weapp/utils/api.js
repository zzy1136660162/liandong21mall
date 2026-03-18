/**
 * API 请求工具类
 * 封装微信小程序的 wx.request，提供统一的请求处理
 */

// API 基础配置 - Flask后端服务地址
const API_BASE_URL = 'http://127.0.0.1:5000'; // Flask 后端地址

// 请求方法
const METHOD = {
  GET: 'GET',
  POST: 'POST',
  PUT: 'PUT',
  DELETE: 'DELETE',
  PATCH: 'PATCH'
};

/**
 * 获取存储的 Token
 */
const getToken = () => {
  return wx.getStorageSync('token') || '';
};

/**
 * 统一的请求处理
 * @param {string} url - 请求地址
 * @param {string} method - 请求方法
 * @param {object} data - 请求数据
 * @param {object} header - 请求头
 * @param {boolean} showLoading - 是否显示加载动画
 * @param {boolean} showError - 是否显示错误提示
 */
const request = (url, method = METHOD.GET, data = {}, header = {}, showLoading = true, showError = true) => {
  return new Promise((resolve, reject) => {
    // 显示加载动画
    if (showLoading) {
      wx.showLoading({
        title: '加载中...',
        mask: true
      });
    }

    // 合并请求头
    const requestHeader = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + getToken(),
      ...header
    };

    wx.request({
      url: url.startsWith('http') ? url : API_BASE_URL + url,
      method: method,
      data: data,
      header: requestHeader,
      timeout: 30000,
      success: (res) => {
        // 隐藏加载动画
        if (showLoading) {
          wx.hideLoading();
        }

        // 处理响应状态
        if (res.statusCode >= 200 && res.statusCode < 300) {
          // 请求成功
          resolve(res.data);
        } else if (res.statusCode === 401) {
          // Token 失效，清除登录状态并跳转到登录页
          wx.removeStorageSync('token');
          wx.removeStorageSync('userInfo');
          wx.showToast({
            title: '登录已过期，请重新登录',
            icon: 'none'
          });
          // 可以在这里跳转到登录页
          // wx.navigateTo({ url: '/pages/login/login' });
          reject(new Error('登录已过期'));
        } else if (res.statusCode === 403) {
          wx.showToast({
            title: '没有权限访问',
            icon: 'none'
          });
          reject(new Error('没有权限'));
        } else if (res.statusCode === 404) {
          wx.showToast({
            title: '请求的资源不存在',
            icon: 'none'
          });
          reject(new Error('资源不存在'));
        } else if (res.statusCode >= 500) {
          if (showError) {
            wx.showToast({
              title: '服务器错误，请稍后重试',
              icon: 'none'
            });
          }
          reject(new Error('服务器错误'));
        } else {
          // 其他错误
          const message = res.data && res.data.message ? res.data.message : '请求失败';
          if (showError) {
            wx.showToast({
              title: message,
              icon: 'none'
            });
          }
          reject(new Error(message));
        }
      },
      fail: (err) => {
        // 隐藏加载动画
        if (showLoading) {
          wx.hideLoading();
        }

        // 网络请求失败
        if (showError) {
          wx.showToast({
            title: '网络连接失败，请检查网络',
            icon: 'none'
          });
        }
        reject(new Error('网络请求失败'));
      }
    });
  });
};

/**
 * GET 请求
 */
const get = (url, params = {}, options = {}) => {
  // 构建查询字符串
  let queryString = '';
  if (Object.keys(params).length > 0) {
    const queryParams = Object.keys(params)
      .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(params[key]))
      .join('&');
    queryString = '?' + queryParams;
  }

  return request(url + queryString, METHOD.GET, {}, options.header, options.showLoading, options.showError);
};

/**
 * POST 请求
 */
const post = (url, data = {}, options = {}) => {
  return request(url, METHOD.POST, data, options.header, options.showLoading, options.showError);
};

/**
 * PUT 请求
 */
const put = (url, data = {}, options = {}) => {
  return request(url, METHOD.PUT, data, options.header, options.showLoading, options.showError);
};

/**
 * DELETE 请求
 */
const del = (url, data = {}, options = {}) => {
  return request(url, METHOD.DELETE, data, options.header, options.showLoading, options.showError);
};

/**
 * PATCH 请求
 */
const patch = (url, data = {}, options = {}) => {
  return request(url, METHOD.PATCH, data, options.header, options.showLoading, options.showError);
};

/**
 * 上传文件
 */
const upload = (url, filePath, name = 'file', formData = {}, options = {}) => {
  return new Promise((resolve, reject) => {
    if (options.showLoading !== false) {
      wx.showLoading({
        title: '上传中...',
        mask: true
      });
    }

    wx.uploadFile({
      url: url.startsWith('http') ? url : API_BASE_URL + url,
      filePath: filePath,
      name: name,
      formData: formData,
      header: {
        'Authorization': 'Bearer ' + getToken()
      },
      success: (res) => {
        if (options.showLoading !== false) {
          wx.hideLoading();
        }

        // 解析返回数据
        let data = res.data;
        try {
          data = JSON.parse(res.data);
        } catch (e) {
          // 返回的不是 JSON 格式
        }

        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(data);
        } else {
          reject(new Error(data.message || '上传失败'));
        }
      },
      fail: (err) => {
        if (options.showLoading !== false) {
          wx.hideLoading();
        }
        wx.showToast({
          title: '上传失败',
          icon: 'none'
        });
        reject(new Error('上传失败'));
      }
    });
  });
};

/**
 * 下载文件
 */
const download = (url, options = {}) => {
  return new Promise((resolve, reject) => {
    if (options.showLoading !== false) {
      wx.showLoading({
        title: '下载中...',
        mask: true
      });
    }

    wx.downloadFile({
      url: url.startsWith('http') ? url : API_BASE_URL + url,
      header: {
        'Authorization': 'Bearer ' + getToken()
      },
      success: (res) => {
        if (options.showLoading !== false) {
          wx.hideLoading();
        }

        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.tempFilePath);
        } else {
          reject(new Error('下载失败'));
        }
      },
      fail: (err) => {
        if (options.showLoading !== false) {
          wx.hideLoading();
        }
        wx.showToast({
          title: '下载失败',
          icon: 'none'
        });
        reject(new Error('下载失败'));
      }
    });
  });
};

module.exports = {
  API_BASE_URL,
  METHOD,
  request,
  get,
  post,
  put,
  del,
  patch,
  upload,
  download
};
