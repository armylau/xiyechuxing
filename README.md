# 🚄 西野出行 · 票务系统

一个模拟的移动端票务系统，支持高铁/动车车票购买、车次查询、智能推荐、目的地景点/美食/酒店浏览、舱位选择、餐食预订等功能。提供 **H5 网页版** 与 **微信小程序** 两种前端，共用同一套 Flask 后端 API。

## 功能特性

- **车次搜索** — 根据出发/到达城市和日期搜索可用车次
- **智能推荐** — 三种偏好模式（速度优先 / 价格优先 / 舒适优先）智能筛选最佳车次，并给出推荐理由
- **舱位选择** — 商务座 / 一等座 / 二等座，价格按倍率自动计算
- **餐食预订** — 红烧牛肉、番茄鸡肉、素食养生、儿童欢乐餐、零食饮料包等多种选项
- **景点浏览** — 查看目的地热门景点介绍、评分、门票价格、开放时间及游玩攻略
- **美食推荐** — 各城市特色美食推荐，含评分、人均价格和标签
- **酒店推荐** — 各城市不同星级酒店推荐，含价格、距离和特色标签
- **在线购票** — 选择车次、舱位、餐食，填写乘客信息，即时出票
- **订单查询** — 通过手机号查询历史购票记录
- **积分系统** — 每消费 1 元得 1 积分，5 个会员等级享受折扣
- **订单持久化** — 订单数据以 JSON 文件持久保存，重启服务不丢失

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.10+ / Flask / Flask-CORS |
| 前端（H5） | HTML5 / CSS3 / Vanilla JS（单页应用） |
| 前端（小程序） | 微信小程序（WXML / WXSS / 原生 JS） |
| 数据 | 内存模拟数据 + JSON 文件持久化（订单、积分） |
| 测试 | pytest |

## 快速开始

### 后端服务（H5 与小程序共用）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务
python app.py

# 3. 浏览器访问 H5 版
# http://localhost:5050
```

### H5 网页版

启动后端后，在浏览器打开 `http://localhost:5050` 即可使用完整功能。

### 微信小程序版

小程序位于 `weapp-ticket/` 目录，与 H5 共用同一套 API，并支持**离线数据**（网络不可用时回退到本地数据）。

1. 安装 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
2. 用开发者工具打开项目下的 `weapp-ticket` 文件夹
3. 在 `app.js` 中配置 `apiBase: 'http://localhost:5050'`（开发时可勾选「不校验合法域名」）
4. 在 `assets/icons/` 下添加 TabBar 图标（详见 [weapp-ticket/README.md](weapp-ticket/README.md)）

详细配置、域名、发布说明见 **[weapp-ticket/README.md](weapp-ticket/README.md)**。

## 运行测试

```bash
# 安装测试依赖
pip install pytest

# 执行全部测试
pytest -v
```

## 项目结构

```
ticket_system/
├── app.py                    # Flask 后端服务（数据模型 + API）
├── requirements.txt          # Python 依赖
├── README.md                 # 项目说明
├── AGENTS.md                 # 开发/协作指南
├── data/
│   ├── orders.json           # 订单持久化存储（自动生成）
│   └── points.json           # 积分数据持久化存储
├── static/
│   └── index.html            # H5 前端单页应用
├── weapp-ticket/             # 微信小程序前端
│   ├── app.js, app.json      # 小程序入口与全局配置
│   ├── utils/
│   │   ├── api.js            # API 封装
│   │   └── data.js           # 本地数据（离线回退）
│   ├── pages/                # 首页、车次、购票、景点、吃住、我的等页面
│   └── README.md             # 小程序配置与发布说明
└── tests/
    ├── conftest.py           # pytest fixtures
    ├── test_cities.py        # 城市列表 API 测试
    ├── test_trains.py        # 车次搜索与智能推荐 API 测试
    ├── test_seat_meal.py     # 舱位等级与餐食选项 API 测试
    ├── test_orders.py        # 订单创建/查询/持久化测试
    ├── test_points.py        # 积分系统测试
    └── ...                   # 其他 API 与数据完整性测试
```

## API 接口

### 基础数据

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/cities` | 获取城市列表（10个城市，含经纬度） |
| GET | `/api/seat_classes` | 获取舱位等级（商务座/一等座/二等座） |
| GET | `/api/meals` | 获取餐食选项（6种可选） |

### 车次查询

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/trains/search?from=&to=&date=` | 搜索车次（按发车时间排序） |
| GET | `/api/trains/recommend?from=&to=&date=&preference=` | 智能推荐（返回最多5条，附推荐理由） |
| GET | `/api/trains/discount?from=&to=&date=` | 折扣车票推荐 |

> `preference` 可选值：`fastest`（速度优先）、`cheapest`（价格优先）、`comfortable`（舒适优先）

### 目的地信息

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/attractions?city_id=` | 查询城市景点列表 |
| GET | `/api/attractions/<attraction_id>` | 查询景点详情（含图库、攻略） |
| GET | `/api/foods?city_id=` | 查询城市美食推荐 |
| GET | `/api/hotels?city_id=` | 查询城市酒店推荐 |

### 订单管理

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/orders` | 购票下单（含舱位、餐食选择） |
| GET | `/api/orders?phone=` | 按手机号查询订单 |

#### 下单请求体示例

```json
{
  "train_id": "G1001-20260218",
  "passenger_name": "张三",
  "phone": "13800138000",
  "quantity": 2,
  "seat_class": "business",
  "meal": "meal_a"
}
```

### 积分系统

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/points?phone=` | 查询用户积分与等级 |
| GET | `/api/points/levels` | 获取积分等级规则 |

### 其他

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/safety_tips` | 出行安全提醒 |

## 模拟数据

- **10 个城市**：北京、上海、广州、成都、杭州、西安、重庆、昆明、南京、武汉
- **31 条路线**：覆盖主流高铁/动车路线，每条路线每天最多 3 个班次，共 7 天数据
- **20+ 个景点**：每个城市 2-3 个知名景点，含详细介绍、评分、门票价格、开放时间和游玩贴士
- **30+ 家美食**：每个城市 2-4 家特色餐厅，含评分、人均价格和地址
- **20+ 家酒店**：每个城市 1-3 家不同档次酒店，从青旅到五星级全覆盖
- **3 种舱位**：商务座（×2.8）、一等座（×1.6）、二等座（×1.0）
- **6 种餐食**：含免费选项和 25-45 元付费套餐
