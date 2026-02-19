# 西野出行 · H5票务系统 - 项目指南

## 项目概述

西野出行是一个模拟的移动端 H5 票务系统，支持高铁/动车的车票购买、车次查询、智能推荐、目的地景点/美食/酒店浏览、舱位选择、餐食预订等功能。

### 核心功能

- **车次搜索**: 根据出发/到达城市和日期搜索可用车次
- **智能推荐**: 三种偏好模式（速度优先 / 价格优先 / 舒适优先）智能筛选最佳车次
- **舱位选择**: 商务座(×2.8) / 一等座(×1.6) / 二等座(×1.0)
- **餐食预订**: 6种餐食选项（含免费选项和付费套餐）
- **景点浏览**: 查看目的地热门景点介绍、评分、门票价格、开放时间
- **美食推荐**: 各城市特色美食推荐，含评分、人均价格和标签
- **酒店推荐**: 各城市不同星级酒店推荐
- **在线购票**: 选择车次、舱位、餐食，填写乘客信息，即时出票
- **订单查询**: 通过手机号查询历史购票记录
- **积分系统**: 每消费1元获得1积分，5个会员等级享受折扣
- **订单持久化**: 订单数据以 JSON 文件持久保存，重启服务不丢失

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.10+ / Flask / Flask-CORS |
| 前端 | HTML5 / CSS3 / Vanilla JS (单页应用) |
| 数据 | 内存模拟数据 + JSON 文件持久化 |
| 测试 | pytest |

## 项目结构

```
ticket_system/
├── app.py                    # Flask 后端服务（~987行，数据模型 + API）
├── requirements.txt          # Python 依赖
├── README.md                 # 项目说明（中文）
├── AGENTS.md                 # 本文件
├── data/
│   ├── orders.json           # 订单持久化存储（自动生成）
│   └── points.json           # 积分数据持久化存储
├── static/
│   └── index.html            # H5 前端单页应用（~406行）
└── tests/
    ├── conftest.py           # pytest fixtures（测试客户端、临时数据隔离）
    ├── test_amap.py          # 高德地图链接功能测试
    ├── test_attractions.py   # 景点 API 测试
    ├── test_cities.py        # 城市列表 API 测试
    ├── test_data_integrity.py # 数据完整性测试
    ├── test_discount.py      # 折扣车票 API 测试
    ├── test_foods_hotels.py  # 美食和酒店 API 测试
    ├── test_index_page.py    # 首页可访问性测试
    ├── test_orders.py        # 订单创建/查询/持久化测试
    ├── test_points.py        # 积分系统测试
    ├── test_safety.py        # 安全提醒 API 测试
    ├── test_seat_meal.py     # 舱位等级与餐食选项 API 测试
    └── test_trains.py        # 车次搜索与智能推荐 API 测试
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务

```bash
python app.py
```

服务将在 `http://localhost:5050` 启动。

### 运行测试

```bash
# 运行全部测试
pytest -v

# 运行特定测试文件
pytest tests/test_orders.py -v

# 运行特定测试类
pytest tests/test_trains.py::TestSearchTrains -v
```

## API 接口文档

### 基础数据

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/cities` | 获取城市列表（10个城市，含经纬度） |
| GET | `/api/seat_classes` | 获取舱位等级 |
| GET | `/api/meals` | 获取餐食选项 |

### 车次查询

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/trains/search?from=&to=&date=` | 搜索车次（按发车时间排序） |
| GET | `/api/trains/recommend?from=&to=&date=&preference=` | 智能推荐（最多5条） |
| GET | `/api/trains/discount?from=&to=&date=` | 折扣车票推荐 |

`preference` 可选值：`fastest`（速度优先）、`cheapest`（价格优先）、`comfortable`（舒适优先）

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

**下单请求体示例**:
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
| GET | `/api/points?phone=` | 查询用户积分信息 |
| GET | `/api/points/levels` | 获取积分等级规则 |

