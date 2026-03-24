/**
 * 智能客服服务
 * 对接云托引擎智能客服 API
 */

// 智能客服 API 地址
const CHAT_API_URL = 'http://agent.yuntuoengine.com/api';

// API 密钥 (FastGPT 格式: 完整的 API Key)
const API_KEY = 'fastgpt-bDgdD1cREGZz88WOqfbN2W4tkxQ2y5txUVzgneMjfM8DdE80B9h9llt';

// 备用密钥 (如果上面的不行，尝试使用不带前缀的)
const API_TOKEN = 'bDgdD1cREGZz88WOqfbN2W4tkxQ2y5txUVzgneMjfM8DdE80B9h9llt';

// 调试开关
const DEBUG = true;

/**
 * 打印调试信息
 * @param {string} tag - 标签
 * @param {any} data - 数据
 */
const log = (tag, data) => {
  if (DEBUG) {
    console.log(`[ChatService] ${tag}:`, data);
  }
};

/**
 * 发送消息到智能客服 (FastGPT OpenAI 格式)
 * @param {string} message - 用户消息
 * @param {string} sessionId - 会话ID（用于保持上下文）
 * @param {object} userInfo - 用户信息（可选）
 * @returns {Promise} - 返回客服回复
 */
const sendMessage = (message, sessionId = '', userInfo = {}) => {
  log('sendMessage 开始', { message, sessionId, userInfo });
  
  return new Promise((resolve, reject) => {
    // FastGPT OpenAI 格式 API
    const url = `${CHAT_API_URL}/v1/chat/completions`;
    
    log('请求URL', url);
    
    // OpenAI 标准格式请求体
    const requestData = {
      model: 'gpt-3.5-turbo',
      messages: [
        {
          role: 'system',
          content: '你是一个专业的电商选品平台客服助手，可以帮助用户解答关于研发需求提交、需求审核、进度查询、达人申请、样品申请等问题。请用中文回答，语气友好专业。'
        },
        {
          role: 'user',
          content: message
        }
      ],
      temperature: 0.7,
      max_tokens: 1000,
      stream: false
    };
    
    // FastGPT 使用完整的 API_KEY 作为 token (包含 fastgpt- 前缀)
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + API_KEY
    };
    
    log('请求数据', requestData);
    log('请求头', { ...headers, Authorization: 'Bearer ***' });
    
    wx.request({
      url: url,
      method: 'POST',
      data: requestData,
      header: headers,
      timeout: 30000,
      success: (res) => {
        log('请求成功', { statusCode: res.statusCode, data: res.data });
        
        if (res.statusCode === 200 && res.data.choices && res.data.choices[0]) {
          // OpenAI 格式响应
          let reply = res.data.choices[0].message.content;
          // 清理可能重复的回复
          reply = cleanDuplicateReply(reply);
          log('API返回成功，使用真实回复', reply);
          resolve({
            reply: reply,
            sessionId: sessionId || 'fastgpt_' + Date.now(),
            suggestions: getSuggestions(message)
          });
        } else {
          log(`API返回异常`, res.data);
          // 返回模拟回复
          const reply = getSimulatedReply(message);
          resolve({
            reply,
            sessionId: sessionId || 'local_' + Date.now(),
            suggestions: getSuggestions(message)
          });
        }
      },
      fail: (err) => {
        log('请求失败', err);
        // 返回模拟回复
        const reply = getSimulatedReply(message);
        resolve({
          reply,
          sessionId: sessionId || 'local_' + Date.now(),
          suggestions: getSuggestions(message)
        });
      }
    });
  });
};

/**
 * 清理重复的回复内容
 * @param {string} reply - 原始回复
 * @returns {string} - 清理后的回复
 */
