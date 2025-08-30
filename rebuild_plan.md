# 重构计划

### 现状

- 单体架构，所有插件在主文件中硬编码注册
- 紧耦合，插件与框架直接依赖
- 重复代码较多（JSON加载、日期检查等）
- 不支持热重载

### 目标

采用插件化架构，实现：

- 插件自动发现与加载
- 统一的插件接口
- 配置集中管理
- 代码复用最大化

### 1：基础搭建

**代码参考**

1. **创建插件基类**

   ```python
   class BasePlugin(ABC):
       @abstractmethod
       async def handle(self, bot, message) -> bool:
           """处理消息，返回是否已处理"""
           pass

       @property
       @abstractmethod
       def command(self) -> str:
           """命令触发词"""
           pass
   ```
2. **创建插件管理器**

   ```python
   class PluginManager:
       def __init__(self):
           self.plugins: List[BasePlugin] = []

       def load_plugins(self):
           """自动加载plugins目录下的所有插件"""
           pass
   ```

### 2：插件迁移

**将现有插件转换为新格式**

**参考mirai所使用jar包的封装**

**创建共享工具库如：**

JSON数据管理器，日期工具类，日志装饰器

### 3：主程序重构

1. **移除硬编码插件注册**
2. **实现自动路由**
3. **统一配置管理**

## 其他要补充的技术细节

使用Python的 `importlib`和 `pkgutil`实现动态加载

### 共享组件

- `DataManager`: 统一JSON文件操作
- `CacheManager`: 缓存管理
- `ConfigManager`: 配置管理
