// pages/explore/explore.js - 吃住推荐页
const app = getApp();

Page({
  data: {
    cities: [],
    currentCity: 'BJ',
    currentCityIndex: 0,
    currentCityName: '北京',
    activeTab: 'food', // food 或 hotel
    foodList: [],
    hotelList: [],
    loading: false
  },

  onLoad() {
    this.setData({ 
      cities: app.globalData.cities,
      currentCity: app.globalData.cities[0]?.id || 'BJ',
      currentCityIndex: 0,
      currentCityName: app.globalData.cities[0]?.name || '北京'
    });
    this.loadData();
  },

  // 城市切换
  onCityChange(e) {
    const index = e.detail.value;
    const city = this.data.cities[index];
    this.setData({ 
      currentCity: city.id,
      currentCityIndex: index,
      currentCityName: city.name
    });
    this.loadData();
  },

  // Tab 切换
  switchTab(e) {
    const tab = e.currentTarget.dataset.tab;
    this.setData({ activeTab: tab });
    this.loadData();
  },

  // 加载数据
  async loadData() {
    if (this.data.activeTab === 'food') {
      await this.loadFoods();
    } else {
      await this.loadHotels();
    }
  },

  // 加载美食 - 优先使用 API，失败使用本地数据
  async loadFoods() {
    const { currentCity } = this.data;
    
    this.setData({ loading: true });

    // 先使用本地数据
    const localFoods = app.getFoods(currentCity);
    this.setData({ foodList: localFoods });

    // 尝试从服务器获取
    try {
      const res = await app.request(`/api/foods?city_id=${currentCity}`);
      if (res.code === 0 && res.data && res.data.length > 0) {
        this.setData({ foodList: res.data });
      }
    } catch (err) {
      console.log('使用本地美食数据');
    } finally {
      this.setData({ loading: false });
    }
  },

  // 加载酒店 - 优先使用 API，失败使用本地数据
  async loadHotels() {
    const { currentCity } = this.data;
    
    this.setData({ loading: true });

    // 先使用本地数据，处理星星显示
    let localHotels = app.getHotels(currentCity).map(item => ({
      ...item,
      starsText: '★'.repeat(item.stars || 0)
    }));
    this.setData({ hotelList: localHotels });

    // 尝试从服务器获取
    try {
      const res = await app.request(`/api/hotels?city_id=${currentCity}`);
      if (res.code === 0 && res.data && res.data.length > 0) {
        const hotels = res.data.map(item => ({
          ...item,
          starsText: '★'.repeat(item.stars || 0)
        }));
        this.setData({ hotelList: hotels });
      }
    } catch (err) {
      console.log('使用本地酒店数据');
    } finally {
      this.setData({ loading: false });
    }
  },

  // 打开地图
  openMap(e) {
    const { url } = e.currentTarget.dataset;
    if (!url) {
      app.toast('暂无地图信息');
      return;
    }
    
    wx.setClipboardData({
      data: url,
      success: () => {
        wx.showModal({
          title: '地图链接已复制',
          content: '请在浏览器中打开查看地图位置',
          showCancel: false
        });
      }
    });
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadData().finally(() => {
      wx.stopPullDownRefresh();
    });
  }
});
