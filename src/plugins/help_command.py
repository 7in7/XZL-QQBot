import logging
from botpy.message import Message


logger = logging.getLogger(__name__)

#输出内容
HELP_CONTENT = """目前可用指令有几点需要注意
若没找到你想要的，或是需要更多的代码
欢迎前往Overhub寻找更多的地图工坊代码

1 任何发送给喜芝狼的文本，涉及到标点符号的英雄名，需要去掉标点，如Dva、士兵76
2 关于特殊文字的用法：字体变色，则在颜色的前面加上#，如#红色；需要用到游戏内图标的，在英雄名前面加上#，如#源氏
举例：#红色我是#安娜，请不要选出#末日铁拳

目前正在逐步更新，后续将支持更多功能，大多都会和ow有关，敬请期待！
这里再次向 overhub点cn 致谢，感谢站长KINDYEAR的支持，得以将角斗出装和地图工坊代码功能带给大家
角斗搭配？地图工坊？战绩查询QQ机器人？社群地图整合？更多守望先锋相关实用工具？
那就来overhub看看吧！"""

async def handle_help_command(bot, message):
    """处理 /帮助 指令"""
    try:
        logger.info(f"收到帮助指令: {message.content}")
        
        #发送固定内容回复
        await message.reply(content=HELP_CONTENT)
        
        logger.info("帮助回复发送成功")
        
    except Exception as e:
        logger.error(f"处理帮助指令时出错: {e}")
        await message.reply(content="处理指令时出现错误，请稍后再试。")