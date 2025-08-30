import os
import logging

#正则表达式库，插件的匹配
#下方代码实现里也有说用config.py后续的开发可能，也许会用不到这玩意
import re
#dotenv加载环境变量
from dotenv import load_dotenv
#日志记录库
from loguru import logger
#这个库就是qq机器人的基本库
from botpy import Client

#消息库
from botpy.message import Message, GroupMessage
#插件，每写一个新的插件，都要在这里import
from plugins.ow_fortune import handle_ow_fortune
from plugins.nana_counter import handle_nana_counter
from plugins.workshop_codes import handle_workshop_codes
from plugins.daily_fortune import handle_daily_fortune
from plugins.juedou_command import handle_juedou_command
from plugins.help_command import handle_help_command
#权限系统
from botpy import Intents

#加载环境变量
#如果你想按照我这个也搞个自己的bot，记得去配置config目录下的env文件，
#Token，APP_ID和APP_SECRET是你在qq开发者平台申请的
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../config/.env'))

#统一使用os.getenv获取配置
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')
TOKEN = os.getenv('TOKEN')
LOG_FILE = os.getenv('LOG_FILE', '../logs/bot.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

logger.info(f"APP_ID loaded: {APP_ID[:4]}****")
logger.info(f"APP_SECRET loaded: {APP_SECRET[:4]}****")

os.environ['APPID'] = APP_ID
os.environ['TOKEN'] = TOKEN

#配置日志的输出
logger.add(LOG_FILE,
           level=LOG_LEVEL,
           rotation='10 MB',
           retention='7 days',
           encoding='utf-8')

class QQBot(Client):
    async def on_ready(self):
        """喜芝狼启动成功"""
        logger.info(f"{self.robot.name} 已成功启动")


    async def on_group_at_message_create(self, message: GroupMessage):
        """处理群聊@消息，路由到对应插件"""
        #理消息：移除@机器人，保留纯指令
        #能力实在有限，这里的正则表达也只能简单处理
        #建议使用config.py进行重构
        message_text = message.content
        message_text = re.sub(r'@[^\s]+\s*', '', message_text)
        message_text = message_text.strip()
        logger.info(f"[插件路由] 消息内容: {message_text}")
        #插件注册表，格式：指令关键词, 处理函数
        plugins = [
            ('/今日OW运势', handle_ow_fortune),
            ('/吃个娜娜', handle_nana_counter),
            ('/常用地图工坊代码', handle_workshop_codes),
            ('/今日运势', handle_daily_fortune),
            ('/帮助', handle_help_command),
            ('/角斗领域', handle_juedou_command),
            #后续插件都要在这里注册对应的指令
        ]

        logger.info(f"[插件路由] 已加载{len(plugins)}个插件")
        #遍历插件并执行匹配的插件
        for cmd_keyword, handler in plugins:
            if cmd_keyword in message_text:
                logger.info(f"[插件调用] 匹配到指令 '{cmd_keyword}'，开始处理")
                try:
                    await handler(self, message)
                    logger.info(f"[插件调用] 指令 '{cmd_keyword}' 处理成功")
                    break  #找到匹配插件后停止遍历
                except Exception as e:
                    logger.error(f"[插件调用] 指令 '{cmd_keyword}' 处理失败: {str(e)} 详细信息: {repr(e)}")
                    #老实说，这里遍历有明显的性能问题，并且我本就准备好了进行重构
                    #但因为个人事情，只写了个大概的config.py
                    #而这个config.py很明显还没有用到，你可以进行参考
        logger.info("所有插件处理完成")



if __name__ == "__main__":
    intents = Intents(public_messages=True)

    #喜芝狼，启动!
    bot = QQBot(
        intents=intents
    )

    try:
        bot.run(appid=APP_ID, secret=APP_SECRET)
    except Exception as e:
        logger.error(f"喜芝狼启动失败: {str(e)}")
        raise