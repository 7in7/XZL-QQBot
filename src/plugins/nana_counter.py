import json
import os
from datetime import datetime, time, date
import logging

#配置日志
logger = logging.getLogger(__name__)

#数据文件路径
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'nana_counter.json')

#特殊时间点的爱娜tv
SPECIAL_REPLIES = {
    #凌晨12点
    time(0, 0): "你是今天第一个为娜娜献上维生立场的！好浪漫啊！",
    #早上6点
    time(6, 0): "你是今天第一个用上勾拳让娜娜起床的！拳套的充能蓝光比太阳还耀眼！",
    #晚上10点
    time(22, 0): "你是今天第一个把娜娜锤到墙上哄睡着的！抠都抠不下来！"
}


def load_counter():
    """加载计数器数据"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                #检查日期是否需要重置
                today = datetime.now().date().isoformat()
                if data.get('date') != today:
                    data['count'] = 0
                    data['date'] = today
                    data['last_reset'] = datetime.now().isoformat()
                    #重置特殊时间点触发标记
                    data['special_triggered'] = {}
                return data
        except Exception as e:
            logger.error(f"加载计数器数据失败: {e}")
            return {
                'count': 0, 
                'date': datetime.now().date().isoformat(), 
                'last_reset': datetime.now().isoformat(),
                'special_triggered': {}
            }
    else:
        return {
            'count': 0, 
            'date': datetime.now().date().isoformat(), 
            'last_reset': datetime.now().isoformat(),
            'special_triggered': {}
        }


def save_counter(data):
    """保存计数器数据"""
    try:
        #确保数据目录存在
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存计数器数据失败: {e}")


def get_special_reply(data):
    """获取特殊时间点的回复内容"""
    now = datetime.now()
    current_time = now.time()
    today = now.date().isoformat()
    
    #检查是否在特殊时间点附近（允许几分钟的误差）
    #妈的这么多if，我自己都想杀了自己
    for special_time, reply in SPECIAL_REPLIES.items():
        #允许5分钟的误差
        time_diff = abs((datetime.combine(date.today(), current_time) - datetime.combine(date.today(), special_time)).total_seconds())
        if time_diff <= 300:
            #检查今天该特殊时间点是否已经触发过
            time_key = special_time.strftime('%H:%M')
            if time_key not in data.get('special_triggered', {}):
                #标记该特殊时间点已触发
                if 'special_triggered' not in data:
                    data['special_triggered'] = {}
                data['special_triggered'][time_key] = today
                return reply
    return ""


async def handle_nana_counter(bot, message):
    """处理 /吃个娜娜 指令""" 
    try:
        data = load_counter()
        data['count'] += 1
        
        #获取特殊回复（如果有）
        special_reply = get_special_reply(data)
        
        #回复的内容
        #这个插件审核未通过，估计就是这个“曹飞“
        reply_message = f"娜娜今天已被曹飞{data['count']}次"
        if special_reply:
            reply_message += f"，{special_reply}"
        
        #保存更新后的数据
        save_counter(data)
        
        #发送回复
        await message.reply(content=reply_message)
        
    except Exception as e:
        logger.error(f"处理 /吃个娜娜 指令时出错: {e}")
        await message.reply(content="处理指令时出现错误，请稍后再试")