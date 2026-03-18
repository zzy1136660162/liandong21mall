/**
 * 简易 Markdown 解析器
 * 将 Markdown 转换为微信小程序 rich-text 支持的 HTML 格式
 */

/**
 * 解析 Markdown 文本
 * @param {string} markdown - Markdown 格式的文本
 * @returns {string} - HTML 格式的文本
 */
const parseMarkdown = (markdown) => {
  if (!markdown) return '';
  
  let html = markdown;
  
  // 转义 HTML 特殊字符
  html = html.replace(/&/g, '&amp;')
             .replace(/</g, '&lt;')
             .replace(/>/g, '&gt;');
  
  // 解析代码块 ```code```
  html = html.replace(/```([\s\S]*?)```/g, '<pre style="background:#f5f5f5;padding:10px;border-radius:5px;overflow-x:auto;"><code>$1</code></pre>');
  
  // 解析行内代码 `code`
  html = html.replace(/`([^`]+)`/g, '<code style="background:#f5f5f5;padding:2px 4px;border-radius:3px;font-family:monospace;">$1</code>');
  
  // 解析标题 ####
  html = html.replace(/^#### (.*$)/gim, '<h4 style="font-size:16px;font-weight:bold;margin:10px 0;">$1</h4>');
  html = html.replace(/^### (.*$)/gim, '<h3 style="font-size:17px;font-weight:bold;margin:12px 0;">$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2 style="font-size:18px;font-weight:bold;margin:14px 0;">$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1 style="font-size:20px;font-weight:bold;margin:16px 0;">$1</h1>');
  
  // 解析粗体 **text**
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong style="font-weight:bold;">$1</strong>');
  
  // 解析斜体 *text*
  html = html.replace(/\*(.*?)\*/g, '<em style="font-style:italic;">$1</em>');
  
  // 解析删除线 ~~text~~
  html = html.replace(/~~(.*?)~~/g, '<del style="text-decoration:line-through;">$1</del>');
  
  // 解析链接 [text](url)
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" style="color:#1890ff;text-decoration:underline;">$1</a>');
  
  // 解析无序列表 - item
  html = html.replace(/^\- (.*$)/gim, '<li style="margin-left:20px;list-style-type:disc;">$1</li>');
  html = html.replace(/(<li[^>]*>.*<\/li>\n?)+/g, '<ul style="margin:10px 0;padding-left:20px;">$&</ul>');
  
  // 解析有序列表 1. item
  html = html.replace(/^\d+\. (.*$)/gim, '<li style="margin-left:20px;list-style-type:decimal;">$1</li>');
  
  // 解析引用 > text
  html = html.replace(/^&gt; (.*$)/gim, '<blockquote style="border-left:4px solid #1890ff;padding-left:10px;margin:10px 0;color:#666;">$1</blockquote>');
  
  // 解析水平线 ---
  html = html.replace(/^---+$/gim, '<hr style="border:none;border-top:1px solid #e8e8e8;margin:15px 0;" />');
  
  // 解析换行符（保留段落）
  html = html.replace(/\n\n/g, '</p><p style="margin:10px 0;line-height:1.6;">');
  html = html.replace(/\n/g, '<br />');
  
  // 包裹在段落标签中
  if (!html.startsWith('<')) {
    html = '<p style="margin:10px 0;line-height:1.6;">' + html + '</p>';
  }
  
  return html;
};

/**
 * 解析 Markdown 为微信小程序 rich-text 节点格式
 * @param {string} markdown - Markdown 格式的文本
 * @returns {Array} - rich-text 节点数组
 */
const parseToNodes = (markdown) => {
  if (!markdown) return [];
  
  const html = parseMarkdown(markdown);
  
  // 返回 rich-text 支持的格式
  return [{
    type: 'node',
    name: 'div',
    attrs: {
      style: 'font-size:14px;line-height:1.6;color:#333;'
    },
    children: [{
      type: 'text',
      text: html
    }]
  }];
};

module.exports = {
  parseMarkdown,
  parseToNodes
};
