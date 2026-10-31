#!/bin/bash
# Linux/macOS安装脚本

echo "============================================"
echo "   TTS Toolkit 安装程序"
echo "============================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3"
    echo "请安装Python 3.7+"
    exit 1
fi

echo "[1/3] 检测Python环境..."
python3 --version

echo ""
echo "[2/3] 安装依赖包..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "[警告] 安装失败，尝试使用国内镜像..."
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
fi

echo ""
echo "[3/3] 安装TTS Toolkit..."
pip3 install -e .

echo ""
echo "============================================"
echo "   安装完成！"
echo "============================================"
echo ""
echo "使用方法:"
echo "  命令行: tts-cli -t '你好' -o output.mp3"
echo "  GUI界面: tts-gui"
echo "  Python: python3 -m tts_toolkit.cli --help"
echo ""
echo "查看文档:"
echo "  README.md"
echo "  docs/usage.md"
echo ""
