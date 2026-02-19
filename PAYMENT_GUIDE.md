# 微信支付集成指南

本文档介绍如何在微信小程序中集成微信支付功能。

## 目录

1. [前置条件](#前置条件)
2. [支付流程](#支付流程)
3. [代码实现](#代码实现)
4. [测试支付](#测试支付)
5. [生产环境配置](#生产环境配置)

---

## 前置条件

### 1. 注册微信商户号

- 访问 [微信支付商户平台](https://pay.weixin.qq.com/)
- 申请成为商户（需要企业或个体户营业执照）
- 完成实名认证和协议签署

### 2. 配置小程序支付

在微信公众平台完成以下配置：

1. **关联商户号**
   - 登录小程序后台 → 微信支付 → 关联商户号
   - 输入商户号完成绑定

2. **配置支付目录**
   - 微信支付 → 开发配置 → 支付授权目录
   - 添加: `https://your-domain.com/api/payment/`

3. **获取关键配置**
   - `mchid` (商户号)
   - `api_key` (APIv3密钥)
   - `appid` (小程序AppID)
   - `serial_no` (商户证书序列号)
   - 商户证书文件 (`apiclient_cert.pem`, `apiclient_key.pem`)

---

## 支付流程

```
┌──────────────┐      1.创建订单       ┌──────────────┐
│   小程序     │ ────────────────────→ │   后端API    │
│  (book.js)   │                       │ (payment.py) │
└──────────────┘                       └──────────────┘
       │                                       │
       │ 2.返回支付参数                          │
       │ (timeStamp/nonceStr/package/paySign)    │
       │                                       │
       │←────────────────────────────────────────┘
       │
       │ 3.调起支付
       │ wx.requestPayment()
       ▼
┌──────────────┐
│   微信支付   │
│   (微信APP)  │
└──────────────┘
       │
       │ 4.支付结果回调
       ▼
┌──────────────┐
│   后端API    │
│ (notify接口) │
└──────────────┘
```

---

## 代码实现

### 方式一：模拟支付（演示/测试）

当前代码已实现模拟支付，无需真实商户号即可测试支付流程。

**特点：**
- ✅ 无需企业资质
- ✅ 无需申请商户号
- ✅ 即时到账，方便测试
- ⚠️ 仅用于开发测试

### 方式二：真实微信支付（生产环境）

#### 步骤1：安装依赖

```bash
pip install wechatpayv3
```

#### 步骤2：配置支付参数

修改 `payment.py`：

```python
WECHAT_PAY_CONFIG = {
    "mchid": "YOUR_MCHID",           # 商户号
    "appid": "YOUR_APPID",           # 小程序AppID
    "api_key": "YOUR_API_KEY",       # APIv3密钥
    "notify_url": "https://your-domain.com/api/payment/notify",
}
```

#### 步骤3：创建真实支付订单

修改 `payment.py` 中的 `create_payment_order` 函数：

```python
from wechatpayv3 import WeChatPay

# 初始化微信支付
wxpay = WeChatPay(
    wechatpay_type=WeChatPay.MINIPROG,
    mchid=WECHAT_PAY_CONFIG["mchid"],
    private_key=open('apiclient_key.pem').read(),
    cert_serial_no='YOUR_CERT_SERIAL_NO',
    appid=WECHAT_PAY_CONFIG["appid"],
    apiv3_key=WECHAT_PAY_CONFIG["api_key"],
)

def create_payment_order(order_data: dict) -> dict:
    """创建真实微信支付订单"""
    
    # 构建订单描述
    description = f"{order_data['train_no']} {order_data['from_city']}→{order_data['to_city']}"
    
    # 调用微信统一下单API
    result = wxpay.pay(
        description=description,
        out_trade_no=generate_out_trade_no(),
        amount={'total': int(order_data['total_price'] * 100)},  # 转为分
        payer={'openid': order_data['openid']},
        notify_url=WECHAT_PAY_CONFIG["notify_url"],
    )
    
    if result.get('code') == 0:
        prepay_id = result['data']['prepay_id']
        
        # 生成前端调起支付所需参数
        pay_params = wxpay.sign(
            appid=WECHAT_PAY_CONFIG["appid"],
            prepay_id=prepay_id,
        )
        
        return {
            "code": 0,
            "data": {
                "out_trade_no": result['data']['out_trade_no'],
                "pay_params": pay_params,
            }
        }
    else:
        return {"code": -1, "msg": result.get('message', '支付创建失败')}
```

#### 步骤4：处理支付回调

修改 `payment.py` 中的 `verify_payment_result`：

```python
def verify_payment_result(notify_data: dict) -> bool:
    """验证微信支付回调"""
    # 验证签名
    if not wxpay.verify_signature(notify_data):
        return False
    
    # 检查订单状态
    if notify_data.get('event_type') == 'TRANSACTION.SUCCESS':
        out_trade_no = notify_data['resource']['out_trade_no']
        # 更新订单状态为已支付
        # ...
        return True
    
    return False
```

#### 步骤5：修改后端接口

修改 `app.py` 中的支付接口调用：

```python
# 将 create_mock_payment 替换为 create_payment_order
from payment import create_payment_order, verify_payment_result

# 在 create_payment 函数中
result = create_payment_order(order_data)
```

#### 步骤6：获取用户 OpenID

小程序需要获取用户的 `openid` 才能调起支付：

```javascript
// app.js 或登录页面
wx.login({
  success: (res) => {
    // 发送 code 到后端换取 openid
    wx.request({
      url: '/api/auth/login',
      data: { code: res.code },
      success: (res) => {
        const openid = res.data.openid;
        wx.setStorageSync('openid', openid);
      }
    });
  }
});
```

后端获取 openid：

```python
import requests

def get_openid(code):
    url = f"https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": APPID,
        "secret": APP_SECRET,
        "js_code": code,
        "grant_type": "authorization_code"
    }
    resp = requests.get(url, params=params)
    return resp.json().get("openid")
```

---

## 测试支付

### 1. 开发者工具测试

1. 使用微信开发者工具预览小程序
2. 进入购票页面，填写信息
3. 点击"确认支付"
4. 由于是模拟支付，会直接显示支付成功

### 2. 真机测试

1. 点击开发者工具"真机调试"
2. 扫描二维码在手机上运行
3. 进行支付测试

### 3. 沙箱环境测试

微信支付提供沙箱环境，可使用测试商户号进行测试：

```python
# 使用沙箱环境
WECHAT_PAY_CONFIG = {
    "mchid": "沙箱商户号",
    "api_key": "沙箱密钥",
    # ...
}
```

---

## 生产环境配置

### 环境变量管理

建议将敏感配置放在环境变量中：

```python
import os

WECHAT_PAY_CONFIG = {
    "mchid": os.getenv("WECHAT_MCHID"),
    "appid": os.getenv("WECHAT_APPID"),
    "api_key": os.getenv("WECHAT_API_KEY"),
    "notify_url": os.getenv("WECHAT_NOTIFY_URL"),
}
```

### HTTPS 要求

- 生产环境必须使用 HTTPS
- 域名需要在微信支付后台配置
- 证书需要有效且未过期

### 安全注意事项

1. **API密钥保密**
   - 不要提交到代码仓库
   - 使用环境变量或密钥管理服务

2. **签名验证**
   - 必须验证微信支付回调的签名
   - 防止伪造支付通知

3. **幂等性处理**
   - 同一笔订单不要重复处理
   - 使用 out_trade_no 保证唯一性

---

## 常见问题

### Q: 调用支付时报错 "请求参数错误"

检查：
- `timeStamp` 是否为字符串
- `package` 是否包含 `prepay_id=` 前缀
- `signType` 是否为 "RSA"（V3版本）

### Q: 支付回调没有收到

检查：
- `notify_url` 是否可访问
- 是否使用了 HTTPS
- 域名是否在微信支付后台配置

### Q: 如何退款

```python
def refund(out_trade_no, refund_amount):
    result = wxpay.refund(
        out_trade_no=out_trade_no,
        out_refund_no=generate_refund_no(),
        amount={'refund': refund_amount, 'total': total_amount},
    )
    return result
```

---

## 参考文档

- [微信支付官方文档](https://pay.weixin.qq.com/wiki/doc/apiv3/index.shtml)
- [wechatpayv3 Python SDK](https://github.com/minibear2021/wechatpayv3)
- [小程序支付开发指南](https://developers.weixin.qq.com/miniprogram/dev/api/payment/wx.requestPayment.html)
