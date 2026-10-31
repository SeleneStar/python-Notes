#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS工具GUI启动器
快速启动PyQt5图形界面
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# 导入并运行GUI
from tts_toolkit.gui_pyqt5 import main

if __name__ == "__main__":
    main()
