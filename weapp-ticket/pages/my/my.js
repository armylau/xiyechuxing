// pages/my/my.js - 个人中心页
const app = getApp();
const { DEMO_ORDERS, DEMO_POINTS } = require('../../utils/data.js');

Page({
  data: {
    activeTab: 'orders', // orders, points, safety
    // 订单
    phone: '',
    orders: [],
    useDemoOrders: false,  // 是否使用演示订单
    // 积分
    pointsPhone: '',
    pointsInfo: null,
    useDemoPoints: false,  // 是否使用演示积分
    levels: [],
    // 安全
    safetyTips: []
  },

  onLoad() {
    // 尝试加载上次使用的手机号
    const lastPhone = wx.getStorageSync('lastPhone');
    if (lastPhone) {
      this.setData({ 
        phone: lastPhone,
        pointsPhone: lastPhone
      });
    }
    
    // 使用本地安全数据
    this.setData({ 
      safetyTips: app.globalData.safetyTips,
      levels: app.globalData.pointsLevels
    });
    
    // 尝试从服务器加载安全提示
    this.loadSafetyTips();
    
    // 如果没有手机号，默认显示演示订单
    if (!lastPhone) {
      this.setDemoOrders();
    }
  },

  onShow() {
    const { activeTab, phone } = this.data;
    
    // 如果有手机号，尝试加载真实数据
    if (activeTab === 'orders') {
      if (phone) {
        this.loadOrders();
      } else {
        // 没有手机号，显示演示数据
        this.setDemoOrders();
      }
    } else if (activeTab === 'points') {
      if (this.data.pointsPhone) {
        this.loadPoints();
      } else {
        // 没有手机号，显示演示积分
        this.setDemoPoints();
      }
    }
  },

  // Tab 切换
  switchTab(e) {
    const tab = e.currentTarget.dataset.tab;
    this.setData({ activeTab: tab });
    
    if (tab === 'orders') {
      const { phone } = this.data;
      if (phone) {
        this.loadOrders();
      } else {
        this.setDemoOrders();
      }
    } else if (tab === 'points') {
      const { pointsPhone } = this.data;
      if (pointsPhone) {
        this.loadPoints();
      } else {
        this.setDemoPoints();
      }
    }
  },

  // ========== 订单相关 ==========
  
  onPhoneInput(e) {
    this.setData({ phone: e.detail.value });
  },

  // 设置演示订单
  setDemoOrders() {
    this.setData({
      orders: DEMO_ORDERS,
      useDemoOrders: true
    });
  },

  async loadOrders() {
    const { phone } = this.data;
    
    if (!phone) {
      // 没有手机号，显示演示数据
      this.setDemoOrders();
      return;
    }

    try {
      const url = `/api/orders?phone=${phone}`;
      const res = await app.request(url);
      
      if (res.code === 0) {
        const orders = (res.data || []).map(item => {
          const departTime = item.train?.depart_time 
            ? item.train.depart_time.split(' ')[1] 
            : '';
          const arriveTime = item.train?.arrive_time 
            ? item.train.arrive_time.split(' ')[1] 
            : '';
          const seatClassDisplay = item.seat_class 
            ? `${item.seat_class.icon} ${item.seat_class.name}` 
            : '二等座';
          const mealDisplay = item.meal && item.meal.id !== 'none' 
            ? `${item.meal.icon} ${item.meal.name}` 
            : '未选购';
          
          return {
            ...item,
            departTime,
            arriveTime,
            seatClassDisplay,
            mealDisplay
          };
        });
        
        // 如果真实订单为空，显示演示数据
        if (orders.length === 0) {
          this.setDemoOrders();
          wx.showToast({
            title: '暂无真实订单，显示演示数据',
            icon: 'none',
            duration: 2000
          });
        } else {
          this.setData({ 
            orders,
            useDemoOrders: false
          });
        }
      }
    } catch (err) {
      console.log('订单加载失败，使用演示数据');
      this.setDemoOrders();
      wx.showToast({
        title: '网络错误，显示演示数据',
        icon: 'none',
        duration: 2000
      });
    }
  },

  // ========== 积分相关 ==========
  
  onPointsPhoneInput(e) {
    this.setData({ pointsPhone: e.detail.value });
  },

  // 设置演示积分
  setDemoPoints() {
    this.setData({
      pointsInfo: DEMO_POINTS,
      useDemoPoints: true
    });
  },

  async loadPoints() {
    const { pointsPhone } = this.data;
    
    if (!pointsPhone) {
      this.setDemoPoints();
      return;
    }

    try {
      const res = await app.request(`/api/points?phone=${pointsPhone}`);
      if (res.code === 0 && res.data) {
        // 如果没有历史记录，添加演示历史
        if (!res.data.history || res.data.history.length === 0) {
          res.data.history = DEMO_POINTS.history;
        }
        this.setData({ 
          pointsInfo: res.data,
          useDemoPoints: false
        });
      } else {
        // 查询失败，使用演示数据
        this.setDemoPoints();
      }
    } catch (err) {
      console.log('积分加载失败，使用演示数据');
      this.setDemoPoints();
    }
  },

  // ========== 安全相关 ==========
  
  async loadSafetyTips() {
    try {
      const res = await app.request('/api/safety_tips');
      if (res.code === 0 && res.data && res.data.length > 0) {
        this.setData({ safetyTips: res.data });
      }
    } catch (err) {
      console.log('使用本地安全提示数据');
    }
  },

  // 下拉刷新
  onPullDownRefresh() {
    const { activeTab } = this.data;
    let promise;
    
    if (activeTab === 'orders') {
      promise = this.loadOrders();
    } else if (activeTab === 'points') {
      promise = this.loadPoints();
    } else {
      promise = this.loadSafetyTips();
    }

    Promise.resolve(promise).finally(() => {
      wx.stopPullDownRefresh();
    });
  }
});
