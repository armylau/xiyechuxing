// pages/book/book.js - 购票页面
const app = getApp();

Page({
  data: {
    train: null,
    seatClasses: [],
    mealOptions: [],
    selectedSeat: 'second',
    selectedMeal: 'none',
    selectedSeatName: '二等座',
    selectedMealName: '不需要餐食',
    passengerName: '',
    phone: '',
    quantity: 1,
    quantityOptions: [1, 2, 3, 4, 5],
    summary: {
      ticketPrice: 0,
      mealPrice: 0,
      total: 0,
      points: 0
    },
    paying: false,  // 支付中状态
  },

  onLoad(options) {
    const train = JSON.parse(decodeURIComponent(options.train));
    
    // 预处理时间显示
    const processedTrain = {
      ...train,
      departTime: train.depart_time ? train.depart_time.split(' ')[1] : '',
      arriveTime: train.arrive_time ? train.arrive_time.split(' ')[1] : ''
    };
    
    const seatClasses = app.globalData.seatClasses;
    const mealOptions = app.globalData.mealOptions;
    
    // 获取默认选中的名称
    const defaultSeat = seatClasses.find(s => s.id === 'second');
    const defaultMeal = mealOptions.find(m => m.id === 'none');
    
    this.setData({ 
      train: processedTrain,
      seatClasses,
      mealOptions,
      selectedSeatName: defaultSeat ? defaultSeat.name : '二等座',
      selectedMealName: defaultMeal ? defaultMeal.name : '不需要餐食'
    });
    
    this.calculateSummary();
  },

  // 选择舱位
  selectSeat(e) {
    const id = e.currentTarget.dataset.id;
    const seat = this.data.seatClasses.find(s => s.id === id);
    this.setData({ 
      selectedSeat: id,
      selectedSeatName: seat ? seat.name : ''
    });
    this.calculateSummary();
  },

  // 选择餐食
  selectMeal(e) {
    const id = e.currentTarget.dataset.id;
    const meal = this.data.mealOptions.find(m => m.id === id);
    this.setData({ 
      selectedMeal: id,
      selectedMealName: meal ? meal.name : ''
    });
    this.calculateSummary();
  },

  // 数量变化
  onQuantityChange(e) {
    const index = e.detail.value;
    this.setData({ quantity: this.data.quantityOptions[index] });
    this.calculateSummary();
  },

  // 姓名输入
  onNameInput(e) {
    this.setData({ passengerName: e.detail.value });
  },

  // 手机号输入
  onPhoneInput(e) {
    this.setData({ phone: e.detail.value });
  },

  // 计算汇总
  calculateSummary() {
    const { train, selectedSeat, selectedMeal, quantity, seatClasses, mealOptions } = this.data;
    if (!train) return;

    const seat = seatClasses.find(s => s.id === selectedSeat);
    const meal = mealOptions.find(m => m.id === selectedMeal);

    // 计算票价（使用折扣价如果有）
    const basePrice = train.discount ? train.discount.price : train.price;
    const ticketPrice = Math.round(basePrice * seat.multiplier * 10) / 10;
    const mealPrice = meal.price;
    const total = Math.round((ticketPrice * quantity + mealPrice * quantity) * 10) / 10;
    const points = Math.floor(total);

    this.setData({
      summary: {
        ticketPrice,
        mealPrice,
        total,
        points
      }
    });
  },

  // 提交订单并支付
  async submitOrder() {
    const { train, selectedSeat, selectedMeal, passengerName, phone, quantity, summary } = this.data;

    // 验证
    if (!passengerName.trim()) {
      app.toast('请输入乘客姓名');
      return;
    }
    if (!/^1\d{10}$/.test(phone)) {
      app.toast('请输入正确的手机号');
      return;
    }

    this.setData({ paying: true });
    app.showLoading('正在创建订单...');

    try {
      // 步骤1: 创建支付订单
      const createRes = await app.request('/api/payment/create', 'POST', {
        train_id: train.id,
        passenger_name: passengerName.trim(),
        phone: phone.trim(),
        quantity: parseInt(quantity),
        seat_class: selectedSeat,
        meal: selectedMeal,
        openid: 'mock_openid',  // 实际应从登录态获取
        total_price: summary.total
      });

      if (createRes.code !== 0) {
        throw new Error(createRes.msg || '创建订单失败');
      }

      const { out_trade_no, pay_params, mock } = createRes.data;

      // 如果是模拟支付，直接确认成功
      if (mock) {
        app.showLoading('正在支付...');
        // 模拟支付延迟
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // 确认支付成功
        await this.confirmPayment(out_trade_no);
        return;
      }

      // 步骤2: 调起微信支付
      app.hideLoading();
      const payResult = await this.requestPayment(pay_params);
      
      if (payResult.success) {
        // 步骤3: 确认支付成功
        await this.confirmPayment(out_trade_no);
      } else {
        throw new Error(payResult.error || '支付失败');
      }

    } catch (err) {
      console.error('支付失败:', err);
      app.toast(err.message || '支付失败');
    } finally {
      this.setData({ paying: false });
      app.hideLoading();
    }
  },

  // 调起微信支付
  requestPayment(payParams) {
    return new Promise((resolve) => {
      wx.requestPayment({
        timeStamp: payParams.timeStamp,
        nonceStr: payParams.nonceStr,
        package: payParams.package,
        signType: payParams.signType || 'RSA',
        paySign: payParams.paySign,
        success: (res) => {
          console.log('支付成功:', res);
          resolve({ success: true });
        },
        fail: (err) => {
          console.log('支付失败:', err);
          // err.errCode: -1(失败), -2(取消)
          if (err.errCode === -2) {
            resolve({ success: false, error: '支付已取消' });
          } else {
            resolve({ success: false, error: err.errMsg || '支付失败' });
          }
        }
      });
    });
  },

  // 确认支付成功，创建正式订单
  async confirmPayment(outTradeNo) {
    const { train, selectedSeat, selectedMeal, passengerName, phone, quantity, summary, seatClasses, mealOptions } = this.data;
    
    app.showLoading('确认订单...');

    try {
      const seat = seatClasses.find(s => s.id === selectedSeat);
      const meal = mealOptions.find(m => m.id === selectedMeal);

      const res = await app.request('/api/payment/confirm', 'POST', {
        out_trade_no: outTradeNo,
        train_id: train.id,
        passenger_name: passengerName.trim(),
        phone: phone.trim(),
        quantity: parseInt(quantity),
        seat_class: { id: seat.id, name: seat.name, icon: seat.icon },
        meal: { id: meal.id, name: meal.name, icon: meal.icon, price: meal.price },
        total_price: summary.total
      });

      if (res.code === 0) {
        wx.showModal({
          title: '支付成功',
          content: `🎉 订单已支付！获得 ${res.points_earned} 积分`,
          showCancel: false,
          success: () => {
            // 保存手机号到本地
            wx.setStorageSync('lastPhone', phone);
            // 跳转到订单页
            wx.switchTab({
              url: '/pages/my/my'
            });
          }
        });
      } else {
        throw new Error(res.msg || '确认订单失败');
      }
    } catch (err) {
      console.error('确认支付失败:', err);
      app.toast(err.message || '确认支付失败');
    } finally {
      app.hideLoading();
    }
  }
});
