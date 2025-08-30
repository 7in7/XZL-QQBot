# XZL-QQBot

一个QQ机器人示例，基于QQ官方Python SDK开发

## 项目特色

- **简单易用**：适合Python初学者学习和二次开发（是的，我就是边学py边做的这个）
- **插件化设计**：功能模块化，易于扩展
- **功能示例**：自己做的一些功能都拿出来当示例了

## 快速开始

### 环境要求

- Python 3.7+
- Windows/Mac/Linux 均可运行

### 1. 克隆项目

```bash
git clone https://github.com/7in7/XZL-QQBot
cd XZL-QQBot
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置机器人

1. 复制配置文件模板：

   ```bash
   cp config/.env.example config/.env
   ```
2. 编辑 `config/.env` 文件，填入你的QQ机器人配置：

   ```
   APP_ID=你的APP_ID
   APP_SECRET=你的APP_SECRET
   TOKEN=你的TOKEN
   ```
3. **如何获取配置？** 前往 [QQ开放平台](https://bot.qq.com/) 创建机器人应用获取

### 4. PyCharm打开项目

~~（我反正是这样搞的，作为初学者也不怎么懂）~~

1. 打开PyCharm
2. 点击 "File" → "Open" → 选择项目文件夹
3. PyCharm会自动识别Python解释器和依赖

### 5. 运行机器人

```bash
python src/main.py
```

## 项目结构

```
simple_pyqqbot_sample/
├── src/
│   ├── main.py              # 主程序入口
│   └── plugins/             # 功能插件目录
├── data/                    # 数据文件
├── config/
│   └── .env                # 环境配置
├── logs/                    # 日志文件
├── requirements.txt         # Python依赖
└── LICENSE                  # 开源协议
```

## 二次开发指南

### 添加新功能

1. 在`src/plugins/` 创建新插件文件
2. 实现处理函数，参考现有插件格式
3. 在`main.py` 的插件列表中注册

### 示例：天气插件

```python
# src/plugins/weather.py
async def handle_weather_command(bot, message):
    # 你的天气查询逻辑
    await message.reply(content="今天天气晴朗！")
```

然后在 `main.py` 中添加：

```python
from plugins.weather import handle_weather_command

plugins = [
    # ... 其他插件
    ('/天气', handle_weather_command),
]
```

## 技术文档

- **框架**：基于腾讯官方`qq-botpy` SDK
- **日志**：使用`loguru` 进行日志管理
- **配置**：使用`.env` 文件管理配置
- **数据**：JSON文件存储用户数据

## 贡献指南

这是一个个人学习示例项目，欢迎：

- √直接拿去用
- √个性化改造
- √学习参考
- √分享传播

## 开源协议

本项目采用 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。

## 常见问题

### Q: 机器人没反应？

A: 检查.env配置是否正确，确保网络通畅

### Q: 如何调试？

A: 查看 `logs/bot.log` 日志文件~~(目前有拉屎到上级目录的情况，能力有限不知道怎么修)~~

### Q: 支持私聊/频道吗？

A: 当前版本只支持群聊@消息，可自行扩展

### Q: 需要服务器吗？

A: 本地运行即可，~~但需保持网络稳定~~ (根据腾讯要求，IP变动需要在开放平台重新添加白名单)

## API参考

### 机器人API

基于腾讯官方 `qq-botpy` SDK，完整文档参考：

- [官方文档](https://bot.qq.com/wiki/)
- [SDK源码](https://github.com/tencent-connect/botpy)

---

那么，开始实验吧！

> 这是一个学习项目，代码可能不够完美，且有AI部分，欢迎随意改造！
