/**
 * 人才库相关API服务
 */
const { get, post, put, delete: del } = require('../utils/api');

const API_BASE = '/api/talent_pool';

module.exports = {
  /**
   * 获取人才列表
   * @param {Object} params - 查询参数
   * @param {number} params.page - 页码
   * @param {number} params.pageSize - 每页数量
   * @param {string} params.area - 领域筛选
   * @param {number} params.experience - 经验筛选
   * @param {string} params.keyword - 搜索关键词
   */
  getTalentList(params = {}) {
    return get(API_BASE + '/list', params);
  },

  /**
   * 获取人才详情
   * @param {number} talentId - 人才ID
   */
  getTalentDetail(talentId) {
    return get(`${API_BASE}/detail/${talentId}`);
  },

  /**
   * 创建人才（后台管理）
   * @param {Object} data - 人才数据
   */
  createTalent(data) {
    return post(`${API_BASE}/create`, data);
  },

  /**
   * 更新人才（后台管理）
   * @param {number} talentId - 人才ID
   * @param {Object} data - 更新数据
   */
  updateTalent(talentId, data) {
    return put(`${API_BASE}/update/${talentId}`, data);
  },

  /**
   * 删除人才（后台管理）
   * @param {number} talentId - 人才ID
   */
  deleteTalent(talentId) {
    return del(`${API_BASE}/delete/${talentId}`);
  },

  /**
   * 切换人才状态（后台管理）
   * @param {number} talentId - 人才ID
   * @param {number} status - 状态
   */
  toggleTalentStatus(talentId, status) {
    return post(`${API_BASE}/toggle_status/${talentId}`, { status });
  }
};
