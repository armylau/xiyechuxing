// app.js - 小程序入口文件
App({
  // 小程序初始化时执行
  onLaunch(options) {
    console.log('小程序启动:', options);
    
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || [];
    logs.unshift(Date.now());
    wx.setStorageSync('logs', logs);
  },

  // 小程序显示时执行
  onShow(options) {
    console.log('小程序显示:', options);
  },

  // 小程序隐藏时执行
  onHide() {
    console.log('小程序隐藏');
  },

  // 全局数据
  globalData: {
    userInfo: null,
    version: '1.0.0'
  }
});
