#!/bin/bash
# TTS Toolkit - Linux/macOS打包脚本

set -e

echo "============================================================"
echo "          TTS Toolkit - Linux/macOS打包脚本"
echo "============================================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

echo "[1/3] 检查依赖..."
echo ""

# 检查并安装PyInstaller
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "PyInstaller未安装，正在安装..."
    pip3 install pyinstaller
fi

# 检查edge-tts
if ! python3 -c "import edge_tts" &> /dev/null; then
    echo "edge-tts未安装，正在安装..."
    pip3 install edge-tts
fi

# 检查PyQt5
if ! python3 -c "import PyQt5" &> /dev/null; then
    echo "PyQt5未安装，正在安装..."
    pip3 install PyQt5
fi

echo ""
echo "[2/3] 开始打包..."
echo ""

# 运行打包脚本
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/build_exe.py"

echo ""
echo "[3/3] 打包完成!"
echo ""
echo "可执行文件位置: $SCRIPT_DIR/../release/"
echo ""
echo "============================================================"
