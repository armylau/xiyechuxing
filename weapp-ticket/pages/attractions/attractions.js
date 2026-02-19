// pages/attractions/attractions.js - 景点列表页
const app = getApp();

Page({
  data: {
    cities: [],
    currentCity: 'BJ',
    currentCityIndex: 0,
    currentCityName: '北京',
    attractions: [],
    loading: false
  },

  onLoad() {
    this.setData({ 
      cities: app.globalData.cities,
      currentCity: app.globalData.cities[0]?.id || 'BJ',
      currentCityIndex: 0,
      currentCityName: app.globalData.cities[0]?.name || '北京'
    });
    this.loadAttractions();
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
    this.loadAttractions();
  },

  // 加载景点 - 优先使用 API，失败使用本地数据
  async loadAttractions() {
    const { currentCity } = this.data;
    
    this.setData({ loading: true });

    // 先使用本地数据展示
    const localAttractions = app.getAttractions(currentCity);
    this.setData({ attractions: localAttractions });

    // 尝试从服务器获取最新数据
    try {
      const res = await app.request(`/api/attractions?city_id=${currentCity}`);
      if (res.code === 0 && res.data && res.data.length > 0) {
        const grads = ['grad-1', 'grad-2', 'grad-3', 'grad-4', 'grad-5', 'grad-6'];
        const attractions = res.data.map((item, index) => ({
          ...item,
          gradClass: grads[index % 6]
        }));
        this.setData({ attractions });
      }
    } catch (err) {
      console.log('使用本地景点数据');
    } finally {
      this.setData({ loading: false });
    }
  },

  // 打开景点详情
  openDetail(e) {
    const { id } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/attraction-detail/attraction-detail?id=${id}`
    });
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadAttractions().finally(() => {
      wx.stopPullDownRefresh();
    });
  }
});