const cleanDuplicateReply = (reply) => {
  if (!reply) return reply;
  
  // 首先检查是否有整段重复（同一句话出现多次）
  // 常见模式：句子A\n句子B\n句子A\n句子B
  const trimmedReply = reply.trim();
  const halfLength = Math.floor(trimmedReply.length / 2);
  
  // 检查前半部分和后半部分是否相同
  const firstHalf = trimmedReply.substring(0, halfLength).trim();
  const secondHalf = trimmedReply.substring(halfLength).trim();
  
  // 如果后半部分包含前半部分的主要内容，可能是重复
  if (secondHalf.includes(firstHalf.substring(0, Math.min(20, firstHalf.length)))) {
    // 可能是重复，返回前半部分
    log('检测到整段重复，清理后半部分');
    return firstHalf;
  }
  
  // 按换行符分割进行行去重
  const lines = reply.split('\n');
  const seen = new Set();
  const uniqueLines = [];
  
  for (const line of lines) {
    const trimmed = line.trim();
    // 跳过空行
    if (!trimmed) continue;
    // 如果这行已经出现过，跳过
    if (seen.has(trimmed)) continue;
    seen.add(trimmed);
    uniqueLines.push(line);
  }
  
  const result = uniqueLines.join('\n');
  
  // 再次检查：如果结果还是包含明显的重复段落（超过50字重复）
  if (result.length > 100) {
    const midPoint = Math.floor(result.length / 2);
    const firstPart = result.substring(0, midPoint);
    const secondPart = result.substring(midPoint);
    
    // 检查第一部分是否在第二部分中出现
    if (secondPart.includes(firstPart.substring(0, Math.min(50, firstPart.length)))) {
      log('检测到段落重复，返回前半部分');
      return firstPart;
    }
  }
  
  return result;
};

/**
 * 根据用户消息生成模拟回复
 * @param {string} message - 用户消息
 * @returns {string} - 回复内容
 */
const getSimulatedReply = (message) => {
  log('getSimulatedReply 调用', message);
  
  if (!message) {
    log('消息为空，返回默认回复');
    return '您好！我是智能客服助手，请问有什么可以帮助您的？';
  }
  
  const msg = message.toLowerCase();
  log('处理消息', msg);
  
  if (msg.includes('提交') || msg.includes('需求')) {
    log('匹配到: 提交/需求');
    return '提交研发需求非常简单：\n1. 点击首页的"提交需求"按钮\n2. 填写产品名称、需求描述等信息\n3. 选择需求类型和优先级\n4. 提交后等待审核\n\n一般在1-2个工作日内会有专人联系您确认需求详情。';
  }
  if (msg.includes('审核') || msg.includes('多久')) {
    log('匹配到: 审核/多久');
    return '需求审核时间通常为1-2个工作日。审核通过后，我们会立即安排研发团队与您对接，制定详细的开发计划。您可以在"我的需求"页面实时查看审核进度。';
  }
  if (msg.includes('进度') || msg.includes('查看')) {
    log('匹配到: 进度/查看');
    return '查看需求进度的方法：\n1. 进入"我的需求"页面\n2. 点击对应的需求卡片\n3. 在详情页查看当前状态和进度\n\n系统会在关键节点自动推送进度通知给您。';
  }
  if (msg.includes('达人') || msg.includes('申请')) {
    log('匹配到: 达人/申请');
    return '申请成为达人的条件：\n1. 完成实名认证\n2. 有一定的带货经验\n3. 粉丝数量达到一定要求\n\n申请入口：我的 -> 达人中心 -> 申请成为达人。提交申请后我们会在3个工作日内完成审核。';
  }
  if (msg.includes('样品') || msg.includes('申请')) {
    log('匹配到: 样品/申请');
    return '样品申请流程：\n1. 在选品中心找到心仪的产品\n2. 点击"申请样品"按钮\n3. 填写收货信息和推广计划\n4. 等待商家审核\n\n审核通过后，样品会尽快寄出，您可以在"我的样品"中查看物流信息。';
  }
  if (msg.includes('你好') || msg.includes('您好') || msg.includes('在吗')) {
    log('匹配到: 你好/您好/在吗');
    return '您好！我是智能客服助手，很高兴为您服务。请问有什么可以帮助您的？';
  }
  if (msg.includes('谢谢') || msg.includes('感谢')) {
    log('匹配到: 谢谢/感谢');
    return '不客气！如果您还有其他问题，随时可以问我。祝您使用愉快！';
  }
  if (msg.includes('人工') || msg.includes('客服')) {
    log('匹配到: 人工/客服');
    return '如需联系人工客服，请拨打：400-xxx-xxxx\n工作时间：周一至周五 9:00-18:00\n\n或者发送邮件至：support@example.com';
  }
  
  log('未匹配到关键词，返回默认回复');
  return '感谢您的咨询！我是智能客服助手，可以帮您解答以下问题：\n• 如何提交研发需求\n• 需求审核需要多久\n• 怎么查看需求进度\n• 如何申请成为达人\n• 样品申请流程\n\n请直接输入您想了解的问题，或点击下方的快捷问题。';
};

