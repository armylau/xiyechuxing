// pages/attraction-detail/attraction-detail.js - 景点详情页
const app = getApp();

Page({
  data: {
    attraction: null,
    city: '',
    loading: true
  },

  onLoad(options) {
    const { id } = options;
    this.loadDetail(id);
  },

  // 加载景点详情
  async loadDetail(id) {
    this.setData({ loading: true });
    app.showLoading();

    try {
      const res = await app.request(`/api/attractions/${id}`);
      if (res.code === 0) {
        this.setData({
          attraction: res.data,
          city: res.city,
          loading: false
        });
      } else {
        app.toast('加载失败');
        wx.navigateBack();
      }
    } catch (err) {
      console.error('加载景点详情失败:', err);
      app.toast('加载失败');
      wx.navigateBack();
    } finally {
      app.hideLoading();
    }
  },

  // 打开地图
  openMap() {
    const { attraction } = this.data;
    if (!attraction || !attraction.amap_url) {
      app.toast('暂无地图信息');
      return;
    }
    
    // 复制链接或使用小程序内置地图
    wx.setClipboardData({
      data: attraction.amap_url,
      success: () => {
        wx.showModal({
          title: '地图链接已复制',
          content: '请在浏览器中打开查看地图位置',
          showCancel: false
        });
      }
    });
  },

  // 预览图片
  previewImage(e) {
    const { url } = e.currentTarget.dataset;
    const { gallery } = this.data.attraction;
    wx.previewImage({
      current: url,
      urls: gallery || [url]
    });
  }
});
