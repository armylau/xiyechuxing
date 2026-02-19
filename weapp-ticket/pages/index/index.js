// pages/index/index.js - 首页
const app = getApp();

Page({
  data: {
    cities: [],
    fromCity: { id: 'BJ', name: '北京' },
    toCity: { id: 'SH', name: '上海' },
    date: '',
    minDate: '',
    preference: 'fastest',
    preferenceIndex: 0,
    quickLinks: [],
    hotRoutes: []
  },

  onLoad() {
    this.initDate();
    this.setData({ 
      cities: app.globalData.cities,
      quickLinks: this.processQuickLinks(app.globalData.quickLinks),
      hotRoutes: app.globalData.hotRoutes
    });
  },

  // 处理快捷链接的样式
  processQuickLinks(links) {
    const colors = [
      { bg: '#EEF2FF', icon: '#4F6DF5' },
      { bg: '#FEF3C7', icon: '#92400E' },
      { bg: '#D1FAE5', icon: '#065F46' },
      { bg: '#FEE2E2', icon: '#991B1B' }
    ];
    return links.map((item, index) => ({
      ...item,
      color: colors[index % colors.length].bg,
      iconColor: colors[index % colors.length].icon
    }));
  },

  // 初始化日期
  initDate() {
    const today = new Date();
    const dateStr = this.formatDate(today);
    this.setData({
      date: dateStr,
      minDate: dateStr
    });
  },

  formatDate(date) {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  },

  // 打开城市选择器
  openCityPicker(e) {
    const type = e.currentTarget.dataset.type;
    wx.navigateTo({
      url: `/pages/index/city-picker?type=${type}&current=${type === 'from' ? this.data.fromCity.id : this.data.toCity.id}`
    });
  },

  // 交换城市
  swapCities() {
    const { fromCity, toCity } = this.data;
    this.setData({
      fromCity: toCity,
      toCity: fromCity
    });
  },

  // 日期变化
  onDateChange(e) {
    this.setData({ date: e.detail.value });
  },

  // 偏好变化
  onPreferenceChange(e) {
    const index = parseInt(e.detail.value);
    const preferences = ['fastest', 'cheapest', 'comfortable'];
    this.setData({ 
      preference: preferences[index],
      preferenceIndex: index
    });
  },

  // 搜索车次
  searchTrains() {
    const { fromCity, toCity, date, preference } = this.data;
    
    if (fromCity.id === toCity.id) {
      app.toast('出发和到达城市不能相同');
      return;
    }
    
    wx.navigateTo({
      url: `/pages/trains/trains?from=${fromCity.id}&to=${toCity.id}&date=${date}&preference=${preference}`
    });
  },

  // 快速搜索
  quickSearch(e) {
    const { from, to } = e.currentTarget.dataset;
    const cities = this.data.cities;
    const fromCity = cities.find(c => c.id === from) || { id: from, name: from };
    const toCity = cities.find(c => c.id === to) || { id: to, name: to };
    
    this.setData({ fromCity, toCity }, () => {
      this.searchTrains();
    });
  },

  // 下拉刷新
  onPullDownRefresh() {
    // 重新加载数据
    this.setData({
      cities: app.globalData.cities,
      quickLinks: this.processQuickLinks(app.globalData.quickLinks),
      hotRoutes: app.globalData.hotRoutes
    });
    wx.stopPullDownRefresh();
  },

  // 分享
  onShareAppMessage() {
    return {
      title: '西野出行 - 智能高铁票务',
      desc: '搜车次、查景点、订美食酒店，一站搞定！',
      path: '/pages/index/index'
    };
  }
});
