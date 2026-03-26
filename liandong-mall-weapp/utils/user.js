/**
 * 用户工具类
 * 封装用户登录状态检查、用户信息获取等功能
 */

/**
 * 检查用户是否已登录
 * @returns {boolean} 是否已登录
 */
const isLogin = () => {
  const token = wx.getStorageSync('token');
  const userInfo = wx.getStorageSync('userInfo');
  return !!(token && userInfo);
};

/**
 * 获取当前登录用户信息
 * @returns {object|null} 用户信息
 */
const getUserInfo = () => {
  return wx.getStorageSync('userInfo') || null;
};

/**
 * 获取当前登录 Token
 * @returns {string} Token
 */
const getToken = () => {
  return wx.getStorageSync('token') || '';
};

/**
 * 保存用户信息
 * @param {object} userInfo 用户信息
 */
const setUserInfo = (userInfo) => {
  wx.setStorageSync('userInfo', userInfo);
};

/**
 * 保存 Token
 * @param {string} token Token
 */
const setToken = (token) => {
  wx.setStorageSync('token', token);
};

/**
 * 清除登录信息
 */
const clearLoginInfo = () => {
  wx.removeStorageSync('token');
  wx.removeStorageSync('userInfo');
};

/**
 * 检查登录状态，未登录则跳转到登录页
 * @param {string} redirect 登录成功后的跳转地址
 * @returns {boolean} 是否已登录
 */
const checkLogin = (redirect = '') => {
  if (!isLogin()) {
    let url = '/pages/login/index';
    if (redirect) {
      url += `?redirect=${encodeURIComponent(redirect)}`;
    }
    wx.navigateTo({
      url: url
    });
    return false;
  }
  return true;
};

/**
 * 退出登录
 * @param {function} callback 退出后的回调函数
 */
const logout = (callback) => {
  wx.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        clearLoginInfo();
        wx.showToast({
          title: '已退出登录',
          icon: 'success'
        });
        setTimeout(() => {
          wx.switchTab({
            url: '/pages/index/index'
          });
          if (callback && typeof callback === 'function') {
            callback();
          }
        }, 1500);
      }
    }
  });
};

/**
 * 检查是否为 VIP 会员
 * @returns {boolean} 是否为 VIP
 */
const isVIP = () => {
  const userInfo = getUserInfo();
  return userInfo && userInfo.isMember;
};

/**
 * 检查是否为达人
 * @returns {boolean} 是否为达人
 */
const isTalent = () => {
  const userInfo = getUserInfo();
  return userInfo && userInfo.isTalent;
};

/**
 * 获取会员等级
 * @returns {string|null} 会员等级
 */
const getMemberLevel = () => {
  const userInfo = getUserInfo();
  return userInfo ? userInfo.memberLevel : null;
};

/**
 * 获取达人状态
 * @returns {string|null} 达人状态
 */
const getTalentStatus = () => {
  const userInfo = getUserInfo();
  return userInfo ? userInfo.talentStatus : null;
};

module.exports = {
  isLogin,
  getUserInfo,
  getToken,
  setUserInfo,
  setToken,
  clearLoginInfo,
  checkLogin,
  logout,
  isVIP,
  isTalent,
  getMemberLevel,
  getTalentStatus
};