### 其他

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/safety_tips` | 获取出行安全提醒 |

## 代码风格指南

### Python 代码规范

1. **类型注解**: 使用 `from __future__ import annotations` 启用新类型注解语法
2. **命名规范**: 
   - 常量使用大写下划线：`CITIES`, `SEAT_CLASSES`, `ORDERS_FILE`
   - 私有函数使用下划线前缀：`_load_orders()`, `_calc_level()`
   - 类名使用驼峰命名：`TestCreateOrder`
3. **注释**: 使用中文注释，描述功能意图
4. **字符串**: 使用双引号，f-string 进行格式化

### 数据结构规范

1. **城市数据**: `{id, name, lat, lng}`
2. **舱位数据**: `{id, name, icon, multiplier, desc}`
3. **餐食数据**: `{id, name, price, icon, desc}`
4. **订单数据**: 包含订单ID、车次快照、乘客信息、价格明细、积分等

### API 响应格式

统一返回格式：
```python
{
    "code": 0,        # 0表示成功，其他表示错误
    "data": {...},    # 响应数据
    "msg": "...",     # 可选的错误信息
    "total": N        # 列表数据总数（可选）
}
```

## 测试策略

### 测试架构

- **fixtures**: `conftest.py` 提供 `client` fixture 和 `sample_train_id` fixture
- **数据隔离**: 每个测试使用临时目录 `_tmp_test_data`，测试后自动清理
- **测试分类**: 按功能模块划分测试文件，每个测试类对应一个 API 端点或功能点

### 测试约定

1. **命名规范**: 
   - 测试类：`Test<功能名>`，如 `TestCreateOrder`
   - 测试方法：`test_<场景>_<期望结果>`，如 `test_missing_params_returns_400`
2. **断言风格**: 使用 `assert` 语句，验证返回数据的结构和内容
3. **辅助函数**: 测试文件内部可定义 `_create_order()` 等辅助函数

### 运行测试的注意事项

- 测试会修改 `app_module.ORDERS`, `app_module.POINTS_FILE` 等全局变量，但通过 fixture 会自动恢复
- 测试使用内存中的模拟数据，不会影响生产环境的 `data/orders.json` 文件

## 数据持久化

### 文件存储

- `data/orders.json`: 订单列表，每条订单包含完整的车次快照
- `data/points.json`: 用户积分数据，按手机号索引

### 持久化工具函数

- `_ensure_data_dir()`: 确保数据目录存在
- `_load_orders()`: 从 JSON 加载订单
- `_save_orders(orders)`: 保存订单到 JSON
- `_load_points()`: 加载积分数据
- `_save_points(points)`: 保存积分数据

### 积分规则

- `POINTS_PER_YUAN = 1`: 每消费1元获得1积分
- 会员等级：
  - 普通会员: 0积分 (0%折扣)
  - 白银会员: 500积分 (2%折扣)
  - 黄金会员: 2000积分 (5%折扣)
  - 铂金会员: 5000积分 (8%折扣)
  - 钻石会员: 10000积分 (10%折扣)

## 模拟数据

### 城市 (10个)

北京(BJ)、上海(SH)、广州(GZ)、成都(CD)、杭州(HZ)、西安(XA)、重庆(CQ)、昆明(KM)、南京(NJ)、武汉(WH)

### 车次

- 31条路线，每条路线每天最多3个班次，共7天数据
- 车次类型：高铁(G开头) / 动车(D开头)
- 票价根据路线固定，舱位按倍率计算

### 景点、美食、酒店

- 每个城市2-3个景点，含图片、评分、门票、开放时间
- 每个城市2-4家美食推荐
- 每个城市1-3家不同档次酒店

## 开发注意事项

1. **不要修改测试文件中的测试逻辑**，测试代码是验证功能正确性的标准
2. **新增 API 时**: 需要在 `app.py` 中添加路由函数，并在 `tests/` 中添加对应测试
3. **修改数据模型时**: 注意检查 `tests/test_data_integrity.py` 中的数据完整性测试
4. **前端页面**: `static/index.html` 是一个完整的单页应用，包含所有 CSS 和 JavaScript
5. **高德地图集成**: 景点、美食、酒店数据包含 `amap_url` 字段，可跳转至高德地图

## 安全考虑

1. **数据验证**: API 端点验证必填参数，返回适当的错误码（400/404/409）
2. **文件操作**: 使用 `Path` 对象进行文件操作，避免路径注入
3. **测试隔离**: 测试使用临时目录，避免污染生产数据
4. **UUID 生成**: 订单ID使用 `uuid.uuid4().hex[:12]` 生成

## 扩展开发建议

如需添加新功能，建议遵循以下模式：

1. 在 `app.py` 中添加数据模型（常量或生成函数）
2. 添加 API 路由处理函数，返回统一的响应格式
3. 在 `tests/` 中创建对应的测试文件
4. 更新 `README.md` 和本文件的 API 文档部分
5. 如需前端支持，在 `static/index.html` 中添加对应页面和交互逻辑
