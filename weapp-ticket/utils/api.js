// utils/api.js - API 封装
const app = getApp();

/**
 * API 请求封装
 */
class Api {
  constructor() {
    this.baseUrl = '';
  }

  // GET 请求
  get(url, params = null) {
    let fullUrl = url;
    if (params) {
      const queryString = Object.keys(params)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
        .join('&');
      fullUrl += `?${queryString}`;
    }
    return this.request(fullUrl, 'GET');
  }

  // POST 请求
  post(url, data = {}) {
    return this.request(url, 'POST', data);
  }

  // 通用请求
  request(url, method = 'GET', data = null) {
    return new Promise((resolve, reject) => {
      const appInstance = getApp();
      
      wx.request({
        url: appInstance.globalData.apiBase + url,
        method,
        data,
        header: {
          'Content-Type': 'application/json'
        },
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
  }

  // ========== 具体 API ==========

  // 获取城市列表
  getCities() {
    return this.get('/api/cities');
  }

  // 获取舱位等级
  getSeatClasses() {
    return this.get('/api/seat_classes');
  }

  // 获取餐食选项
  getMeals() {
    return this.get('/api/meals');
  }

  // 搜索车次
  searchTrains(from, to, date) {
    return this.get('/api/trains/search', { from, to, date });
  }

  // 智能推荐
  recommendTrains(from, to, date, preference) {
    return this.get('/api/trains/recommend', { from, to, date, preference });
  }

  // 折扣车票
  discountTrains(from, to, date) {
    return this.get('/api/trains/discount', { from, to, date });
  }

  // 获取景点列表
  getAttractions(cityId) {
    return this.get('/api/attractions', { city_id: cityId });
  }

  // 获取景点详情
  getAttractionDetail(id) {
    return this.get(`/api/attractions/${id}`);
  }

  // 获取美食
  getFoods(cityId) {
    return this.get('/api/foods', { city_id: cityId });
  }

  // 获取酒店
  getHotels(cityId) {
    return this.get('/api/hotels', { city_id: cityId });
  }

  // 创建订单
  createOrder(data) {
    return this.post('/api/orders', data);
  }

  // 查询订单
  getOrders(phone = null) {
    const params = phone ? { phone } : null;
    return this.get('/api/orders', params);
  }

  // 查询积分
  getPoints(phone) {
    return this.get('/api/points', { phone });
  }

  // 获取积分等级
  getPointsLevels() {
    return this.get('/api/points/levels');
  }

  // 获取安全提示
  getSafetyTips() {
    return this.get('/api/safety_tips');
  }
}

module.exports = new Api();
