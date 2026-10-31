#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS Toolkit - Windows EXE打包脚本
使用PyInstaller将项目打包成Windows可执行文件
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# 打包配置
APP_NAME = "TTS-Toolkit"
VERSION = "1.0.0"
AUTHOR = "TTS Toolkit Team"

# 路径配置
ROOT_DIR = Path(__file__).parent.parent
SRC_DIR = ROOT_DIR / "src"
DIST_DIR = ROOT_DIR / "dist"
BUILD_DIR = ROOT_DIR / "build"
RESOURCES_DIR = ROOT_DIR / "resources"

# 图标文件路径
ICON_PNG = RESOURCES_DIR / "logo.png"
ICON_ICO = RESOURCES_DIR / "logo.ico"

# GUI程序配置
GUI_PYQT5_CONFIG = {
    "name": "TTS-Toolkit-GUI-PyQt5",
    "script": str(SRC_DIR / "tts_toolkit" / "gui_pyqt5.py"),
    "icon": str(ICON_ICO),  # 直接使用路径，在打包时会检查
    "noconsole": True,  # GUI程序不显示控制台
}

GUI_TKINTER_CONFIG = {
    "name": "TTS-Toolkit-GUI-Tkinter",
    "script": str(SRC_DIR / "tts_toolkit" / "gui.py"),
    "icon": str(ICON_ICO),
    "noconsole": True,
}

# CLI程序配置
CLI_CONFIG = {
    "name": "tts-cli",
    "script": str(SRC_DIR / "tts_toolkit" / "cli.py"),
    "icon": str(ICON_ICO),
    "noconsole": False,  # CLI程序需要控制台
}


def convert_png_to_ico():
    """将PNG图标转换为ICO格式"""
    if not ICON_PNG.exists():
        print(f"⚠ 警告: 图标文件不存在: {ICON_PNG}")
        return False

    if ICON_ICO.exists():
        print(f"✓ ICO图标已存在: {ICON_ICO}")
        return True

    try:
        from PIL import Image
        print(f"正在转换图标: {ICON_PNG} -> {ICON_ICO}")

        # 打开PNG图片
        img = Image.open(ICON_PNG)

        # 转换为RGBA模式（如果不是的话）
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # 生成多种尺寸的图标（Windows标准尺寸）
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

        # 保存为ICO文件
        img.save(ICON_ICO, format='ICO', sizes=icon_sizes)
        print(f"✓ 图标转换成功: {ICON_ICO}")
        return True

    except ImportError:
        print("⚠ 警告: Pillow未安装，无法转换图标")
        print("  可以运行: pip install Pillow")
        print("  或者手动将logo.png转换为logo.ico")
        return False
    except Exception as e:
        print(f"⚠ 警告: 图标转换失败: {e}")
        return False


def check_requirements():
    """检查打包所需的依赖"""
    print("=" * 60)
    print("检查打包环境...")
    print("=" * 60)

    try:
        import PyInstaller
        print(f"✓ PyInstaller已安装: {PyInstaller.__version__}")
    except ImportError:
        print("✗ PyInstaller未安装")
        print("\n请先安装PyInstaller:")
        print("  pip install pyinstaller")
        return False

    # 检查edge-tts
    try:
        import edge_tts
        print(f"✓ edge-tts已安装")
    except ImportError:
        print("✗ edge-tts未安装")
        print("\n请先安装edge-tts:")
        print("  pip install edge-tts")
        return False

    # 转换图标
    print("\n检查图标文件...")
    convert_png_to_ico()

    return True


def clean_build():
    """清理之前的构建"""
    print("\n清理旧的构建文件...")

    for directory in [BUILD_DIR, DIST_DIR]:
        if directory.exists():
            print(f"  删除: {directory}")
            shutil.rmtree(directory)

    # 删除spec文件
    for spec_file in ROOT_DIR.glob("*.spec"):
        print(f"  删除: {spec_file}")
        spec_file.unlink()

    print("✓ 清理完成")


def build_executable(config):
    """构建可执行文件"""
    print("\n" + "=" * 60)
    print(f"开始打包: {config['name']}")
    print("=" * 60)

    # 构建PyInstaller命令
    cmd = [
        "pyinstaller",
        "--name", config["name"],
        "--onefile",  # 打包成单个文件
        "--clean",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR}",
    ]

    # 添加隐藏导入
    hidden_imports = [
        "edge_tts",
        "asyncio",
        "aiohttp",
        "certifi",
    ]

    for module in hidden_imports:
        cmd.extend(["--hidden-import", module])

    # GUI程序不显示控制台
    if config.get("noconsole"):
        cmd.append("--noconsole")

    # 添加图标（确保图标文件存在）
    icon_path = config.get("icon")
    if icon_path:
        icon_file = Path(icon_path)
        if icon_file.exists():
            cmd.extend(["--icon", str(icon_file)])
            print(f"使用图标: {icon_file}")
        else:
            print(f"⚠ 警告: 图标文件不存在: {icon_file}")

    # 添加脚本路径
    cmd.append(config["script"])

    # 执行打包命令
    print(f"\n执行命令:")
    print(" ".join(cmd))
    print()

    try:
        result = subprocess.run(cmd, check=True, cwd=ROOT_DIR)
        print(f"\n✓ {config['name']} 打包成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {config['name']} 打包失败!")
        print(f"错误: {e}")
        return False


