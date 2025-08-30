import json
import random
import logging
import os
from datetime import datetime, date
from pathlib import Path
from botpy.message import Message


logger = logging.getLogger(__name__)

#相对路径
daily_fortune_text = Path(__file__).parent.parent.parent / 'data' / 'daily_fortune_text.json'
daily_fortune_record = Path(__file__).parent.parent.parent / 'data' / 'daily_fortune_record.json'

#确保数据目录存在
daily_fortune_record.parent.mkdir(parents=True, exist_ok=True)

class DailyFortunePlugin:
    def __init__(self):
        self.fortunes = self._load_fortunes()
        self.user_records = self._load_records()

    def _load_fortunes(self):
        """从JSON文件加载运势数据"""
        try:
            if not daily_fortune_text.exists():
                logger.error(f"运势数据文件不存在: {daily_fortune_text}")
                return []

            with open(daily_fortune_text, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('fortunes', [])
        except Exception as e:
            logger.error(f"加载运势数据失败: {e}")
            return []

    def _load_records(self):
        """加载用户每日运势记录"""
        if not daily_fortune_record.exists():
            return {}

        try:
            #检查文件修改时间，如果是昨天，初始化
            file_mtime = datetime.fromtimestamp(daily_fortune_record.stat().st_mtime).date()
            today = date.today()
            
            if file_mtime < today:
                #清空记录
                return {}

            with open(daily_fortune_record, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_records(self):
        """保存用户每日运势记录"""
        try:
            with open(daily_fortune_record, 'w', encoding='utf-8') as f:
                json.dump(self.user_records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存用户记录失败: {e}")

    def get_fortune(self, user_id):
        """获取用户今日的运势"""
        try:
            #检查是否已有今天的记录
            if user_id in self.user_records:
                fortune_id = self.user_records[user_id]
                return self.fortunes[fortune_id] if 0 <= fortune_id < len(self.fortunes) else "今日运势获取失败"

            #随机选择一条运势
            if not self.fortunes:
                return "运势数据加载失败，检查下fortune_data.json文件"

            fortune_id = random.randint(0, len(self.fortunes) - 1)

            #记录运势
            self.user_records[user_id] = fortune_id
            self._save_records()

            return self.fortunes[fortune_id]
            
        except Exception as e:
            logger.error(f"获取用户每日运势失败: {e}")
            return "获取运势时发生错误"

fortune_plugin = DailyFortunePlugin()

async def handle_daily_fortune(bot, message):
    """处理 /今日运势 指令"""
    try:
        logger.info(f"收到今日运势指令: {message.content}")
        user_id = str(message.author.member_openid)
        selected_fortune = fortune_plugin.get_fortune(user_id)
        
        if not selected_fortune or isinstance(selected_fortune, str):
            await message.reply(content=selected_fortune or "运势文案加载失败！快去踹开发者一脚让他修复！")
            return
        #回复内容
        reply_content = f"""🎭 **今日运势**

📊 运势等级: {selected_fortune['fortuneSummary']}
⭐ 幸运指数: {selected_fortune['luckyStar']}

🎯 签文: 
{selected_fortune['signText']}

📖 解读: 
{selected_fortune['unsignText']}

✨ 祝您今儿个好运！"""
        
        #发送回复
        await message.reply(content=reply_content)
        logger.info(f"今日运势回复成功 - 用户ID: {user_id}, 运势ID: {selected_fortune['id']}")
        
    except Exception as e:
        logger.error(f"处理今日运势指令时出错: {e}")
        await message.reply(content="逻辑bug！快去踹开发者一脚让他修复！")