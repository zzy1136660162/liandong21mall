/**
 * 样品申请相关API服务
 */
const { get, post } = require('../utils/api');

const API_BASE = '/api/samples';

module.exports = {
  /**
   * 获取样品申请列表
   * @param {Object} params - 查询参数
   * @param {string} params.status - 状态筛选
   * @param {number} params.page - 页码
   * @param {number} params.pageSize - 每页数量
   */
  getSamples(params = {}) {
    return get(API_BASE, params);
  },

  /**
   * 提交样品申请
   * @param {Object} data - 申请数据
   * @param {Array} data.productIds - 商品ID列表
   * @param {string} data.recipientName - 收件人姓名
   * @param {string} data.phone - 联系电话
   * @param {string} data.province - 省份
   * @param {string} data.city - 城市
   * @param {string} data.district - 区县
   * @param {string} data.address - 详细地址
   * @param {string} data.remark - 备注
   */
  applySample(data) {
    return post(`${API_BASE}/apply`, data);
  },

  /**
   * 获取样品申请详情
   * @param {string} id - 申请单号
   */
  getSampleDetail(id) {
    return get(`${API_BASE}/${id}`);
  },

  /**
   * 确认收货
   * @param {string} id - 申请单号
   */
  receiveSample(id) {
    return post(`${API_BASE}/${id}/receive`);
  }
};
