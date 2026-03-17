// 模拟 API 服务 - 用于演示
// 当后端服务不可用时，使用本地存储模拟数据

const MOCK_DATA_KEY = 'rd_demand_mock_data';

// 获取模拟数据
const getMockData = () => {
  const data = wx.getStorageSync(MOCK_DATA_KEY);
  return data || { demands: [], progress: [] };
};

// 保存模拟数据
const saveMockData = (data) => {
  wx.setStorageSync(MOCK_DATA_KEY, data);
};

// 生成需求编号
const generateDemandNo = () => {
  const date = new Date();
  const dateStr = `${date.getFullYear()}${String(date.getMonth() + 1).padStart(2, '0')}${String(date.getDate()).padStart(2, '0')}`;
  const random = Math.floor(1000 + Math.random() * 9000);
  return `RD${dateStr}${random}`;
};

// 状态映射
const statusMap = {
  0: '待处理',
  1: '需求确认中',
  2: '研发中',
  3: '样品制作中',
  4: '已完成',
  5: '已取消'
};

// 处理提交需求
const handleSubmit = (data) => {
  const mockData = getMockData();
  console.log('提交需求 - submitterId:', data.submitterId);
  
  const newDemand = {
    id: Date.now(),
    demandNo: generateDemandNo(),
    ...data,
    status: 0,
    submitTime: new Date().toISOString().replace('T', ' ').substring(0, 19),
    updateTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
  };
  mockData.demands.push(newDemand);
  
  // 添加初始进度
  mockData.progress.push({
    id: Date.now() + 1,
    demandId: newDemand.id,
    demandNo: newDemand.demandNo,
    progressRemark: '需求已提交，等待处理',
    statusBefore: null,
    statusAfter: 0,
    operatorName: data.submitterName || '用户',
    operatorType: 1,
    createTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
  });
  
  saveMockData(mockData);
  
  return { 
    code: 0, 
    message: '需求提交成功', 
    data: { id: newDemand.id, demandNo: newDemand.demandNo }, 
    success: true 
  };
};

// 处理获取列表
const handleList = (url) => {
  const mockData = getMockData();
  
  // 手动解析 URL 参数
  const queryString = url.split('?')[1] || '';
  const params = {};
  queryString.split('&').forEach(pair => {
    const [key, value] = pair.split('=');
    if (key) params[key] = decodeURIComponent(value || '');
  });
  
  const submitterId = params.submitterId;
  const status = params.status;
  
  console.log('获取列表 - submitterId:', submitterId);
  console.log('获取列表 - 所有需求数量:', mockData.demands.length);
  
  let list = mockData.demands.filter(d => d.submitterId === submitterId);
  console.log('获取列表 - 过滤后数量:', list.length);
  
  if (status !== null && status !== '' && status !== undefined) {
    list = list.filter(d => d.status === parseInt(status));
  }
  
  // 格式化数据
  list = list.map(item => ({
    id: item.id,
    demandNo: item.demandNo,
    title: item.title,
    status: item.status,
    statusText: statusMap[item.status],
    submitTime: item.submitTime,
    expectedDeliveryTime: item.expectedDeliveryTime
  })).sort((a, b) => b.id - a.id);
  
  const result = { 
    code: 0, 
    message: '操作成功', 
    data: { 
      list, 
      total: list.length, 
      page: 1, 
      pageSize: 10,
      totalPages: 1
    }, 
    success: true 
  };
  
  console.log('获取列表 - 返回数据:', result);
  return result;
};

// 处理获取详情
const handleDetail = (url) => {
  const mockData = getMockData();
  const match = url.match(/\/detail\/(\d+)/);
  if (!match) {
    return { code: 400, message: 'ID格式错误', success: false };
  }
  
  const id = parseInt(match[1]);
  const demand = mockData.demands.find(d => d.id === id);
  
  if (demand) {
    return { 
      code: 0, 
      message: '操作成功', 
      data: {
        ...demand,
        statusText: statusMap[demand.status]
      }, 
      success: true 
    };
  } else {
    return { code: 404, message: '需求不存在', success: false };
  }
};

// 处理获取进度
const handleProgress = (url) => {
  const mockData = getMockData();
  const match = url.match(/\/progress\/(\d+)/);
  if (!match) {
    return { code: 400, message: 'ID格式错误', success: false };
  }
  
  const demandId = parseInt(match[1]);
  let list = mockData.progress.filter(p => p.demandId === demandId);
  
  // 格式化数据
  list = list.map(item => ({
    id: item.id,
    progressRemark: item.progressRemark,
    statusBefore: item.statusBefore,
    statusBeforeText: item.statusBefore !== null ? statusMap[item.statusBefore] : null,
    statusAfter: item.statusAfter,
    statusAfterText: item.statusAfter !== null ? statusMap[item.statusAfter] : null,
    operatorName: item.operatorName,
    operatorType: item.operatorType,
    operatorTypeText: item.operatorType === 2 ? '管理员' : '用户',
    createTime: item.createTime
  }));
  
  return { code: 0, message: '操作成功', data: list, success: true };
};

