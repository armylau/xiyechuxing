// pages/index/index.js - 首页逻辑
Page({
  /**
   * 页面的初始数据
   */
  data: {
    motto: 'Hello World',
    userInfo: null,
    hasUserInfo: false,
    canIUseGetUserProfile: false,
    count: 0
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    console.log('页面加载:', options);
    
    // 检查是否可以使用 getUserProfile
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      });
    }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {
    console.log('页面渲染完成');
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {
    console.log('页面显示');
  },

  /**
   * 点击计数器
   */
  addCount() {
    this.setData({
      count: this.data.count + 1
    });
    
    // 轻触反馈
    wx.vibrateShort({
      type: 'light'
    });
  },

  /**
   * 获取用户信息
   */
  getUserProfile() {
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        console.log('获取用户信息成功:', res.userInfo);
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        });
      },
      fail: (err) => {
        console.log('获取用户信息失败:', err);
        wx.showToast({
          title: '需要授权才能获取信息',
          icon: 'none'
        });
      }
    });
  },

  /**
   * 简单的跳转示例
   */
  navigateToLogs() {
    wx.navigateTo({
      url: '/pages/logs/logs',
      fail: () => {
        wx.showToast({
          title: '页面不存在',
          icon: 'none'
        });
      }
    });
  },

  /**
   * 分享功能
   */
  onShareAppMessage() {
    return {
      title: 'Hello World - 我的第一个小程序',
      desc: '欢迎体验微信小程序',
      path: '/pages/index/index'
    };
  },

  /**
   * 下拉刷新
   */
  onPullDownRefresh() {
    console.log('下拉刷新');
    setTimeout(() => {
      wx.stopPullDownRefresh();
      wx.showToast({
        title: '刷新完成',
        icon: 'success'
      });
    }, 1000);
  }
});
