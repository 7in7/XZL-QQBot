"""
统一配置管理模块
提供统一访问接口
"""

import os
from pathlib import Path
from typing import Dict, Any

#项目根目录
ROOT_DIR = Path(__file__).parent.parent

class Config:
    """统一配置管理类"""
    
    #路径配置
    DATA_DIR = ROOT_DIR / "data"
    CONFIG_DIR = ROOT_DIR / "config"
    LOGS_DIR = ROOT_DIR / "logs"
    
    #文件路径
    ENV_FILE = CONFIG_DIR / ".env"
    
    #数据文件
    DAILY_FORTUNE_TEXT = DATA_DIR / "daily_fortune_text.json"
    DAILY_FORTUNE_RECORD = DATA_DIR / "daily_fortune_record.json"
    OW_FORTUNE_TEXT = DATA_DIR / "ow_fortune_data.json"
    OW_FORTUNE_RECORD = DATA_DIR / "ow_fortune_record.json"
    NANA_COUNTER = DATA_DIR / "nana_counter.json"
    
    @classmethod
    def ensure_directories(cls) -> None:
        """确保必要的目录存在"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.CONFIG_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)

#初始化时确保目录存在
Config.ensure_directories()