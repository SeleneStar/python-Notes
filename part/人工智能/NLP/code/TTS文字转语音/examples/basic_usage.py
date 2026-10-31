#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础使用示例
演示如何使用TTS Toolkit进行基本的文本转语音
"""

import sys
from pathlib import Path

# 添加src到路径（开发模式）
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tts_toolkit import TTSEngine


def main():
    """基础使用示例"""
    print("="*60)
    print("TTS Toolkit - 基础使用示例")
    print("="*60)

    # 创建TTS引擎
    engine = TTSEngine(default_voice="zh-CN-XiaoxiaoNeural")

    # 示例1: 基本合成
    print("\n1. 基本合成:")
    text1 = "你好，欢迎使用TTS工具包！"
    output1 = Path("../output/example1_basic.mp3")

    print(f"   文本: {text1}")
    print(f"   输出: {output1}")

    success = engine.synthesize(text1, output1)
    if success:
        print("   ✓ 合成成功")
    else:
        print("   ✗ 合成失败")

    # 示例2: 调整参数
    print("\n2. 参数调节:")
    text2 = "这是一个语速加快、音调升高的示例"
    output2 = Path("../output/example2_params.mp3")

    print(f"   文本: {text2}")
    print(f"   语速: +30%")
    print(f"   音调: +10Hz")

    success = engine.synthesize(
        text2,
        output2,
        rate="+30%",
        pitch="+10Hz"
    )
    if success:
        print("   ✓ 合成成功")

    # 示例3: 使用不同声音
    print("\n3. 更换声音:")
    text3 = "我是云扬，一个成熟的男性声音"
    output3 = Path("../output/example3_voice.mp3")

    print(f"   文本: {text3}")
    print(f"   声音: zh-CN-YunyangNeural (男声)")

    success = engine.synthesize(
        text3,
        output3,
        voice="zh-CN-YunyangNeural"
    )
    if success:
        print("   ✓ 合成成功")

    print("\n" + "="*60)
    print("示例完成！音频文件已保存到 output/ 目录")
    print("="*60)


if __name__ == "__main__":
    main()
