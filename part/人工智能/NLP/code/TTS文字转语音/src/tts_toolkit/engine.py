#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS引擎核心模块
提供文本转语音的核心功能
"""

import asyncio
from pathlib import Path
from typing import Optional, Union

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False


class TTSEngine:
    """文本转语音引擎"""

    def __init__(self, default_voice: str = "zh-CN-XiaoxiaoNeural"):
        """
        初始化TTS引擎

        Args:
            default_voice: 默认使用的声音
        """
        if not EDGE_TTS_AVAILABLE:
            raise ImportError("edge-tts未安装，请运行: pip install edge-tts")

        self.default_voice = default_voice

    def synthesize(
        self,
        text: str,
        output: Union[str, Path],
        voice: Optional[str] = None,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz"
    ) -> bool:
        """
        同步方式合成语音

        Args:
            text: 要合成的文本
            output: 输出文件路径
            voice: 声音名称（可选）
            rate: 语速调节（例如：+20%, -10%）
            volume: 音量调节（例如：+20%, -10%）
            pitch: 音调调节（例如：+5Hz, -10Hz）

        Returns:
            bool: 合成是否成功
        """
        try:
            asyncio.run(
                self.synthesize_async(text, output, voice, rate, volume, pitch)
            )
            return True
        except Exception as e:
            print(f"合成失败: {e}")
            return False

    async def synthesize_async(
        self,
        text: str,
        output: Union[str, Path],
        voice: Optional[str] = None,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz"
    ):
        """
        异步方式合成语音

        Args:
            text: 要合成的文本
            output: 输出文件路径
            voice: 声音名称（可选）
            rate: 语速调节
            volume: 音量调节
            pitch: 音调调节
        """
        voice = voice or self.default_voice
        output = Path(output)

        # 确保输出目录存在
        output.parent.mkdir(parents=True, exist_ok=True)

        # 创建通信对象
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate,
            volume=volume,
            pitch=pitch
        )

        # 保存音频
        await communicate.save(str(output))

    async def synthesize_stream(
        self,
        text: str,
        voice: Optional[str] = None,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz"
    ):
        """
        流式合成语音（返回音频块）

        Args:
            text: 要合成的文本
            voice: 声音名称
            rate: 语速调节
            volume: 音量调节
            pitch: 音调调节

        Yields:
            音频数据块
        """
        voice = voice or self.default_voice

        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate,
            volume=volume,
            pitch=pitch
        )

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]

    def batch_synthesize(
        self,
        texts: list,
        output_dir: Union[str, Path],
        voice: Optional[str] = None,
        rate: str = "+0%",
        volume: str = "+0%",
        pitch: str = "+0Hz",
        prefix: str = "audio"
    ) -> list:
        """
        批量合成语音

        Args:
            texts: 文本列表
            output_dir: 输出目录
            voice: 声音名称
            rate: 语速调节
            volume: 音量调节
            pitch: 音调调节
            prefix: 文件名前缀

        Returns:
            生成的文件路径列表
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        async def batch_task():
            tasks = []
            for i, text in enumerate(texts, 1):
                output = output_dir / f"{prefix}_{i:03d}.mp3"
                task = self.synthesize_async(text, output, voice, rate, volume, pitch)
                tasks.append((output, task))

            results = []
            for output, task in tasks:
                await task
                results.append(output)

            return results

        return asyncio.run(batch_task())
