#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试图标转换
"""
from pathlib import Path

try:
    from PIL import Image

    # 路径配置
    ROOT_DIR = Path(__file__).parent.parent
    RESOURCES_DIR = ROOT_DIR / "resources"
    ICON_PNG = RESOURCES_DIR / "logo.png"
    ICON_ICO = RESOURCES_DIR / "logo.ico"

    print(f"PNG路径: {ICON_PNG}")
    print(f"PNG存在: {ICON_PNG.exists()}")
    print(f"ICO路径: {ICON_ICO}")

    if ICON_PNG.exists():
        print("\n正在转换图标...")
        img = Image.open(ICON_PNG)

        # 转换为RGBA
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Windows标准图标尺寸
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

        # 保存为ICO
        img.save(ICON_ICO, format='ICO', sizes=icon_sizes)
        print(f"✓ 图标转换成功: {ICON_ICO}")
        print(f"ICO文件大小: {ICON_ICO.stat().st_size / 1024:.2f} KB")
    else:
        print("✗ PNG文件不存在")

except ImportError:
    print("请先安装Pillow: pip install Pillow")
except Exception as e:
    print(f"错误: {e}")
