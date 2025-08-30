import logging
from botpy.message import Message


logger = logging.getLogger(__name__)

#输出内容
WORKSHOP_CODES_CONTENT = """以下仅是喜芝狼作者个人对常用代码的收藏整理
若没找到你想要的，或是需要更多的代码
欢迎前往Overhub寻找更多的地图工坊代码

练习工具向：

哈瓦那练枪 3E4AX
漓江塔1v1 34204
安娜睡针 KX29W
更好的靶场 AAPPX
百合狙房 F9X1B
源氏安娜 8P6A2

娱乐向：

大锤碰碰车 8NHN7
猪猪钩钩乐 19962
2D守望先锋 XHC0M
麦克雷对决 22NTZ
暴打毛加 V2QH5
劲舞团 VT0KK
铁拳相扑 E1878
托马斯 2VSMM
随机超能力(v2) H94T0
僵尸拦截车 MK42G
符文 TN7QK
木头人 XB3BK

这里再次感谢Overhub站长KINDYEAR的支持
在找守望先锋游戏助手？
角斗搭配？地图工坊？战绩查询QQ机器人？社群地图整合？更多实用工具？
来overhub点cn就对了"""

async def handle_workshop_codes(bot, message):
    """处理 /常用地图工坊代码 指令"""
    try:
        logger.info(f"收到地图工坊代码指令: {message.content}")
        
        #发送固定内容回复
        await message.reply(content=WORKSHOP_CODES_CONTENT)
        
        logger.info("地图工坊代码回复发送成功")
        
    except Exception as e:
        logger.error(f"处理地图工坊代码指令时出错: {e}")
        await message.reply(content="处理指令时出现错误，请稍后再试。")