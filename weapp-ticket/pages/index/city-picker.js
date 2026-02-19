// pages/index/city-picker.js - 城市选择器
const app = getApp();

Page({
  data: {
    type: '', // 'from' 或 'to'
    cities: [],
    currentId: ''
  },

  onLoad(options) {
    const { type, current } = options;
    this.setData({
      type,
      currentId: current,
      cities: app.globalData.cities
    });
    
    // 如果全局数据未加载，从接口获取
    if (!this.data.cities.length) {
      this.loadCities();
    }
  },

  async loadCities() {
    try {
      const res = await app.request('/api/cities');
      if (res.code === 0) {
        this.setData({ cities: res.data });
        app.globalData.cities = res.data;
      }
    } catch (err) {
      app.toast('加载城市失败');
    }
  },

  // 选择城市
  selectCity(e) {
    const { id, name } = e.currentTarget.dataset;
    const city = { id, name };
    
    // 返回上一页并传递数据
    const pages = getCurrentPages();
    const prevPage = pages[pages.length - 2];
    
    if (this.data.type === 'from') {
      prevPage.setData({ fromCity: city });
    } else {
      prevPage.setData({ toCity: city });
    }
    
    wx.navigateBack();
  }
});
