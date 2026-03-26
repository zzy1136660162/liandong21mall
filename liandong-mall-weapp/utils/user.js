/**
 * 用户相关工具函数
 */

const USER_INFO_KEY = 'userInfo';
const TOKEN_KEY = 'token';

/**
 * 检查用户是否已登录
 * @returns {boolean}
 */
const isLogin = () => {
  const token = wx.getStorageSync(TOKEN_KEY);
  return !!token;
};

/**
 * 获取用户信息
 * @returns {object|null}
 */
const getUserInfo = () => {
  return wx.getStorageSync(USER_INFO_KEY) || null;
};

/**
 * 设置用户信息
 * @param {object} userInfo
 */
const setUserInfo = (userInfo) => {
  wx.setStorageSync(USER_INFO_KEY, userInfo);
};

/**
 * 获取 Token
 * @returns {string|null}
 */
const getToken = () => {
  return wx.getStorageSync(TOKEN_KEY) || null;
};

/**
 * 设置 Token
 * @param {string} token
 */
const setToken = (token) => {
  wx.setStorageSync(TOKEN_KEY, token);
};

/**
 * 退出登录
 * @param {function} callback
 */
const logout = (callback) => {
  wx.removeStorageSync(USER_INFO_KEY);
  wx.removeStorageSync(TOKEN_KEY);
  if (typeof callback === 'function') {
    callback();
  }
};

module.exports = {
  isLogin,
  getUserInfo,
  setUserInfo,
  getToken,
  setToken,
  logout
};
