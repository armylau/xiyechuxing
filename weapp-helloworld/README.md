# 微信小程序 Hello World

这是一个简单的微信小程序 Hello World 示例项目，包含了小程序的基本结构和常用功能演示。

## 项目结构

```
weapp-helloworld/
├── app.js              # 小程序入口逻辑
├── app.json            # 小程序全局配置
├── app.wxss            # 小程序全局样式
├── sitemap.json        # 小程序索引配置
├── project.config.json # 项目配置文件
├── pages/
│   └── index/          # 首页
│       ├── index.js    # 页面逻辑
│       ├── index.wxml  # 页面结构
│       ├── index.wxss  # 页面样式
│       └── index.json  # 页面配置
├── utils/
│   └── util.js         # 工具函数
└── assets/             # 静态资源目录
    └── README.md
```

## 文件说明

### 全局文件

| 文件 | 说明 |
|------|------|
| `app.js` | 小程序生命周期管理、全局数据 |
| `app.json` | 页面路由、窗口样式、TabBar 等全局配置 |
| `app.wxss` | 全局 CSS 变量、通用样式类 |
| `sitemap.json` | 配置小程序页面是否可被微信索引 |

### 页面文件

每个页面由四个文件组成：

| 文件 | 必需 | 说明 |
|------|------|------|
| `.js` | 是 | 页面逻辑和数据处理 |
| `.wxml` | 是 | 页面结构（类似 HTML） |
| `.wxss` | 否 | 页面样式（类似 CSS） |
| `.json` | 否 | 页面配置（覆盖全局配置） |

## 快速开始

### 1. 安装开发者工具

1. 访问 [微信开发者工具下载页面](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
2. 下载对应系统的稳定版安装包
3. 安装并运行开发者工具

### 2. 导入项目

#### 方式一：使用测试号（推荐新手）

1. 打开微信开发者工具
2. 点击「+」新建项目
3. 选择项目目录为 `weapp-helloworld` 文件夹
4. **AppID** 选择「使用测试号」
5. 点击「确定」创建项目

#### 方式二：使用正式 AppID

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 注册小程序账号（个人/企业）
3. 在「开发」→「开发管理」→「开发设置」中获取 AppID
4. 在开发者工具中填入 AppID 创建项目

### 3. 预览效果

- 在开发者工具左侧模拟器中查看效果
- 点击「预览」按钮，用手机微信扫码在真机上测试
- 点击「真机调试」可在手机端调试代码

## 页面功能说明

### 首页 (pages/index/index)

1. **欢迎展示** - 显示 Hello World 标题和 Logo
2. **点击计数器** - 演示数据绑定和事件处理
3. **用户信息** - 演示微信授权获取用户头像和昵称
4. **功能列表** - 展示小程序特性图标

## 常用命令

```bash
# 进入项目目录
cd weapp-helloworld

# 查看项目结构
tree -L 3

# 使用 Git 初始化版本控制
git init
git add .
git commit -m "Initial commit: Hello World Mini Program"
```

## 下一步

### 添加新页面

1. 在 `app.json` 的 `pages` 数组中添加页面路径：
```json
{
  "pages": [
    "pages/index/index",
    "pages/logs/logs"    // 新增页面
  ]
}
```

2. 在 `pages/logs/` 目录下创建四个页面文件

### 添加底部 TabBar

在 `app.json` 中添加：
```json
{
  "tabBar": {
    "list": [
      {
        "pagePath": "pages/index/index",
        "text": "首页",
        "iconPath": "assets/home.png",
        "selectedIconPath": "assets/home-active.png"
      }
    ]
  }
}
```

### 发起网络请求

```javascript
wx.request({
  url: 'https://api.example.com/data',
  method: 'GET',
  success: (res) => {
    console.log(res.data);
  },
  fail: (err) => {
    console.error(err);
  }
});
```

## 发布上线

### 1. 上传代码

1. 在开发者工具中点击「上传」
2. 填写版本号和项目备注
3. 等待上传完成

### 2. 提交审核

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入「管理」→「版本管理」
3. 找到「开发版本」，点击「提交审核」
4. 填写审核信息并提交

### 3. 发布上线

审核通过后，在「版本管理」中点击「发布」即可上线。

## 参考文档

- [小程序官方文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [小程序组件库](https://developers.weixin.qq.com/miniprogram/dev/component/)
- [小程序 API 文档](https://developers.weixin.qq.com/miniprogram/dev/api/)
- [小程序设计指南](https://developers.weixin.qq.com/miniprogram/design/)

## 常见问题

**Q: 报错 "app.json: 未找到入口页面"**  
A: 检查 `app.json` 中的 `pages` 配置，确保页面文件存在且路径正确。

**Q: 无法获取用户信息**  
A: 微信已更新用户授权机制，需使用 `getUserProfile` 方法，并注意需要在真机调试。

**Q: 网络请求失败**  
A: 检查请求的域名是否已在「开发设置」→「服务器域名」中配置，或在开发者工具中开启「不校验合法域名」。
