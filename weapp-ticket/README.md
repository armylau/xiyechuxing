# 西野出行 - 微信小程序版

这是西野出行 H5 票务系统的微信小程序版本，完整保留了原 H5 的所有功能。

## 功能特性

- 🚄 **车次搜索** - 根据出发/到达城市和日期搜索可用车次
- ⭐ **智能推荐** - 三种偏好模式（速度优先/价格优先/舒适优先）
- 💺 **舱位选择** - 商务座/一等座/二等座
- 🍱 **餐食预订** - 6种餐食选项
- 🏞️ **景点浏览** - 目的地热门景点
- 🍜 **美食推荐** - 各城市特色美食
- 🏨 **酒店推荐** - 各城市酒店推荐
- 🎫 **在线购票** - 选择车次、舱位、餐食，填写乘客信息
- 📋 **订单查询** - 通过手机号查询历史订单
- ⭐ **积分系统** - 5个会员等级享受折扣

## 离线数据支持

小程序内置完整的本地数据，即使后端服务不可用或网络不佳时，也能正常浏览：

- ✅ **10个城市** - 北京、上海、广州、成都、杭州、西安、重庆、昆明、南京、武汉
- ✅ **30+景点** - 每个城市2-3个热门景点（含图片、评分、门票、攻略）
- ✅ **40+美食** - 各城市特色美食推荐
- ✅ **20+酒店** - 不同档次酒店推荐
- ✅ **安全提醒** - 6条出行安全提示
- ✅ **积分等级** - 5个会员等级规则

数据文件位于 `utils/data.js`，API 请求失败时会自动回退到本地数据。

## 项目结构

```
weapp-ticket/
├── app.js                 # 小程序入口
├── app.json               # 全局配置
├── app.wxss               # 全局样式
├── sitemap.json           # 搜索索引配置
├── project.config.json    # 项目配置
├── utils/
│   ├── api.js            # API 封装
│   └── data.js           # 本地数据（离线使用）
├── assets/
│   └── icons/            # TabBar 图标（需自行添加）
└── pages/
    ├── index/            # 首页 - 车次搜索
    │   ├── index.js
    │   ├── index.wxml
    │   ├── index.wxss
    │   ├── index.json
    │   ├── city-picker.js    # 城市选择器
    │   ├── city-picker.wxml
    │   └── city-picker.wxss
    ├── trains/           # 车次结果页
    │   ├── trains.js
    │   ├── trains.wxml
    │   ├── trains.wxss
    │   └── trains.json
    ├── book/             # 购票页
    │   ├── book.js
    │   ├── book.wxml
    │   ├── book.wxss
    │   └── book.json
    ├── attractions/      # 景点列表页
    │   ├── attractions.js
    │   ├── attractions.wxml
    │   ├── attractions.wxss
    │   └── attractions.json
    ├── attraction-detail/# 景点详情页
    │   ├── attraction-detail.js
    │   ├── attraction-detail.wxml
    │   ├── attraction-detail.wxss
    │   └── attraction-detail.json
    ├── explore/          # 吃住推荐页
    │   ├── explore.js
    │   ├── explore.wxml
    │   ├── explore.wxss
    │   └── explore.json
    └── my/               # 个人中心页
        ├── my.js
        ├── my.wxml
        ├── my.wxss
        └── my.json
```

## 快速开始

### 1. 安装微信开发者工具

下载地址：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html

### 2. 配置后端 API

修改 `app.js` 中的 `apiBase` 为你的后端服务地址：

```javascript
// 开发环境（本地）
apiBase: 'http://localhost:5050'

// 生产环境（需要 HTTPS）
apiBase: 'https://your-domain.com'
```

### 3. 配置服务器域名

在微信小程序后台「开发」→「开发设置」→「服务器域名」中添加：

- **request 合法域名**: 你的 API 域名（必须 HTTPS）

**注意**: 开发阶段可以在开发者工具中开启「不校验合法域名」进行测试。

### 4. 添加 TabBar 图标

在 `assets/icons/` 目录下添加以下图标文件：

- `home.png` / `home-active.png` - 首页
- `attraction.png` / `attraction-active.png` - 景点
- `food.png` / `food-active.png` - 吃住
- `my.png` / `my-active.png` - 我的

图标建议使用 81x81px 的 PNG 格式。

### 5. 导入项目

1. 打开微信开发者工具
2. 点击「+」新建项目
3. 选择 `weapp-ticket` 文件夹
4. AppID 选择「使用测试号」或填入你的正式 AppID
5. 点击「确定」创建项目

### 6. 预览

- 在模拟器中查看效果
- 点击「预览」用手机微信扫码真机测试

## 后端服务部署

小程序需要连接后端 API 服务，请确保：

1. 启动 Flask 后端服务
2. 配置 CORS 允许小程序域名访问
3. 生产环境使用 HTTPS

### 修改 Flask 后端支持小程序

在 `app.py` 中添加小程序域名到 CORS：

```python
# 开发环境
CORS(app, origins=["*"])

# 生产环境
CORS(app, origins=[
    "https://servicewechat.com",
    "https://mp.weixin.qq.com"
])
```

### 使用内网穿透（开发测试）

如果没有公网服务器，可以使用内网穿透工具：

```bash
# 使用 ngrok
ngrok http 5050

# 或使用花生壳等工具
```

将获得的 HTTPS 地址配置到小程序的 `apiBase` 和服务器域名中。

## 发布上线

### 1. 准备条件

- 注册微信小程序账号（个人/企业）
- 完成实名认证
- 配置服务器域名（HTTPS）

### 2. 上传代码

1. 在微信开发者工具中点击「上传」
2. 填写版本号和项目备注
3. 等待上传完成

### 3. 提交审核

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入「版本管理」
3. 找到「开发版本」，点击「提交审核」
4. 填写审核信息

### 4. 发布

审核通过后，在「版本管理」中点击「发布」即可上线。

## 与 H5 的差异

| 功能 | H5 | 小程序 |
|------|-----|--------|
| 地图导航 | 直接跳转高德地图网页 | 复制地图链接 |
| 存储 | localStorage | wx.setStorageSync |
| 网络请求 | fetch | wx.request |
| 页面切换 | JS 控制显示隐藏 | 页面跳转 |
| 底部导航 | CSS 实现 | TabBar 配置 |

## 常见问题

**Q: 真机调试时请求失败**
A: 检查「开发设置」→「服务器域名」是否已配置，或开启「不校验合法域名」。

**Q: 无法加载图片**
A: 确保图片域名已添加到「服务器域名」→「downloadFile 合法域名」。

**Q: 后端接口返回 CORS 错误**
A: 在 Flask 中配置正确的 CORS origins，使用 `flask-cors` 扩展。

**Q: 没有 TabBar 图标**
A: 需要自行添加图标文件到 `assets/icons/` 目录。

## API 列表

完整 API 列表参见原 H5 项目文档，小程序使用相同的 API 接口。

## 开发建议

1. 开发时使用本地后端，测试时使用内网穿透
2. 生产环境务必使用 HTTPS
3. 图片资源建议使用 CDN 加速
4. 接口做好错误处理和重试机制