def create_release_package():
    """创建发布包"""
    print("\n" + "=" * 60)
    print("创建发布包...")
    print("=" * 60)

    # 创建release目录
    release_dir = ROOT_DIR / "release"
    release_dir.mkdir(exist_ok=True)

    # 复制可执行文件
    if DIST_DIR.exists():
        for exe_file in DIST_DIR.glob("*.exe"):
            dest = release_dir / exe_file.name
            print(f"  复制: {exe_file.name}")
            shutil.copy2(exe_file, dest)

    # 创建README
    readme_content = f"""
# TTS Toolkit - Windows发布版 v{VERSION}

## 包含文件

1. TTS-Toolkit-GUI-PyQt5.exe - 图形界面版本(PyQt5, 推荐)
2. TTS-Toolkit-GUI-Tkinter.exe - 图形界面版本(Tkinter)
3. tts-cli.exe - 命令行版本

## 使用方法

### 方法1: 图形界面 (推荐)

双击运行 `TTS-Toolkit-GUI-PyQt5.exe` 或 `TTS-Toolkit-GUI-Tkinter.exe`

在界面中:
1. 输入要转换的文本
2. 选择语音类型
3. 调整语速、音量、音调
4. 点击"合成语音"按钮
5. 等待生成完成

### 方法2: 命令行

打开命令提示符(CMD)或PowerShell，运行:

```cmd
# 基本用法
tts-cli.exe -t "你好世界" -o output.mp3

# 查看帮助
tts-cli.exe --help

# 列出所有可用声音
tts-cli.exe --list

# 指定声音和参数
tts-cli.exe -t "测试文本" -v zh-CN-XiaoxiaoNeural --rate +20% -o output.mp3
```

## 支持的语言

- 中文（普通话、粤语、台湾话）
- 英语（美式、英式、澳式等）

## 注意事项

1. 首次运行需要联网下载语音数据
2. 生成的音频文件默认保存在 `output_audio` 目录
3. 支持的输出格式: MP3, WAV, OGG

## 系统要求

- Windows 7/8/10/11 (64位)
- 网络连接

## 问题反馈

如有问题，请访问: https://github.com/yourusername/tts-toolkit/issues

## 版本信息

版本: {VERSION}
构建时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
完全免费 | 基于微软Edge TTS
"""

    readme_file = release_dir / "README.txt"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"✓ 发布包已创建: {release_dir}")
    print(f"\n包含文件:")
    for file in release_dir.iterdir():
        size = file.stat().st_size / (1024 * 1024)  # MB
        print(f"  - {file.name} ({size:.2f} MB)")


def main():
    """主函数"""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "TTS Toolkit - Windows打包工具" + " " * 18 + "║")
    print("╚" + "═" * 58 + "╝\n")

    # 检查环境
    if not check_requirements():
        print("\n请先安装所需依赖后再运行此脚本")
        return 1

    # 清理旧文件
    clean_build()

    # 打包各个版本
    configs = []

    # 询问用户要打包哪些版本
    print("\n请选择要打包的版本:")
    print("1. PyQt5 GUI版本 (推荐)")
    print("2. Tkinter GUI版本")
    print("3. CLI命令行版本")
    print("4. 全部打包")

    choice = input("\n请输入选项 (1-4) [默认: 4]: ").strip() or "4"

    if choice == "1":
        configs.append(GUI_PYQT5_CONFIG)
    elif choice == "2":
        configs.append(GUI_TKINTER_CONFIG)
    elif choice == "3":
        configs.append(CLI_CONFIG)
    else:  # 默认打包全部
        configs = [GUI_PYQT5_CONFIG, GUI_TKINTER_CONFIG, CLI_CONFIG]

    # 执行打包
    success_count = 0
    for config in configs:
        if build_executable(config):
            success_count += 1

    # 创建发布包
    if success_count > 0:
        create_release_package()

        print("\n" + "=" * 60)
        print("✓ 打包完成!")
        print("=" * 60)
        print(f"\n成功打包 {success_count}/{len(configs)} 个版本")
        print(f"\n发布包位置: {ROOT_DIR / 'release'}")
        print("\n您可以将 release 文件夹分发给其他用户使用")
    else:
        print("\n" + "=" * 60)
        print("✗ 打包失败!")
        print("=" * 60)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
