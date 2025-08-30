#老实说，这个插件就是一个屎山，但腾讯的bot本来也已经屎山了
#我甚至都没来得及把图片做完，没来得及把同英雄不同流派出装做出来
import os
from botpy.message import GroupMessage
from loguru import logger

#英雄图片URL映射，这里是我以前试图使用腾讯云cos
#总之，发送图片很麻烦的，建议自己仔细看看文档
HERO_IMAGE_URLS = {
    "安娜": "https://?????/%E5%AE%89%E5%A8%9C.png",
    "源氏": "https://?????/%E6%BA%90%E6%B0%8F.png",
    "半藏": "https://?????/%E5%8D%8A%E8%97%8F.png",
    #在这里添加更多英雄的图片
}

async def handle_juedou_command(client, message: GroupMessage):
    """
    处理 /角斗领域出装 指令
    :param client: 机器人客户端实例
    :param message: 消息对象
    """
    try:
        #检查指令是否正确，有没有回复对应参数
        parts = message.content.split()
        if len(parts) != 2 or parts[0] != "/角斗领域出装":
            await message.reply(content="指令格式错误！请使用：/角斗领域出装 英雄名")
            return
        
        hero_name = parts[1]
        
        #检查是否有该英雄的图
        if hero_name not in HERO_IMAGE_URLS:
            available_heroes = "、".join(HERO_IMAGE_URLS.keys())
            await message.reply(content=f"暂不支持英雄 {hero_name} 的出装查询\n目前支持的英雄有：{available_heroes}")
            return
        
        #获取英雄对应的图片URL，就是你在上面配置的（二次开发请注意格式什么的是否对的上）
        image_url = HERO_IMAGE_URLS[hero_name]
        
        #上传图片文件
        uploadMedia = await client.api.post_group_file(
            group_openid=message.group_openid,
            file_type=1,#图片类型，如果你看了官方文档就知道这玩意不能去掉
            url=image_url
        )
        
        # 发送图片消息
        await client.api.post_group_message(
            group_openid=message.group_openid,
            msg_type=7,#富媒体类型，如果你看了官方文档就知道这玩意不能去掉
            media=uploadMedia
        )
        
        logger.info(f"角斗领域发送出装图片成功 - 英雄: {hero_name}")
    except Exception as e:
        logger.error(f"角斗领域指令处理失败: {str(e)}")
        await message.reply(content="出装图片发送失败，请稍后重试")