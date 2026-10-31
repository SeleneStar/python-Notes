#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行版本的语音合成工具 - 用于快速测试
"""

import asyncio
import sys
import argparse

try:
    import edge_tts
except ImportError:
    print("❌ edge-tts未安装！")
    print("请运行: pip install edge-tts")
    sys.exit(1)


def list_voices():
    """列出所有可用的中文声音"""
    print("📋 可用的中文语音：\n")

    async def get_voices():
        voices = await edge_tts.list_voices()
        chinese_voices = [v for v in voices if v['Locale'].startswith('zh-')]

        for i, voice in enumerate(chinese_voices, 1):
            print(f"{i:2d}. {voice['ShortName']}")
            print(f"    名称: {voice['FriendlyName']}")
            print(f"    性别: {voice['Gender']}")
            print()

    asyncio.run(get_voices())


def synthesize(text, voice, output, rate="+0%", volume="+0%", pitch="+0Hz"):
    """合成语音"""
    print(f"🔊 正在合成语音...")
    print(f"   文本: {text[:50]}{'...' if len(text) > 50 else ''}")
    print(f"   声音: {voice}")
    print(f"   输出: {output}")

    async def do_synthesize():
        communicate = edge_tts.Communicate(
            text,
            voice,
            rate=rate,
            volume=volume,
            pitch=pitch
        )
        await communicate.save(output)

    try:
        asyncio.run(do_synthesize())
        print(f"\n✅ 合成成功！文件已保存到: {output}")
    except Exception as e:
        print(f"\n❌ 合成失败: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="微软语音合成命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 列出所有可用声音
  python tts_cli.py --list

  # 合成语音（使用默认声音）
  python tts_cli.py -t "你好世界" -o output.mp3

  # 指定声音和参数
  python tts_cli.py -t "这是测试" -v zh-CN-XiaoxiaoNeural -o test.mp3 --rate +20% --pitch +5Hz

  # 从文件读取
  python tts_cli.py -f input.txt -o output.mp3
        """
    )

    parser.add_argument('-l', '--list', action='store_true',
                        help='列出所有可用的中文声音')

    parser.add_argument('-t', '--text', type=str,
                        help='要合成的文本')

    parser.add_argument('-f', '--file', type=str,
                        help='从文件读取文本')

    parser.add_argument('-v', '--voice', type=str,
                        default='zh-CN-XiaoxiaoNeural',
                        help='声音名称 (默认: zh-CN-XiaoxiaoNeural)')

    parser.add_argument('-o', '--output', type=str,
                        default='output.mp3',
                        help='输出文件路径 (默认: output.mp3)')

    parser.add_argument('--rate', type=str,
                        default='+0%',
                        help='语速 (例如: +20%%, -10%%) (默认: +0%%)')

    parser.add_argument('--volume', type=str,
                        default='+0%',
                        help='音量 (例如: +20%%, -10%%) (默认: +0%%)')

    parser.add_argument('--pitch', type=str,
                        default='+0Hz',
                        help='音调 (例如: +5Hz, -10Hz) (默认: +0Hz)')

    args = parser.parse_args()

    # 列出声音
    if args.list:
        list_voices()
        return

    # 获取文本
    text = None
    if args.text:
        text = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    # 合成语音
    synthesize(
        text=text,
        voice=args.voice,
        output=args.output,
        rate=args.rate,
        volume=args.volume,
        pitch=args.pitch
    )


if __name__ == "__main__":
    main()
