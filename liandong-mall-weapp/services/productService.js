/**
 * 商品相关API服务
 */
const { get, post } = require('../utils/api');

const API_BASE = '/api/product';
const API_LIST_BASE = '/api/product/list';

module.exports = {
  /**
   * 获取商品列表
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.pageSize - 每页数量
   * @param {string} params.category - 分类
   * @param {string} params.keyword - 关键词
   * @param {string} params.sortBy - 排序方式
   * @param {string} params.sortOrder - 排序顺序
   */
  getProducts(params = {}) {
    return get(API_LIST_BASE, params);
  },

  /**
   * 获取商品详情
   * @param {string|number} id - 商品ID
   */
  getProductDetail(id) {
    return get(`${API_BASE}/${id}`);
  },

  /**
   * 获取商品佣金信息
   * @param {string|number} id - 商品ID
   */
  getProductCommission(id) {
    return get(`${API_BASE}/${id}/commission`);
  },

  /**
   * 获取分类列表
   */
  getCategories() {
    return get(`${API_BASE}/categories`);
  },

  /**
   * 获取活动列表
   */
  getActivities() {
    return get(`${API_BASE}/activities`);
  },

  /**
   * 获取活动商品
   * @param {string} type - 活动类型
   * @param {Object} params - 查询参数
   */
  getActivityProducts(type, params = {}) {
    return get(`${API_BASE}/activities/${type}/products`, params);
  },

  /**
   * 搜索商品
   * @param {string} keyword - 搜索关键词
   * @param {Object} params - 查询参数
   */
  searchProducts(keyword, params = {}) {
    return get(`${API_BASE}/search`, { keyword, ...params });
  },

  /**
   * 获取搜索联想
   */
  getSearchSuggestions(keyword) {
    return get(`${API_BASE}/search/suggestions`, { keyword });
  },

  /**
   * 获取热门搜索词
   */
  getHotSearches() {
    return get(`${API_BASE}/search/hot`);
  },

  /**
   * 获取榜单
   * @param {string} type - 榜单类型
   * @param {Object} params - 查询参数
   */
  getRankings(type = 'hot', params = {}) {
    return get(`${API_BASE}/rankings`, { type, ...params });
  },

  /**
   * 查询物流
   * @param {string} company - 物流公司编码
   * @param {string} trackingNo - 物流单号
   */
  queryLogistics(company, trackingNo) {
    return get(`${API_BASE}/logistics/query`, { company, trackingNo });
  }
};
