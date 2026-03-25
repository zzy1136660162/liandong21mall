Page({
  data: {},

  onLoad() {},

  takePhoto() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['camera'],
      success: (res) => {
        const tempFilePath = res.tempFiles[0].tempFilePath;
        this.handleImage(tempFilePath);
      }
    });
  },

  chooseFromAlbum() {
    wx.chooseMedia({
      count: 1,
      mediaType: ['image'],
      sourceType: ['album'],
      success: (res) => {
        const tempFilePath = res.tempFiles[0].tempFilePath;
        this.handleImage(tempFilePath);
      }
    });
  },

  scanCode() {
    wx.scanCode({
      success: (res) => {
        console.log('扫码结果:', res);
        if (res.result) {
          wx.navigateTo({
            url: '/pages/search/search?keyword=' + encodeURIComponent(res.result)
          });
        }
      },
      fail: (err) => {
        console.log('扫码失败:', err);
      }
    });
  },

  handleImage(imagePath) {
    wx.showLoading({ title: '识别中...' });
    setTimeout(() => {
      wx.hideLoading();
      wx.navigateTo({
        url: '/pages/search/search?image=' + encodeURIComponent(imagePath)
      });
    }, 1000);
  }
});
