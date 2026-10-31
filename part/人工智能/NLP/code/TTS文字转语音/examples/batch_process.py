#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量处理示例
演示如何批量处理多个文本
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tts_toolkit import TTSEngine


def main():
    """批量处理示例"""
    print("="*60)
    print("TTS Toolkit - 批量处理示例")
    print("="*60)

    # 创建引擎
    engine = TTSEngine()

    # 准备文本列表
    texts = [
        "第一段：人工智能正在改变我们的生活",
        "第二段：语音合成技术越来越成熟",
        "第三段：未来将有更多应用场景",
        "第四段：让我们拥抱科技的进步",
        "第五段：创造更美好的明天",
    ]

    print(f"\n准备批量处理 {len(texts)} 段文本...\n")

    # 批量合成
    output_dir = Path("../output/batch")
    results = engine.batch_synthesize(
        texts=texts,
        output_dir=output_dir,
        prefix="segment",
        rate="+10%"
    )

    # 显示结果
    print("\n批量处理完成！")
    print(f"共生成 {len(results)} 个音频文件:\n")

    for i, output_file in enumerate(results, 1):
        size = output_file.stat().st_size / 1024
        print(f"  {i}. {output_file.name} ({size:.1f} KB)")

    print(f"\n文件保存在: {output_dir}")


if __name__ == "__main__":
    main()
