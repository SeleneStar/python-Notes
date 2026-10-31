#!/bin/bash
# TTS工具GUI启动器 - Linux/macOS版

echo "====================================="
echo " 微软语音合成工具 - PyQt5版"
echo "====================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未检测到Python3，请先安装Python3"
    exit 1
fi

# 启动GUI
python3 run_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "启动失败，可能缺少依赖包"
    echo "请运行: pip install -r requirements.txt"
fi
