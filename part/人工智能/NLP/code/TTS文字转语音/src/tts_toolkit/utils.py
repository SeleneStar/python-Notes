#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
提供辅助功能
"""

import asyncio
from typing import List, Dict

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False


async def get_voices_async() -> List[Dict]:
    """
    异步获取所有可用的语音列表

    Returns:
        语音信息列表
    """
    if not EDGE_TTS_AVAILABLE:
        raise ImportError("edge-tts未安装")

    return await edge_tts.list_voices()


def list_voices(locale: str = "zh-CN") -> List[Dict]:
    """
    获取指定语言的语音列表

    Args:
        locale: 语言代码（例如：zh-CN, en-US）

    Returns:
        过滤后的语音列表
    """
    voices = asyncio.run(get_voices_async())

    if locale:
        voices = [v for v in voices if v['Locale'].startswith(locale)]

    return voices


def validate_voice(voice_name: str) -> bool:
    """
    验证声音名称是否有效

    Args:
        voice_name: 声音名称

    Returns:
        是否有效
    """
    try:
        voices = asyncio.run(get_voices_async())
        voice_names = [v['ShortName'] for v in voices]
        return voice_name in voice_names
    except:
        return False


def format_voice_info(voice: Dict) -> str:
    """
    格式化语音信息

    Args:
        voice: 语音信息字典

    Returns:
        格式化的字符串
    """
    gender_icon = "👩" if voice['Gender'] == 'Female' else "👨"
    return f"{gender_icon} {voice['ShortName']} - {voice['FriendlyName']}"


def estimate_audio_duration(text: str, rate: str = "+0%") -> float:
    """
    估算音频时长（秒）

    Args:
        text: 文本内容
        rate: 语速

    Returns:
        估算的时长（秒）
    """
    # 中文平均每分钟250-300字
    chars_per_minute = 250

    # 解析语速参数
    rate_value = 0
    if rate.startswith('+'):
        rate_value = int(rate[1:-1])
    elif rate.startswith('-'):
        rate_value = -int(rate[1:-1])

    # 调整语速
    adjusted_cpm = chars_per_minute * (1 + rate_value / 100)

    # 计算时长
    char_count = len(text)
    duration = (char_count / adjusted_cpm) * 60

    return duration


def parse_rate(rate_str: str) -> int:
    """
    解析语速字符串为数值

    Args:
        rate_str: 语速字符串（例如：+20%, -10%）

    Returns:
        语速数值
    """
    try:
        if rate_str.startswith('+'):
            return int(rate_str[1:-1])
        elif rate_str.startswith('-'):
            return -int(rate_str[1:-1])
        else:
            return 0
    except:
        return 0


def format_rate(rate_value: int) -> str:
    """
    将语速数值格式化为字符串

    Args:
        rate_value: 语速数值

    Returns:
        格式化的语速字符串
    """
    sign = "+" if rate_value >= 0 else ""
    return f"{sign}{rate_value}%"


def format_pitch(pitch_value: int) -> str:
    """
    将音调数值格式化为字符串

    Args:
        pitch_value: 音调数值

    Returns:
        格式化的音调字符串
    """
    sign = "+" if pitch_value >= 0 else ""
    return f"{sign}{pitch_value}Hz"
