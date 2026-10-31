"""
TTS Toolkit - 微软语音合成工具包

一个基于edge-tts的文本转语音工具包，支持命令行和GUI操作。
"""

__version__ = "1.0.0"
__author__ = "TTS Toolkit Team"
__license__ = "MIT"

from .engine import TTSEngine
from .utils import list_voices, validate_voice

__all__ = [
    "TTSEngine",
    "list_voices",
    "validate_voice",
]