// 处理撤回需求
const handleWithdraw = (data) => {
  const mockData = getMockData();
  const { demandId, submitterId } = data;
  
  console.log('撤回需求 - demandId:', demandId, 'submitterId:', submitterId);
  
  // 查找需求
  const demandIndex = mockData.demands.findIndex(d => d.id === demandId);
  if (demandIndex === -1) {
    return { code: 404, message: '需求不存在', success: false };
  }
  
  const demand = mockData.demands[demandIndex];
  
  // 验证提交人身份
  if (demand.submitterId !== submitterId) {
    return { code: 403, message: '无权操作此需求', success: false };
  }
  
  // 检查状态是否允许撤回（只有待处理状态可以撤回）
  if (demand.status !== 0) {
    return { code: 400, message: '该需求状态不允许撤回', success: false };
  }
  
  // 更新需求状态为已取消
  const oldStatus = demand.status;
  demand.status = 5; // 已取消
  demand.updateTime = new Date().toISOString().replace('T', ' ').substring(0, 19);
  
  // 添加进度记录
  mockData.progress.push({
    id: Date.now(),
    demandId: demand.id,
    demandNo: demand.demandNo,
    progressRemark: '用户撤回需求',
    statusBefore: oldStatus,
    statusAfter: 5,
    operatorName: demand.submitterName || '用户',
    operatorType: 1,
    createTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
  });
  
  saveMockData(mockData);
  
  return { 
    code: 0, 
    message: '需求已撤回', 
    data: { id: demand.id, status: 5 }, 
    success: true 
  };
};

// 处理删除需求
const handleDelete = (data) => {
  const mockData = getMockData();
  const { demandId, submitterId } = data;
  
  console.log('删除需求 - demandId:', demandId, 'submitterId:', submitterId);
  
  // 查找需求
  const demandIndex = mockData.demands.findIndex(d => d.id === demandId);
  if (demandIndex === -1) {
    return { code: 404, message: '需求不存在', success: false };
  }
  
  const demand = mockData.demands[demandIndex];
  
  // 验证提交人身份
  if (demand.submitterId !== submitterId) {
    return { code: 403, message: '无权操作此需求', success: false };
  }
  
  // 检查状态是否允许删除（只有已取消状态可以删除）
  if (demand.status !== 5) {
    return { code: 400, message: '该需求状态不允许删除，请先撤回', success: false };
  }
  
  // 删除需求
  mockData.demands.splice(demandIndex, 1);
  
  // 删除相关的进度记录
  mockData.progress = mockData.progress.filter(p => p.demandId !== demandId);
  
  saveMockData(mockData);
  
  return { 
    code: 0, 
    message: '需求已删除', 
    data: { id: demandId }, 
    success: true 
  };
};

// 处理重新申请
const handleReapply = (data) => {
  const mockData = getMockData();
  const { demandId, submitterId } = data;
  
  console.log('重新申请 - demandId:', demandId, 'submitterId:', submitterId);
  
  // 查找需求
  const demandIndex = mockData.demands.findIndex(d => d.id === demandId);
  if (demandIndex === -1) {
    return { code: 404, message: '需求不存在', success: false };
  }
  
  const demand = mockData.demands[demandIndex];
  
  // 验证提交人身份
  if (demand.submitterId !== submitterId) {
    return { code: 403, message: '无权操作此需求', success: false };
  }
  
  // 检查状态是否允许重新申请（只有已取消状态可以重新申请）
  if (demand.status !== 5) {
    return { code: 400, message: '该需求状态不允许重新申请', success: false };
  }
  
  // 更新需求状态为待处理
  const oldStatus = demand.status;
  demand.status = 0; // 待处理
  demand.demandNo = generateDemandNo(); // 生成新的需求编号
  demand.submitTime = new Date().toISOString().replace('T', ' ').substring(0, 19);
  demand.updateTime = demand.submitTime;
  
  // 添加进度记录
  mockData.progress.push({
    id: Date.now(),
    demandId: demand.id,
    demandNo: demand.demandNo,
    progressRemark: '用户重新提交申请',
    statusBefore: oldStatus,
    statusAfter: 0,
    operatorName: demand.submitterName || '用户',
    operatorType: 1,
    createTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
  });
  
  saveMockData(mockData);
  
  return { 
    code: 0, 
    message: '重新申请成功', 
    data: { id: demand.id, demandNo: demand.demandNo, status: 0 }, 
    success: true 
  };
};

// 模拟 API 请求
const mockRequest = (options) => {
  const { url, method = 'GET', data, success, fail } = options;
  
  console.log('mockRequest 收到请求:', url, 'method:', method);
  
  // 模拟网络延迟
  setTimeout(() => {
    try {
      let response;
      
      // 解析 URL 并路由到对应的处理函数
      if (url.includes('/demand/submit') && method === 'POST') {
        response = handleSubmit(data);
      } else if (url.includes('/demand/withdraw') && method === 'POST') {
        response = handleWithdraw(data);
      } else if (url.includes('/demand/delete') && method === 'POST') {
        response = handleDelete(data);
      } else if (url.includes('/demand/reapply') && method === 'POST') {
        response = handleReapply(data);
      } else if (url.includes('/demand/list')) {
        response = handleList(url);
      } else if (url.includes('/demand/detail/')) {
        response = handleDetail(url);
      } else if (url.includes('/demand/progress/')) {
        response = handleProgress(url);
      } else {
        response = { code: 404, message: '接口不存在', success: false };
      }
      
      console.log('mockRequest 返回响应:', url, response);
      success && success(response);
    } catch (error) {
      console.error('mockRequest 错误:', error);
      fail && fail(error);
    }
  }, 100); // 减少延迟到 100ms
};

module.exports = {
  mockRequest
};
