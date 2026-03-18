const chatService = require('../../utils/chatService');
const markdownParser = require('../../utils/markdownParser');
const app = getApp();

// 调试日志
const log = (tag, data) => {
  console.log(`[ChatPage] ${tag}:`, data);
};

Page({
  data: {
    messages: [],
    inputValue: '',
    sessionId: '',
    scrollToMessage: '',
    isLoading: false,
    userInfo: null,
    quickQuestions: [
      '如何提交研发需求？',
      '需求审核需要多久？',
      '怎么查看需求进度？',
      '如何申请成为达人？',
      '样品申请流程是什么？'
    ]
  },

  onLoad() {
    log('页面加载', 'onLoad');
    
    // 获取用户信息
    const userInfo = wx.getStorageSync('userInfo') || {};
    log('获取用户信息', userInfo);
    this.setData({ userInfo });
    
    // 初始化会话
    this.initChatSession();
    
    // 添加欢迎消息
    this.addMessage({
      type: 'system',
      content: '欢迎使用智能客服，我是您的专属助手，请问有什么可以帮助您？'
    });
  },

  onUnload() {
    log('页面卸载', 'onUnload');
    // 页面卸载时结束会话
    if (this.data.sessionId) {
      chatService.endSession(this.data.sessionId).catch(err => {
        console.error('结束会话失败:', err);
      });
    }
  },

  // 初始化会话
  async initChatSession() {
    log('初始化会话', '开始');
    try {
      const userData = {
        userId: app.globalData.userId,
        ...this.data.userInfo
      };
      log('初始化会话参数', userData);
      
      const res = await chatService.initSession(userData);
      log('初始化会话响应', res);
      
      if (res.sessionId) {
        this.setData({ sessionId: res.sessionId });
        log('会话ID已设置', res.sessionId);
      }
    } catch (err) {
      console.error('初始化会话失败:', err);
      log('初始化会话错误', err);
    }
  },

  // 添加消息到列表
  addMessage(message) {
    log('添加消息', message);
    const messages = this.data.messages;
    message.id = Date.now();
    message.time = this.formatTime(new Date());
    
    // 如果是 AI 消息，解析 Markdown
    if ((message.type === 'agent' || message.type === 'system') && message.content) {
      message.htmlContent = markdownParser.parseMarkdown(message.content);
      log('Markdown 解析后', message.htmlContent);
    }
    
    messages.push(message);
    
    log('当前消息列表长度', messages.length);
    
    this.setData({
      messages,
      scrollToMessage: `msg-${message.id}`
    });
  },

  // 格式化时间
  formatTime(date) {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
  },

  // 输入框变化
  onInputChange(e) {
    const value = e.detail.value;
    this.setData({
      inputValue: value
    });
  },

  // 发送消息
  async sendMessage() {
    const content = this.data.inputValue.trim();
    log('发送消息', { content, isLoading: this.data.isLoading });
    
    if (!content || this.data.isLoading) {
      log('发送消息被阻止', { empty: !content, loading: this.data.isLoading });
      return;
    }

    // 添加用户消息
    this.addMessage({
      type: 'user',
      content
    });

    this.setData({
      inputValue: '',
      isLoading: true
    });

    try {
      log('调用chatService.sendMessage', {
        content,
        sessionId: this.data.sessionId,
        userInfo: this.data.userInfo
      });
      
      // 调用智能客服接口
      const res = await chatService.sendMessage(
        content,
        this.data.sessionId,
        this.data.userInfo
      );
      
      log('sendMessage 响应', res);

      // 添加客服回复
      if (res.reply) {
        log('添加客服回复', res.reply);
        this.addMessage({
          type: 'agent',
          content: res.reply,
          suggestions: res.suggestions || []
        });
      } else {
        log('响应中没有reply字段', res);
        this.addMessage({
          type: 'system',
          content: '抱歉，服务器返回数据异常，请稍后重试。'
        });
      }

      // 更新会话ID
      if (res.sessionId) {
        log('更新会话ID', res.sessionId);
        this.setData({ sessionId: res.sessionId });
      }
    } catch (err) {
      console.error('发送消息失败:', err);
      log('发送消息错误', err);
      this.addMessage({
        type: 'system',
        content: '抱歉，网络连接出现问题，请稍后重试。'
      });
    } finally {
      this.setData({ isLoading: false });
      log('发送消息完成', 'finally');
    }
  },

  // 点击快捷问题
  onQuickQuestionTap(e) {
    const question = e.currentTarget.dataset.question;
    log('点击快捷问题', question);
    this.setData({ inputValue: question });
    this.sendMessage();
  },

  // 点击建议选项
  onSuggestionTap(e) {
    const suggestion = e.currentTarget.dataset.suggestion;
    log('点击建议选项', suggestion);
    this.setData({ inputValue: suggestion });
    this.sendMessage();
  },

  // 长按消息复制
  onMessageLongPress(e) {
    const content = e.currentTarget.dataset.content;
    log('长按消息', content);
    wx.setClipboardData({
      data: content,
      success: () => {
        wx.showToast({
          title: '已复制',
          icon: 'success'
        });
      }
    });
  },

  // 返回上一页
  goBack() {
    log('返回上一页', 'goBack');
    wx.navigateBack();
  },

  // 跳转到人工客服
  contactHuman() {
    log('联系人工客服', 'contactHuman');
    wx.showModal({
      title: '联系人工客服',
      content: '人工客服工作时间：9:00-18:00\n客服电话：400-xxx-xxxx',
      showCancel: false
    });
  }
});
