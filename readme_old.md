# 喜芝狼の二次开发指南

## 架构概述

### 1 整体结构

```
qq_bot/
├── config/.env          # 机器人认证配置
├── logs/                # 日志文件
├── data/		 # 插件所用到的数据
├── pics/		 # 还没做完的图
├── src/
│   ├── main.py          # BOT主程序
│   └── plugins/         # 插件目录
└── requirements.txt     # 依赖包，在IDE上进行安装
```

### 2 工作流程

1. 机器人启动后通过`main.py`中的`QQBot`类监听群聊@事件
2. 当收到@消息时，触发`on_group_at_message_create`方法
3. 消息经过预处理后进行插件路由
4. 根据插件注册表中的指令关键词匹配并执行对应的插件处理函数
5. 插件处理完成后返回结果

## ~~插件开发~~

~~后续准备使用统一接口进行重构，但现在还是正确的文档~~

~~知道两年后我回来可能就改了代码的逻辑就行，继续看吧~~

### 1 插件目录规范

- 所有插件需放在`src/plugins/`目录下
- 单个插件建议使用独立文件，推荐的文件名格式：`[功能名]_command.py`
- 插件文件内需包含一个主处理函数，返回给main进行处理
- 此外，别忘了import from

### 2 插件基本结构（示例）

```python
from loguru import logger

async def handle_[插件名]_command(client, message):
    """
    插件主处理函数
    :param client: 机器人客户端实例
    :param message: 消息对象
    """
    try:
        # 1. 解析消息内容
        # 2. 业务逻辑处理
        # 3. 发送回复消息
        await client.api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            content={"text": "回复内容"}
        )
        logger.info(f"[插件名] 指令处理成功")
    except Exception as e:
        logger.error(f"[插件名] 指令处理失败: {str(e)}")
```

## 消息处理

### 1 消息对象属性

常用 `message`对象属性：

- `message.content`: 消息文本内容
- `message.group_openid`: 群聊ID
- `message.id`: 消息ID
- `message.author`: 发送者信息对象
- `message.timestamp`: 消息时间戳

还有更多的建议参考官方文档

### 2 消息发送

```python
# 发送文本消息
await client.api.post_group_message(
    group_openid=message.group_openid,
    msg_type=0,  # 0表示文本类型
    content={"text": "这是一条回复消息"}
)
```

## ~~插件注册~~

### 1 插件注册表

在 `main.py`的 `on_group_at_message_create`方法中，有插件注册表：

```python
plugins = [
    ('/吃个娜娜', handle_nana_command, 10),
	#(指令关键词, 处理函数)
	# 添加新插件在此处注册
]
```

### 2 注册规则

1. **指令关键词**：必须以`/`开头，避免与普通消息冲突
2. **处理函数**：必须是异步函数，参数为`(client, message)`

## ~~开发步骤~~

### 1 开发新插件步骤

1. 在`src/plugins/`目录下创建新插件文件，如`weather_command.py`
2. 实现插件处理函数`handle_weather_command`
3. impor from
4. 在`main.py`的插件注册表中添加新插件条目

### 2 示例：天气查询插件

```python
# src/plugins/weather_command.py
from loguru import logger
import requests

async def handle_weather_command(client, message):
    """天气查询插件"""
    try:
        # 提取城市名（假设消息格式：/天气 北京）
        city = message.content.split()[1]
    
        # 调用天气API（示例）
        # response = requests.get(f"https://api.weather.com/{city}")
        # weather_data = response.json()
    
        # 发送天气信息
        await client.api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            content={"text": f"{city} 今天天气晴朗，气温25°C"}
        )
        logger.info("天气查询指令处理成功")
    except Exception as e:
        logger.error(f"天气查询指令处理失败: {str(e)}")
        await client.api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            content={"text": "查询失败，请重试"}
        )
```

然后在 `main.py`中注册：

```python
from plugins.weather_command import handle_weather_command

plugins = [
    ('/来点牢大', handle_laoda_command, 10),
    ('/天气', handle_weather_command, 9),  # 添加新插件
]
```

## 调试与日志

### 1 日志查看

日志文件位于 `logs/bot.log`，可通过日志排查问题：

```python
from loguru import logger

# 记录信息日志
logger.info("插件处理开始")

# 记录错误日志
logger.error(f"处理失败: {str(e)}")
```

### 2 调试方法

1. 在插件中添加详细日志
2. 通过`python src/main.py`启动机器人
3. 观察终端输出和日志文件
4. **很不推荐直接点击main.py的方式打开bot，如果你已经有点编程基础，听的懂我在说什么**

## 注意事项

1. **权限问题**：确保在QQ开放平台已申请所需权限
2. **错误处理**：所有插件需包含异常捕获，避免单个插件崩溃影响整体
3. **API限制**：遵守QQ开放平台API调用限制
4. **代码规范**：建议保持与现有插件一致的代码风格
5. **性能考虑**：耗时操作需使用异步处理~~目前暂时没有涉及这方面的插件，而且我也才学py没多久，靠你了，加油（~~

## API参考

### 1 核心API

- `client.api.post_group_message()`: 发送群消息
- `client.api.get_group_info()`: 获取群信息
- `client.api.get_user_info()`: 获取用户信息

### 2 消息对象方法

- `message.reply()`: 回复消息
- `message.mentions`: 获取消息中的@用户列表

## 常见问题

### Q: 插件不被触发怎么办？

A: 检查以下几点：

1. 插件是否在`main.py`中正确注册
2. 指令关键词是否匹配（区分大小写）
3. 其他的请检查QQ开发平台

### Q: 发送消息失败？

A: 检查QQ开放平台权限配置，确保已开通"群聊消息发送"权限

### Q:提示IP源不在白名单？

A：须知以下几点

1. 如果是家用或学校网络，IP一般都会变动，非常建议有个固定IP的服务器进行部署
2. IP若有变动，需要前往QQ开放平台重新配置
3. 这是QQ的要求，没办法


*文档最后编辑时间：2025.8.30  	By 7in7*
