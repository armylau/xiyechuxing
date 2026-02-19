// pages/trains/trains.js - 车次结果页
const app = getApp();
const { generateMockTrains } = require('../../utils/data.js');

Page({
  data: {
    from: '',
    to: '',
    date: '',
    preference: 'fastest',
    fromCityName: '',
    toCityName: '',
    trains: [],
    filteredTrains: [],
    filterType: 'all', // all, high, dong, recommend, discount
    loading: true,
    useLocalData: false
  },

  onLoad(options) {
    const { from, to, date, preference } = options;
    this.setData({ from, to, date, preference });
    
    // 获取城市名称
    const cities = app.globalData.cities;
    const fromCity = cities.find(c => c.id === from);
    const toCity = cities.find(c => c.id === to);
    
    this.setData({
      fromCityName: fromCity ? fromCity.name : from,
      toCityName: toCity ? toCity.name : to
    });
    
    this.loadTrains();
  },

  // 加载车次数据 - 优先API，失败使用本地数据
  async loadTrains() {
    const { from, to, date, preference } = this.data;
    
    this.setData({ loading: true, useLocalData: false });
    app.showLoading();
    
    try {
      // 尝试从服务器加载
      await this.loadFromAPI(from, to, date, preference);
    } catch (err) {
      console.log('API加载失败，使用本地数据');
      this.loadLocalData(from, to, date);
    } finally {
      app.hideLoading();
    }
  },

  // 从API加载
  async loadFromAPI(from, to, date, preference) {
    const [searchRes, recRes, discountRes] = await Promise.all([
      app.request(`/api/trains/search?from=${from}&to=${to}&date=${date}`),
      app.request(`/api/trains/recommend?from=${from}&to=${to}&date=${date}&preference=${preference}`),
      app.request(`/api/trains/discount?from=${from}&to=${to}&date=${date}`)
    ]);
    
    let trains = searchRes.data || [];
    
    if (trains.length === 0) {
      throw new Error('无车次数据');
    }
    
    const recommendedIds = new Set((recRes.data || []).map(t => t.id));
    const discountResults = discountRes.data || [];
    
    // 构建折扣和推荐信息映射
    const discountMap = {};
    discountResults.forEach(d => {
      discountMap[d.id] = {
        rate: d.discount_rate,
        price: d.discounted_price,
        label: d.discount_label,
        reasons: d.discount_reasons
      };
    });
    
    const recMap = {};
    (recRes.data || []).forEach(t => {
      recMap[t.id] = t.recommend_reasons || [];
    });
    
    // 合并数据并格式化
    trains = this.formatTrains(trains, recommendedIds, recMap, discountMap);
    
    this.setData({
      trains,
      loading: false,
      useLocalData: false
    });
    
    this.applyFilter();
  },

  // 加载本地模拟数据
  loadLocalData(from, to, date) {
    // 生成模拟车次
    let trains = generateMockTrains(from, to, date);
    
    // 根据偏好添加推荐标记
    const { preference } = this.data;
    trains = trains.map((t, index) => {
      let isRecommended = false;
      let recommendReasons = [];
      let discount = null;
      
      // 模拟推荐逻辑
      if (preference === 'fastest' && t.duration < 300) {
        isRecommended = true;
        recommendReasons.push('速度最快');
      } else if (preference === 'cheapest' && t.price < 400) {
        isRecommended = true;
        recommendReasons.push('价格最低');
      } else if (preference === 'comfortable' && t.train_type === '高铁') {
        isRecommended = true;
        recommendReasons.push('舒适度高');
      }
      
      // 随机给部分车次添加折扣
      if (index === 1 || index === 3) {
        discount = {
          rate: 0.85,
          price: Math.round(t.price * 0.85),
          label: '8.5折',
          reasons: ['限时特惠']
        };
      }
      
      return {
        ...t,
        is_recommended: isRecommended,
        recommend_reasons: recommendReasons,
        discount
      };
    });
    
    // 格式化时间
    trains = this.formatTrains(trains, new Set(), {}, {});
    
    this.setData({
      trains,
      loading: false,
      useLocalData: true
    });
    
    this.applyFilter();
    
    // 提示用户
    wx.showToast({
      title: '使用演示数据',
      icon: 'none',
      duration: 2000
    });
  },

  // 格式化车次数据
  formatTrains(trains, recommendedIds, recMap, discountMap) {
    return trains.map(t => {
      const departTime = t.depart_time ? t.depart_time.split(' ')[1] : '';
      const arriveTime = t.arrive_time ? t.arrive_time.split(' ')[1] : '';
      const durationH = Math.floor(t.duration / 60);
      const durationM = t.duration % 60;
      const durationText = durationM === 0 ? `${durationH}小时` : `${durationH}小时${durationM}分`;
      
      return {
        ...t,
        is_recommended: recommendedIds.has(t.id) || t.is_recommended,
        recommend_reasons: recMap[t.id] || t.recommend_reasons || [],
        discount: discountMap[t.id] || t.discount || null,
        departTime,
        arriveTime,
        durationText
      };
    });
  },

  // 筛选车次
  filterTrains(e) {
    const type = e.currentTarget.dataset.type;
    this.setData({ filterType: type }, () => {
      this.applyFilter();
    });
  },

  // 应用筛选
  applyFilter() {
    const { trains, filterType } = this.data;
    let filtered = trains;
    
    switch (filterType) {
      case 'high':
        filtered = trains.filter(t => t.train_type === '高铁');
        break;
      case 'dong':
        filtered = trains.filter(t => t.train_type === '动车');
        break;
      case 'recommend':
        filtered = trains.filter(t => t.is_recommended);
        break;
      case 'discount':
        filtered = trains.filter(t => t.discount);
        break;
      default:
        filtered = trains;
    }
    
    this.setData({ filteredTrains: filtered });
  },

  // 打开购票页面
  openBook(e) {
    const train = e.currentTarget.dataset.train;
    wx.navigateTo({
      url: `/pages/book/book?train=${encodeURIComponent(JSON.stringify(train))}`
    });
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadTrains().finally(() => {
      wx.stopPullDownRefresh();
    });
  }
});
