// app.js - 西野出行小程序入口
const localData = require('./utils/data.js');

App({
  globalData: {
    userInfo: null,
    // API 基础地址
    apiBase: 'http://localhost:5050',
    // apiBase: 'https://your-domain.com', // 生产环境
    
    // 本地数据（离线时使用）
    cities: localData.CITIES,
    seatClasses: localData.SEAT_CLASSES,
    mealOptions: localData.MEAL_OPTIONS,
    hotRoutes: localData.HOT_ROUTES,
    quickLinks: localData.QUICK_LINKS,
    foods: localData.FOODS,
    hotels: localData.HOTELS,
    attractions: localData.ATTRACTIONS,
    safetyTips: localData.SAFETY_TIPS,
    pointsLevels: localData.POINTS_LEVELS,
  },

  onLaunch() {
    console.log('西野出行小程序启动');
    
    // 尝试从服务器加载最新数据
    this.loadBaseData();
    
    // 获取本地存储的用户信息
    const userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.globalData.userInfo = userInfo;
    }
  },

  // 加载基础数据（城市、舱位、餐食）
  async loadBaseData() {
    try {
      const [citiesRes, seatRes, mealRes] = await Promise.all([
        this.request('/api/cities').catch(() => null),
        this.request('/api/seat_classes').catch(() => null),
        this.request('/api/meals').catch(() => null)
      ]);
      
      // 如果服务器返回成功，更新数据
      if (citiesRes && citiesRes.code === 0) {
        this.globalData.cities = citiesRes.data;
      }
      if (seatRes && seatRes.code === 0) {
        this.globalData.seatClasses = seatRes.data;
      }
      if (mealRes && mealRes.code === 0) {
        this.globalData.mealOptions = mealRes.data;
      }
      
      console.log('基础数据加载完成');
    } catch (err) {
      console.log('使用本地数据');
    }
  },

  // 封装网络请求
  request(url, method = 'GET', data = null) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: this.globalData.apiBase + url,
        method,
        data,
        header: {
          'Content-Type': 'application/json'
        },
        timeout: 10000,
        success: (res) => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(res.data);
          } else {
            reject(new Error(`HTTP ${res.statusCode}`));
          }
        },
        fail: reject
      });
    });
  },

  // 获取本地美食数据
  getFoods(cityId) {
    return this.globalData.foods[cityId] || [];
  },

  // 获取本地酒店数据
  getHotels(cityId) {
    return this.globalData.hotels[cityId] || [];
  },

  // 获取本地景点数据
  getAttractions(cityId) {
    const list = this.globalData.attractions[cityId] || [];
    // 添加渐变样式
    const grads = ['grad-1', 'grad-2', 'grad-3', 'grad-4', 'grad-5', 'grad-6'];
    return list.map((item, index) => ({
      ...item,
      gradClass: grads[index % 6]
    }));
  },

  // 显示提示
  toast(title, icon = 'none') {
    wx.showToast({ title, icon });
  },

  // 显示加载中
  showLoading(title = '加载中...') {
    wx.showLoading({ title, mask: true });
  },

  hideLoading() {
    wx.hideLoading();
  }
});