/**
 * 根据用户消息生成建议选项
 * @param {string} message - 用户消息
 * @returns {Array} - 建议选项列表
 */
const getSuggestions = (message) => {
  log('getSuggestions 调用', message);
  
  if (!message) {
    return ['如何提交研发需求？', '需求审核需要多久？', '怎么查看需求进度？', '联系人工客服'];
  }
  
  const msg = message.toLowerCase();
  
  if (msg.includes('提交') || msg.includes('需求')) {
    return ['需求审核需要多久？', '怎么查看需求进度？', '联系人工客服'];
  }
  if (msg.includes('审核')) {
    return ['如何提交研发需求？', '怎么查看需求进度？', '联系人工客服'];
  }
  if (msg.includes('进度')) {
    return ['如何提交研发需求？', '需求审核需要多久？', '联系人工客服'];
  }
  if (msg.includes('达人')) {
    return ['样品申请流程是什么？', '如何提交研发需求？', '联系人工客服'];
  }
  if (msg.includes('样品')) {
    return ['如何申请成为达人？', '如何提交研发需求？', '联系人工客服'];
  }
  
  return ['如何提交研发需求？', '需求审核需要多久？', '怎么查看需求进度？', '联系人工客服'];
};

/**
 * 获取客服历史记录
 * @param {string} sessionId - 会话ID
 * @returns {Promise} - 返回历史消息列表
 */
const getChatHistory = (sessionId) => {
  log('getChatHistory 调用', sessionId);
  
  return new Promise((resolve) => {
    // 本地存储历史记录
    const history = wx.getStorageSync('chat_history_' + sessionId) || [];
    log('获取历史记录', { sessionId, count: history.length });
    resolve({ history });
  });
};

/**
 * 初始化客服会话
 * @param {object} userInfo - 用户信息
 * @returns {Promise} - 返回会话ID
 */
const initSession = (userInfo = {}) => {
  log('initSession 调用', userInfo);
  
  return new Promise((resolve) => {
    // 生成本地会话ID
    const sessionId = 'session_' + Date.now();
    log('生成会话ID', sessionId);
    resolve({ sessionId });
  });
};

/**
 * 结束客服会话
 * @param {string} sessionId - 会话ID
 * @returns {Promise}
 */
const endSession = (sessionId) => {
  log('endSession 调用', sessionId);
  
  return new Promise((resolve) => {
    // 清理本地存储的历史记录
    wx.removeStorageSync('chat_history_' + sessionId);
    log('清理历史记录完成', sessionId);
    resolve({ success: true });
  });
};

/**
 * 保存聊天记录到本地
 * @param {string} sessionId - 会话ID
 * @param {Array} messages - 消息列表
 */
const saveChatHistory = (sessionId, messages) => {
  log('saveChatHistory 调用', { sessionId, count: messages.length });
  wx.setStorageSync('chat_history_' + sessionId, messages);
};

module.exports = {
  sendMessage,
  getChatHistory,
  initSession,
  endSession,
  saveChatHistory,
  CHAT_API_URL,
  DEBUG
};
