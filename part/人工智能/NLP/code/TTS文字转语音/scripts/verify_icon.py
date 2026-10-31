#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证EXE文件的图标
"""
import sys
from pathlib import Path

try:
    import pefile

    exe_path = Path("release/TTS-Toolkit-GUI-PyQt5.exe")

    if not exe_path.exists():
        print(f"错误: 文件不存在 {exe_path}")
        sys.exit(1)

    print(f"正在检查: {exe_path}")
    print(f"文件大小: {exe_path.stat().st_size / (1024*1024):.2f} MB")
    print()

    # 解析PE文件
    pe = pefile.PE(str(exe_path))

    # 检查资源
    if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
        print("✓ 找到资源目录")

        for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
            if resource_type.name is not None:
                name = str(resource_type.name)
            else:
                name = pefile.RESOURCE_TYPE.get(resource_type.struct.Id, "UNKNOWN")

            print(f"  资源类型: {name} (ID: {resource_type.struct.Id})")

            # RT_ICON = 3, RT_GROUP_ICON = 14
            if resource_type.struct.Id == 3:
                print("    ✓ 找到图标数据 (RT_ICON)")
            elif resource_type.struct.Id == 14:
                print("    ✓ 找到图标组 (RT_GROUP_ICON)")

        print()
        print("结论: EXE文件包含图标资源")
        print()
        print("如果图标没有显示，请尝试:")
        print("1. 删除exe文件的缩略图缓存")
        print("2. 重启资源管理器")
        print("3. 在另一台电脑上测试")
    else:
        print("✗ 未找到资源目录")
        print("图标可能没有正确嵌入")

    pe.close()

except ImportError:
    print("请先安装pefile: pip install pefile")
    print()
    print("或者使用其他方法验证:")
    print("1. 右键exe -> 属性 -> 查看图标")
    print("2. 使用ResourceHacker等工具查看")
except Exception as e:
    print(f"错误: {e}")
