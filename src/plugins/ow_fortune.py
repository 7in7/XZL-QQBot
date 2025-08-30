import os
import random
import json
import logging
from datetime import datetime, date
from pathlib import Path

logger = logging.getLogger(__name__)

#相对路径
ow_fortune_text = Path(__file__).parent.parent.parent / 'data' / 'ow_fortune_data.json'
ow_fortune_record = Path(__file__).parent.parent.parent / 'data' / 'ow_fortune_record.json'

#确保数据目录存在
ow_fortune_record.parent.mkdir(parents=True, exist_ok=True)

class OWFortunePlugin:
    def __init__(self):
        self.fortunes = self._load_fortunes()
        self.user_records = self._load_records()

    def _load_fortunes(self):
        """从JSON文件加载运势文案"""
        try:
            if not ow_fortune_text.exists():
                logger.error(f"运势数据文件不存在: {ow_fortune_text}")
                return []

            with open(ow_fortune_text, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('fortunes', [])
        except Exception as e:
            logger.error(f"加载运势数据失败: {e}")
            return []

    def _load_records(self):
        """加载运势记录"""
        if not ow_fortune_record.exists():
            return {}

        try:
            #检查文件修改时间，如果是昨天，初始化
            file_mtime = datetime.fromtimestamp(ow_fortune_record.stat().st_mtime).date()
            today = date.today()
            
            if file_mtime < today:
                #清空记录
                return {}

            with open(ow_fortune_record, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_records(self):
        """保存运势记录"""
        #保存位置在data中，json格式
        with open(ow_fortune_record, 'w', encoding='utf-8') as f:
            json.dump(self.user_records, f, ensure_ascii=False, indent=2)

    def get_fortune(self, user_id):
        """获取今日运势"""
        #检查是否已有今天的记录
        if user_id in self.user_records:
            return self.fortunes[self.user_records[user_id]] if 0 <= self.user_records[user_id] < len(self.fortunes) else "今日运势获取失败"

        #随机选择一条运势
        if not self.fortunes:
            return "运势数据加载失败，检查下ow运势.txt文件"

        fortune_id = random.randint(0, len(self.fortunes) - 1)
        
        #记录运势
        self.user_records[user_id] = fortune_id
        self._save_records()

        return self.fortunes[fortune_id]

fortune_plugin = OWFortunePlugin()

#处理函数，也就是main.py中调用的函数
async def handle_ow_fortune(bot, message):
    """处理指令"""
    try:
        user_id = str(message.author.member_openid)
        fortune = fortune_plugin.get_fortune(user_id)
        
        if not fortune:
            return await message.reply(content="文案加载BUG！快去踹开发者一脚让他修复！")
        
        #输出
        reply_content = f"""🎮 **OW今日运势**

{fortune}

✨ 祝您今儿个好运！"""
        
        return await message.reply(content=reply_content)
    except Exception as e:
        logger.error(f"处理OW今日运势指令时出错: {e}")
        return await message.reply(content="逻辑bug！快去踹开发者一脚让他修复！")